#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

import math
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
    """Create 3 robot object"""

    # Marker/eraser.
    MARKER_UP = 0
    MARKER_DOWN = 1
    MARKER_ERASE = 2

    # Light sensor.
    LIGHT_UNKNOWN = 0
    LIGHT_DARK = 4
    LIGHT_RIGHT_BRIGHTER_THAN_LEFT = 5
    LIGHT_LEFT_BRIGHTER_THAN_RIGHT = 6
    LIGHT_BRIGHT = 7

    # Gravity compensation.
    GRAVITY_OFF = 0
    GRAVITY_ON = 1
    GRAVITY_WHEN_MARKER = 2

    # Color sensor.
    COLOR_LIGHTING_OFF = 0
    COLOR_LIGHTING_RED = 1
    COLOR_LIGHTING_GREEN = 2
    COLOR_LIGHTING_BLUE = 3
    COLOR_LIGHTING_ALL = 4

    COLOR_FORMAT_ADC_COUNTS = 0
    COLOR_FORMAT_MILLIVOLTS = 1

    COLOR_SENSORS_0_TO_7 = 0
    COLOR_SENSORS_8_TO_15 = 1
    COLOR_SENSORS_16_TO_23 = 2
    COLOR_SENSORS_24_TO_31 = 3

    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        self._events[(4, 2)] = self._when_color_scanned_handler
        self._events[(13, 0)] = self._when_light_seen_handler

        self._when_color_scanned: list[Event] = []
        self._when_light_seen: list[Event] = []

        # Getters.
        self.color_sensor = ColorSensor()
        self.light_sensors = LightSensors()

        self.pose = Pose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # Event Handlers.

    async def _when_color_scanned_handler(self, packet: Packet):
        for event in self._when_color_scanned:
            self.color_sensor.colors = [c >> i & 0xF for c in packet.payload for i in range(4, -1, -4)]
            # TODO: Add trigger.
            await event.run(self)

    # TODO: Test.
    async def _when_light_seen_handler(self, packet: Packet):
        for event in self._when_light_seen:
            self.light_sensors.state = packet.payload[4]
            self.light_sensors.left = unpack(">H", packet.payload[5:7])[0]
            self.light_sensors.right = unpack(">H", packet.payload[7:9])[0]
            # TODO: Add trigger
            await event.run(self)

    # Event Callbacks.

    def when_color_scanned(self, condition: list[List[int]], callback: Callable[[ColorSensor], Awaitable[None]]):
        """Register when color callback of type async def fn(colors:
        List[Color])"""
        self._when_color_scanned.append(Event(condition, callback))

    def when_light_seen(self, condition: list[int, int, int], callback: Callable[[LightSensors], Awaitable[None]]):
        """Register when light callback of type: async def fn(state: Light, left_mV: int, right_mV: int)"""
        self._when_light_seen.append(Event(condition, callback))

    # Commands.

    async def stop(self):
        await self.reset_navigation()
        await super().stop()

    async def move(self, distance: Union[int, float]):
        await super().move(distance)
        self.pose.move(distance)

    async def turn_right(self, angle: Union[int, float]):
        await super().turn_right(angle)
        self.pose.turn_left(-angle)

    async def set_marker(self, position: int):
        """Set marker to position of type Marker"""
        if self._disable_motors:
            return
        dev, cmd, inc = 2, 0, self.inc
        payload = bytes([bound(position, Root.MARKER_UP, Root.MARKER_ERASE)])
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        await completer.wait(self.DEFAULT_TIMEOUT)

    async def set_gravity_compensation(self, gravity: int, amount: Union[int, float]):
        """Set vertical driving compensation for gravity and amount between 0% and 300%"""
        gravity = bound(gravity, Root.GRAVITY_OFF, Root.GRAVITY_WHEN_MARKER)
        amount = bound(int(amount * 10), 0, 3000)
        await self._backend.write_packet(Packet(1, 13, self.inc, pack(">BH", gravity, amount)))

    # It is async since this command will be implemented in the robot's firmware.
    async def get_position(self):
        return self.pose

    async def reset_navigation(self):
        self.pose.x = 0
        self.pose.y = 0
        self.pose.heading = 90

    def compute_movement_to(self, x, y):
        dx = x - self.pose.x
        dy = y - self.pose.y
        return Movement(math.sqrt(dx * dx + dy * dy), math.degrees(math.atan2(dy, dx)) - self.pose.heading)

    # TODO: Finish implementation.
    async def navigate_to(self, x: Union[int, float], y: Union[int, float], heading: Union[int, float] = None):
        """ If heading is None, then it will be ignored, and the robot will arrive to its destination
        pointing towards the direction of the line between the destination and the origin points."""
        movement = self.compute_movement_to(x, y)
        await self.turn_left(Movement.minimize_angle(movement.angle))
        await self.move(movement.distance)
        if heading is not None:
            # TODO: test.
            await self.turn_left(Movement.minimize_angle(heading - self.heading))
