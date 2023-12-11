#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

try:
    import asyncio
    from typing import Union, Dict, Tuple, Callable, Awaitable, List
except ImportError:
    import uasyncio as asyncio

from enum import IntEnum
from struct import pack, unpack
from math import radians
from .completer import Completer
from .packet import Packet
from .utils import bound, is_web
from .color import Color
from .backend.backend import Backend
from .event import Event
from .getter_types import Bumpers, TouchSensors, CliffSensor, MotorStall, Battery, Pose
import signal
import sys


def _exit_handler(signal, frame):
    print('Caught keyboard interrupt, program stopping.')
    sys.exit(0)


class Robot:
    """Base class for mobile robots."""
    DEFAULT_TIMEOUT = 3

    # Speed.
    MAX_SPEED = 500  # cm/s

    # Direction.
    class Dir(IntEnum):
        LEFT = 0
        RIGHT = 1

    # LED lights.
    class LightPattern(IntEnum):
        OFF = 0
        ON = 1
        BLINK = 2
        SPIN = 3

    # For the stall event.
    class StallMotor(IntEnum):
        LEFT = 0
        RIGHT = 1
        MARKER = 2  # Reserved for robots with a physical marker.

    class StallCause(IntEnum):
        NO_STALL = 0
        OVER_CURRENT = 1
        UNDER_CURRENT = 2
        UNDER_SPEED = 3
        SATURATED_PID = 4
        TIMEOUT = 5

    # Empty class for containing robot-specific variables
    class Vars:
        pass

    def __init__(self, backend: Backend):
        self._backend = backend
        self.on_data_reception = getattr(self._backend, 'on_data_reception', None)  # Events based backend?
        if callable(self.on_data_reception):
            self.on_data_reception(self.data_reception)

        self.pose = Pose()

        self._inc = 0
        self._run = False
        self._disable_motors = False
        self._loop = asyncio.get_event_loop()
        self._responses: Dict[Tuple[int, int, int], Completer] = {}

        self._events = {
            # (dev, cmd): event_handler(packet)
            (0, 4): self._when_stop_button_handler,
            (1, 29): self._when_motor_stalled_handler,
            (12, 0): self._when_bumped_handler,
            (14, 0): self._when_battery_handler,
            (17, 0): self._when_touched_handler,
            (20, 0): self._when_cliff_sensor_handler,
        }
        self._when_play: list[Event] = []
        self._when_stop_button: list[Event] = []
        self._when_motor_stalled: list[Event] = []
        self._when_bumped: list[Event] = []
        self._when_battery: list[Event] = []
        self._when_touched: list[Event] = []
        self._when_cliff_sensor: list[Event] = []

        # Automatically updated getters.
        self.motor_stall = MotorStall()
        self.bumpers = Bumpers()
        self.battery = Battery()
        self.touch_sensors = TouchSensors()
        self.cliff_sensor = CliffSensor()

        self.sound_enabled = True

        # Whether or not the local pose estimate should use the robot's estimate or calculate locally
        self.USE_ROBOT_POSE = False
        # Default to no turn angle compensation
        self._turn_scale_comp = 1.0 # percentage of turn to scale input
        self._turn_bias_comp = 0.0  # percentage of absolute value of turn angle to add to turn

        # Initialize class to hold robot-specific variables
        self.vars = self.Vars()

        # Catch all signals and direct to the _exit_handler
        signal.signal(signal.SIGINT, _exit_handler)
        signal.signal(signal.SIGTERM, _exit_handler)

        try:
            signal.signal(signal.SIGTSTP, _exit_handler)
            signal.signal(signal.SIGQUIT, _exit_handler)
            signal.signal(signal.SIGHUP, _exit_handler)
        except AttributeError:
            pass # these signals do not exist in Windows

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def _finished(self):
        """Ensures that the robot resets its state when the program is finished neatly."""
        if self._run and await self._backend.is_connected():
            await self.stop()
            await self.disconnect()
            await self._backend.disconnect()

    @property
    def inc(self):
        """Access then increment wrapping id."""
        inc = self._inc
        self._inc += 1
        if self._inc > 255:
            self._inc = 0
        return inc

    def data_reception(self, data):
        # Only tries to run tasks triggered by BLE events if the program is running.
        if self._run:
            # print('🦋 ', data) # Debug.
            packet = Packet.from_bytes(bytes(data))
            self._decode_packet(packet)

    def _decode_packet(self, packet):
        """"A received packet can either be an event or a response to a command. The callback function for an event is run in a new async coroutine. A command response unblocks the command's async coroutine with received data."""
        # Check CRC.
        if not packet.check_crc():
            return

        # Check if packet is an event.
        key = (packet.dev, packet.cmd)
        if key in self._events.keys():
            self._loop.create_task(self._events[key](packet))
            return

        # Check if packet is a command response.
        key = (packet.dev, packet.cmd, packet.inc)
        if key in self._responses.keys():
            completer = self._responses.pop(key)
            completer.complete(packet)
            return

        # Unknown packet type if we got to here.

    async def _read_packets(self):
        """Reads and parses packets from robot."""
        while self._run and await self._backend.is_connected():
            await asyncio.sleep(0)  # Yield.
            packet = await self._backend.read_packet()
            self._decode_packet(packet)

    async def _main(self):
        # Connect to robot.
        if not await self._backend.is_connected():
            await self._backend.connect()
        self._run = True

        # Always resets the robot's state before starting the user's program.
        await self.stop()

        # The when_play event is always triggered first.
        for event in self._when_play:
            if not event.is_running:
                # print(event.task)
                self._loop.create_task(event.task(self))

        # Only in systems that are not events based, the packets must be polled.
        if not callable(self.on_data_reception):
            await self._read_packets()

    # Event Handlers.

    async def _when_stop_button_handler(self, packet: Packet):
        self._run = False
        stop_program = getattr(self._backend, 'stop_program', None)  # Events based backend?
        if callable(stop_program):
            stop_program()
        for event in self._when_stop_button:
            await event.run(self)

    async def _when_motor_stalled_handler(self, packet: Packet):
        self._disable_motors = True
        self.motor_stall.motor = packet.payload[4]
        self.motor_stall.cause = packet.payload[5]

        for event in self._when_motor_stalled:
            await event.run(self)

    async def _when_bumped_handler(self, packet: Packet):
        if len(packet.payload) > 4:
            self.bumpers.left = packet.payload[4] & 0x80 != 0
            self.bumpers.right = packet.payload[4] & 0x40 != 0

            for event in self._when_bumped:
                # An empty condition list means to trigger the event on every occurrence.
                if (not event.condition and self.bumpers.left) or (not event.condition and self.bumpers.right):  # Any.
                    await event.run(self)
                    continue
                if len(event.condition) > 1 and ((event.condition[0] and self.bumpers.left) or (event.condition[1] and self.bumpers.right)):
                    await event.run(self)

    async def _when_battery_handler(self, packet: Packet):
        self.battery.millivolts = unpack('>H', packet.payload[4:6])[0]
        self.battery.percent = packet.payload[6]

        for event in self._when_battery:
            # TODO: Add trigger? Probably not necessary.
            await event.run(self)

    async def _when_touched_handler(self, packet: Packet):
        if len(packet.payload) > 4:
            self.touch_sensors.front_left = packet.payload[4] & 0x80 != 0
            self.touch_sensors.front_right = packet.payload[4] & 0x40 != 0
            self.touch_sensors.back_right = packet.payload[4] & 0x20 != 0
            self.touch_sensors.back_left = packet.payload[4] & 0x10 != 0

            for event in self._when_touched:
                # An empty condition list means to trigger the event on every occurrence.
                not_condition = not event.condition
                any = (not_condition and self.touch_sensors.front_left) or (not_condition and self.touch_sensors.front_right) or (
                    not_condition and self.touch_sensors.back_left) or (not_condition and self.touch_sensors.back_right)
                if any:
                    await event.run(self)
                elif len(event.condition) > 1 and len(event.condition) < 3:
                    if any or ((event.condition[0] and self.touch_sensors.front_left) or
                               (event.condition[1] and self.touch_sensors.front_right)):
                        await event.run(self)
                elif len(event.condition) > 3:
                    if any or ((event.condition[0] and self.touch_sensors.front_left) or
                               (event.condition[1] and self.touch_sensors.front_right) or
                               (event.condition[2] and self.touch_sensors.back_left) or
                               (event.condition[3] and self.touch_sensors.back_right)):
                        await event.run(self)

    async def _when_cliff_sensor_handler(self, packet: Packet):
        self.cliff_sensor.disable_motors = packet.payload[4] != 0

        for event in self._when_cliff_sensor:
            # TODO: Add trigger
            await event.run(self)

    # Event Callbacks.

    def when_play(self, callback: Callable[[], Awaitable[None]]):
        """Register when play callback of type: async def fn()."""
        self._when_play.append(Event(True, callback))

    def when_stop(self, callback: Callable[[], Awaitable[None]]):
        """Register when stop callback of type async def fn()."""
        self._when_stop_button.append(Event(True, callback))

    def when_motor_stalled(self, condition: list[int, int], callback: Callable[[MotorStall], Awaitable[None]]):
        """Register when motor stall callback of type async def fn(motor: Motor, stall: Stall)."""
        self._when_motor_stalled.append(Event(condition, callback))

    def when_bumped(self, condition: list[bool, bool], callback: Callable[[Bumpers], Awaitable[None]]):
        """Register when bumper callback of type: async def fn(left: bool, right: bool)."""
        self._when_bumped.append(Event(condition, callback))

    def when_battery(self, condition: list[int, int], callback: Callable[[Battery], Awaitable[None]]):
        """Register when battery callback of type: async def fn(mV: int, percent: int)."""
        self._when_battery.append(Event(condition, callback))

    def when_touched(self, condition: list[bool, bool, bool, bool], callback: Callable[[TouchSensors], Awaitable[None]]):
        """Register when touch callback of type: async def fn(front_left: bool, front_right: bool, back_left: bool, back_right: bool)."""
        self._when_touched.append(Event(condition, callback))

    def when_cliff_sensor(self, condition: list[bool], callback: Callable[[bool], Awaitable[None]]):
        """Register when cliff callback of type: async def fn(over_cliff: bool)."""
        self._when_cliff_sensor.append(Event(condition, callback))

    # Commands.

    def play(self):
        """Start the program."""
        if self._run:
            # Calling play() more than once makes the program unpredicable.
            print('🟧 Robot program already running')
            return

        try:
            if hasattr(self._loop, 'is_running') and self._loop.is_running():
                self._main_task = self._loop.create_task(self._main())
            else:
                self._loop.run_until_complete(self._main())
        except KeyboardInterrupt:
            print('Caught keyboard interrupt exception, program stopping.')
            self._run = False
        except SystemExit:
            self._run = False
        finally:
            # This fails on the web version, so determining the platform is crucial:
            if not is_web():
                for task in asyncio.all_tasks(self._loop):
                    task.cancel()

            if not hasattr(self._loop, 'is_running') or not self._loop.is_running():
                self._loop.run_until_complete(self._finished())
                self._loop.close()

    async def stop(self):
        """Stop and reset robot."""
        await self._backend.write_packet(Packet(0, 3, self.inc))

    # TODO: Evaluate if this one needs to be async (most likely not)
    def stop_all_events(self):
        # TODO
        pass

    # TODO: Evaluate if this one needs to be async (most likely not)
    def stop_other_events(self):
        # TODO
        pass

    async def stop_sound(self):
        """Stop currently playing note."""
        await self._backend.write_packet(Packet(5, 1, self.inc))
        self.sound_enabled = False

    async def wait(self, time: Union[int, float]):
        await asyncio.sleep(time)

    async def get_versions(self, board: int) -> List[int]:
        """Get version numbers. Returns [board, fw maj, fw min, hw maj, hw min, boot maj, boot min, proto maj, proto min, patch]."""
        dev, cmd, inc = 0, 0, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, bytes([board])))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        return packet.payload[: 10] if packet else []

    async def set_name(self, name: str):
        """Set robot name."""
        utf = name.encode('utf-8')
        while len(utf) > Packet.PAYLOAD_LEN:
            name = name[: -1]
            utf = name.encode('utf-8')
        await self._backend.write_packet(Packet(0, 1, self.inc, utf))

    async def get_name(self) -> str:
        """Get robot name."""
        dev, cmd, inc = 0, 2, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        return packet.payload.decode('utf-8').rstrip('\0') if packet else ''

    async def disconnect(self):
        """Disconnect Bluetooth from robot side."""
        await self._backend.write_packet(Packet(0, 6, self.inc))

    async def enable_events(self, bitfield: bytes):
        """Enable notifications for events. Accepts 128-bit bitfield for devices 0 to 127."""
        await self._backend.write_packet(Packet(0, 7, self.inc, bitfield))

    async def disable_events(self, bitfield: bytes):
        """Disable notifications for events. Accepts 128-bit bitfield for devices 0 to 127."""
        await self._backend.write_packet(Packet(0, 9, self.inc, bitfield))

    async def get_enabled_events(self) -> bytes:
        """Return 128-bit bitfield for devices 0 to 127."""
        dev, cmd, inc = 0, 11, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        return packet.payload if packet else bytes()

    async def get_serial_number(self) -> str:
        """Get serial number string."""
        dev, cmd, inc = 0, 14, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        try:
            return packet.payload.decode('utf-8').rstrip('\0') if packet else ''
        except UnicodeDecodeError:
            return ''.join([format(b, "02X") for b in packet.payload])

    async def get_sku(self) -> str:
        """Get robot type SKU string."""
        dev, cmd, inc = 0, 15, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        return packet.payload.decode('utf-8').rstrip('\0') if packet else ''

    async def get_battery_level(self) -> Tuple[int, int]:
        # TODO: Update robot's getter.
        # Get battery level. Returns (mV, percent)
        dev, cmd, inc = 14, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        return (unpack(">H", packet.payload[4:6])[0], packet.payload[6]) if packet else (0, 0)

    async def set_wheel_speeds(self, left: Union[int, float], right: Union[int, float]):
        """Set motor speed in cm/s."""
        if self._disable_motors:
            return
        left = bound(int(left * 10), -self.MAX_SPEED, self.MAX_SPEED)
        right = bound(int(right * 10), -self.MAX_SPEED, self.MAX_SPEED)
        await self._backend.write_packet(Packet(1, 4, self.inc, pack('>ii', left, right)))

    async def set_left_speed(self, speed: Union[int, float]):
        """Set left motor speed in cm/s."""
        if self._disable_motors:
            return
        speed = bound(int(speed * 10), -self.MAX_SPEED, self.MAX_SPEED)
        await self._backend.write_packet(Packet(1, 6, self.inc, pack('>i', speed)))

    async def set_right_speed(self, speed: Union[int, float]):
        """Set right motor speed in cm/s."""
        if self._disable_motors:
            return
        speed = bound(int(speed * 10), -self.MAX_SPEED, self.MAX_SPEED)
        await self._backend.write_packet(Packet(1, 7, self.inc, pack('>i', speed)))

    async def move(self, distance: Union[int, float]):
        """Drive distance in centimeters."""
        if self._disable_motors:
            return
        dev, cmd, inc = 1, 8, self.inc
        packet = Packet(dev, cmd, inc, pack('>i', int(distance * 10)))
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(packet)
        packet = await completer.wait(self.DEFAULT_TIMEOUT + int(abs(distance) / 10))
        if self.USE_ROBOT_POSE and packet:
            return self.pose.set_from_packet(packet)
        else:
            self.pose.move(distance)
            return self.pose

    async def turn(self, direction: int, angle: Union[int, float]):
        """Rotate angle in degrees."""
        if self._disable_motors:
            return
        if direction == self.Dir.LEFT:
            angle = -angle

        if self.USE_ROBOT_POSE == False:
            angle *= self._turn_scale_comp
            angle += abs(angle) * self._turn_bias_comp

        dev, cmd, inc = 1, 12, self.inc
        packet = Packet(dev, cmd, inc, pack('>i', int(angle * 10)))
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(packet)
        packet = await completer.wait(self.DEFAULT_TIMEOUT + int(abs(angle) / 100))
        if self.USE_ROBOT_POSE and packet:
            return self.pose.set_from_packet(packet)
        else:
            self.pose.turn_left(-angle)
            return self.pose

    async def turn_left(self, angle: Union[int, float]):
        return await self.turn(self.Dir.LEFT, angle)

    async def turn_right(self, angle: Union[int, float]):
        return await self.turn(self.Dir.RIGHT, angle)

    async def reset_position(self): # this is the name of the command in the protocol doc
        return await self.reset_navigation()

    async def reset_navigation(self):
        """Request that robot resets position and heading."""
        if self.USE_ROBOT_POSE:
            await self._backend.write_packet(Packet(1, 15, self.inc))
        self.pose.set(0, 0, 90)

    async def get_position(self):
        """Get robot's position and heading.
        Units:
            x, y: cm
            heading: deg
        """
        if self.USE_ROBOT_POSE:
            dev, cmd, inc = 1, 16, self.inc
            completer = Completer()
            self._responses[(dev, cmd, inc)] = completer
            await self._backend.write_packet(Packet(dev, cmd, inc))
            packet = await completer.wait(self.DEFAULT_TIMEOUT)
            return self.pose.set_from_packet(packet)
        else:
            return self.pose

    async def arc(self, direction: int, angle: Union[int, float], radius: Union[int, float]):
        """Drive arc defined by angle in degrees and radius in cm."""
        if self._disable_motors:
            return
        dev, cmd, inc = 1, 27, self.inc
        if direction == Robot.Dir.LEFT:
            angle = -angle
            radius = -radius
        payload = pack('>ii', int(angle * 10), int(radius * 10))
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))

        timeout = abs(radians(angle) * (abs(radius * 10) + 51.5)) / 100
        packet = await completer.wait(15 + timeout)
        if self.USE_ROBOT_POSE and packet:
            return self.pose.set_from_packet(packet)
        else:
            return self.pose.arc(angle, radius)

    async def arc_left(self, angle: Union[int, float], radius: Union[int, float]):
        await self.arc(self.Dir.LEFT, angle, radius)

    async def arc_right(self, angle: Union[int, float], radius: Union[int, float]):
        await self.arc(self.Dir.RIGHT, angle, radius)

    async def set_lights(self, animation: int, color: Color = Color(255, 255, 255)):
        """Set robot's LEDs to animation with color red, green, blue."""
        animation = bound(animation, Robot.LightPattern.OFF, Robot.LightPattern.SPIN)
        color.red = bound(color.red, 0, 255)
        color.green = bound(color.green, 0, 255)
        color.blue = bound(color.blue, 0, 255)
        payload = bytes([animation, color.red, color.green, color.blue])
        await self._backend.write_packet(Packet(3, 2, self.inc, payload))

    async def set_lights_off(self):
        await self.set_lights(Robot.LightPattern.OFF)

    async def set_lights_rgb(self, red: int, green: int, blue: int):
        await self.set_lights(Robot.LightPattern.ON, Color(red, green, blue))

    async def set_lights_on_rgb(self, red: int, green: int, blue: int):
        await self.set_lights(Robot.LightPattern.ON, Color(red, green, blue))

    async def set_lights_blink_rgb(self, red: int, green: int, blue: int):
        await self.set_lights(Robot.LightPattern.BLINK, Color(red, green, blue))

    async def set_lights_spin_rgb(self, red: int, green: int, blue: int):
        await self.set_lights(Robot.LightPattern.SPIN, Color(red, green, blue))

    async def play_note(self, frequency: Union[float, int], duration: Union[float, int]):
        """Play note with frequency in hertz for duration in seconds."""
        dev, cmd, inc = 5, 0, self.inc
        payload = pack('>IH', abs(frequency), abs(int(duration * 1000)))
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        await completer.wait(self.DEFAULT_TIMEOUT + int(abs(duration)))

    async def play_tone(self, frequency: Union[float, int], duration: Union[float, int]):
        await self.play_note(frequency, duration)

    # async def play_sweep(
    #    self,
    #    initialFreq: Union[float, int],
    #    finalFreq: Union[float, int],
    #    duration: Union[float, int],
    #    attack: int = 10,
    #    release: int = 10,
    #    volume: int = 255,
    #    modulation_type: int = 2,
    #    modulation_rate: int = 200,
    #    append: int = 0, # TODO: Must be bool.
    #    ):
    #    """Play sweep from initialFreq to finalFreq (both in hertz), for duration (in seconds)."""
    #    dev, cmd, inc = 5, 5, self.inc
    #    payload = pack(
    #        '>IIHBBBBBB',
    #        abs(initialFreq),
    #        abs(finalFreq),
    #        abs(int(duration * 1000)),
    #        attack,
    #        release,
    #        volume,
    #        modulation_type,
    #        modulation_rate,
    #        append
    #    )
    #    completer = Completer()
    #    self._responses[(dev, cmd, inc)] = completer
    #    await self._backend.write_packet(Packet(dev, cmd, inc, payload))
    #    await completer.wait(self.DEFAULT_TIMEOUT + int(duration))

    async def say(self, phrase: str):
        """Say a phrase in robot language."""
        self.sound_enabled = True
        buf = phrase.encode('utf-8')
        for payload in [
                buf[i:i + Packet.PAYLOAD_LEN]
                for i in range(0, len(buf), Packet.PAYLOAD_LEN)
        ]:
            if self.sound_enabled:
                dev, cmd, inc = 5, 4, self.inc
                completer = Completer()
                self._responses[(dev, cmd, inc)] = completer
                await self._backend.write_packet(Packet(dev, cmd, inc, payload))
                await completer.wait(self.DEFAULT_TIMEOUT + len(payload))
                break

    def get_bumpers_cached(self):
        '''Returns list of most recently seen bumper state, or None if no event has happened yet'''
        return (self.bumpers.left, self.bumpers.right)

    async def get_bumpers(self):
        '''Returns list of most recently seen bumper state, or None if no event has happened yet.
           If there were a protocol getter, this would await that response when the cache is empty.
        '''
        return self.get_bumpers_cached()

    async def get_accelerometer(self):
        """Get instantaneous accelerometer values"""
        dev, cmd, inc = 16, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))

        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            (x,y,z) = unpack('>hhh', payload[4:10])
            return (x,y,z)
        return None

    def get_touch_sensors_cached(self):
        '''Returns list of most recently seen touch sensor state, or None if no event has happened yet'''
        return (self.touch_sensors.front_left, self.touch_sensors.front_right,
                self.touch_sensors.back_left,  self.touch_sensors.back_right)

    async def get_touch_sensors(self):
        '''Returns list of most recently seen touch sensor state, or None if no event has happened yet.
           If there were a protocol getter, this would await that response when the cache is empty.
        '''
        return self.get_touch_sensors_cached()
