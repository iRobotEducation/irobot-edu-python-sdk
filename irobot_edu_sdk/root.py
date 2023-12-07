#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

import math
from enum import IntEnum
from typing import Union, Callable, Awaitable, List
from struct import pack, unpack
from .backend.backend import Backend
from .event import Event
from .completer import Completer
from .packet import Packet
from .utils import bound
from .robot import Robot
from .getter_types import Pose, Movement, ColorSensor, LightSensors


class Root(Robot):
    """Root robot object"""

    # Marker/eraser.
    class MarkerPos(IntEnum):
        UP = 0
        DOWN = 1
        ERASE = 2

    # Light sensor.
    class LightEvent(IntEnum):
        UNKNOWN = 0
        DARKER = 4
        RIGHT_BRIGHTER_THAN_LEFT = 5
        LEFT_BRIGHTER_THAN_RIGHT = 6
        BRIGHTER = 7

    # Gravity compensation.
    class GravityComp(IntEnum):
        OFF = 0
        ON = 1
        WHEN_MARKER = 2

    # Color sensor.
    class ColorLighting(IntEnum):
        OFF = 0
        RED = 1
        GREEN = 2
        BLUE = 3
        ALL = 4

    class ColorFormat(IntEnum):
        ADC_COUNTS = 0
        MILLIVOLTS = 1

    class ColorBank(IntEnum):
        BANK_0_TO_7 = 0
        BANK_8_TO_15 = 1
        BANK_16_TO_23 = 2
        BANK_24_TO_31 = 3

    class ColorID(IntEnum):
        # Note: the Root robot color sensor uses an HSI color space.
        # Precedence is given to detemining WHITE, BLACK, LOW_INT(ENSITY), and LOW_SAT(URATION), at which point hue is determined.
        # The hues are defined in the following color wheel order:
        # RED, ORANGE, YELLOW, LIME, GREEN, CYAN, BLUE, VIOLET, MAGENTA, CERISE
        SKIP = -1
        IGNORE = -1
        WHITE = 0
        BLACK = 1
        RED = 2
        GREEN = 3
        BLUE = 4
        # colors below are not supported
        ORANGE = 5
        RED_YELLOW = 5
        YELLOW_RED = 5
        YELLOW = 6
        MAGENTA = 7
        LIME = 8
        YELLOW_GREEN = 8
        GREEN_YELLOW = 8
        CYAN = 9
        GREEN_BLUE = 9
        BLUE_GREEN = 9
        VIOLET = 10
        BLUE_MAGENTA = 10
        MAGENTA_BLUE = 10
        CERISE = 11
        MAGENTA_RED = 11
        RED_MAGENTA = 11
        LOW_INT = 13
        LOW_INTENSITY = 13
        LOW_SAT = 14
        LOW_SATURATION = 14

    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        self._events[(4, 2)] = self._when_color_scanned_handler
        self._events[(13, 0)] = self._when_light_seen_handler

        self._when_color_scanned: list[Event] = []
        self._when_light_seen: list[Event] = []

        # Getters.
        self.color_sensor = ColorSensor()
        self.light_sensors = LightSensors()

        # Use Root robot's internal position estimate #TODO change based on version
        self.USE_ROBOT_POSE = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # Event Handlers.

    async def _when_color_scanned_handler(self, packet: Packet):
        self.color_sensor.colors = [Root.ColorID(c >> i & 0xF) for c in packet.payload for i in range(4, -1, -4)]

        for event in self._when_color_scanned:
            # Trigger matching events based on parsed colors
            if self.color_sensor.matches(event.condition) or event.condition.colors == []:
                await event.run(self)

    async def _when_light_seen_handler(self, packet: Packet):
        self.light_sensors.state = packet.payload[4]
        self.light_sensors.left = unpack(">H", packet.payload[5:7])[0]
        self.light_sensors.right = unpack(">H", packet.payload[7:9])[0]

        for event in self._when_light_seen:
            if len(event.condition) == 1:
                if event.condition[0] == self.light_sensors.state:
                    await event.run(self)

    # Event Callbacks.

    def when_color_scanned(self, condition: list[List[int]], callback: Callable[[ColorSensor], Awaitable[None]]):
        """Register when color callback of type async def fn(colors:
        List[Color])"""
        self._when_color_scanned.append(Event(ColorSensor(condition), callback))

    def when_light_seen(self, condition: list[int, int, int], callback: Callable[[LightSensors], Awaitable[None]]):
        """Register when light callback of type: async def fn(state: Light, left_mV: int, right_mV: int)"""
        self._when_light_seen.append(Event(condition, callback))

    # Commands.

    async def stop(self):
        await self.reset_navigation()
        await super().stop()

    async def move(self, distance: Union[int, float]):
        await super().move(distance)

    async def turn_right(self, angle: Union[int, float]):
        await super().turn_right(angle)

    async def set_marker(self, position: int):
        """Set marker to position of type Marker"""
        if self._disable_motors:
            return
        dev, cmd, inc = 2, 0, self.inc
        payload = bytes([bound(position, self.MarkerPos.UP, self.MarkerPos.ERASE)])
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        await completer.wait(self.DEFAULT_TIMEOUT)

    async def set_marker_up(self):
        await self.set_marker(self.MarkerPos.UP)

    async def set_marker_down(self):
        await self.set_marker(self.MarkerPos.DOWN)

    async def set_eraser_down(self):
        await self.set_marker(self.MarkerPos.ERASE)

    async def set_marker_and_eraser_up(self):
        await self.set_marker(self.MarkerPos.UP)

    async def set_eraser_up(self):
        await self.set_marker(self.MarkerPos.UP)

    async def set_gravity_compensation(self, gravity: int, amount: Union[int, float]):
        """Set vertical driving compensation for gravity and amount between 0% and 100%"""
        gravity = bound(gravity, Root.GravityComp.OFF, Root.GravityComp.WHEN_MARKER)
        amount = bound(int(amount * 10), 0, 1000)
        await self._backend.write_packet(Packet(1, 13, self.inc, pack(">BH", gravity, amount)))

    async def compute_movement_to(self, x, y):
        await self.get_position()
        dx = x - self.pose.x
        dy = y - self.pose.y
        return Movement(math.sqrt(dx * dx + dy * dy), math.degrees(math.atan2(dy, dx)) - self.pose.heading)

    async def navigate_to(self, x: Union[int, float], y: Union[int, float], heading: Union[int, float] = None):
        """ If heading is None, then it will be ignored, and the robot will arrive to its destination
        pointing towards the direction of the line between the destination and the origin points."""
        movement = await self.compute_movement_to(x, y)
        await self.turn_left(Movement.minimize_angle(movement.angle))
        await self.move(movement.distance)
        if heading is not None:
            await self.get_position()
            await self.turn_left(Movement.minimize_angle(heading - self.pose.heading))

    async def get_version_string(self) -> str:
        """Get version as a human-readable string."""
        main = await self.get_versions(0xA5)
        color = await self.get_versions(0xC6)
        try:
            return f'Main: {str(main[1])}.{str(main[2])}\tColor: {str(color[1])}.{str(color[2])}'
        except IndexError:
            try:
                return f'Main: {str(main[1])}.{str(main[2])}'
            except IndexError:
                return None;

    async def get_light_values(self):
        """Get instantaneous ambient light sensor values"""
        dev, cmd, inc = 13, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))

        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            (l, r) = unpack('>HH', payload[4:8])
            return (l / 1000, r / 1000) # normalize between 0 and 1
        return None

    async def get_color_section(self, bank: ColorBank, lighting: ColorLighting, data_format: ColorFormat):
        """Returns tuple with color sensor data from one bank of 8 sensors"""
        dev, cmd, inc = 4, 1, self.inc
        bank = bound(bank, Root.ColorBank.BANK_0_TO_7, Root.ColorBank.BANK_24_TO_31)
        lighting = bound(lighting, Root.ColorLighting.OFF, Root.ColorLighting.ALL)
        data_format = bound(data_format, Root.ColorFormat.ADC_COUNTS, Root.ColorFormat.MILLIVOLTS)
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, pack(">BBB", bank, lighting, data_format)))

        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            values = unpack('>HHHHHHHH', payload[0:16])
            return values
        else:
            return None

    async def get_color_values(self, lighting: ColorLighting, data_format: ColorFormat):
        '''Returns tuple with color sensor data from left to right for a given lighting condition'''
        values = []
        for bank in Root.ColorBank:
            section = await self.get_color_section(bank, lighting, data_format)
            if section:
                values += list(section)
            else:
                return None
        return tuple(values)

    def get_color_ids_cached(self):
        '''Returns list of most recently seen color sensor IDs, or None if no event has happened yet'''
        return tuple(self.color_sensor.colors) if self.color_sensor.colors != [] else None

    async def get_color_ids(self):
        '''Returns list of most recently seen color sensor IDs, or None if no event has happened yet.
           If there were a protocol getter, this would await that response when the cache is empty.
        '''
        return self.get_color_ids_cached()
