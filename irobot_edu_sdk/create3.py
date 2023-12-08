#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

import math
from enum import IntEnum, IntFlag
from typing import Union, Callable, Awaitable, List
from struct import pack, unpack
from .backend.backend import Backend
from .event import Event
from .completer import Completer
from .packet import Packet
from .utils import bound
from .getter_types import IPv4Addresses, IrProximity, Pose, DockingSensor
from .robot import Robot


class Create3(Robot):
    """Create 3 robot object."""

    class DockStatus(IntEnum):
        SUCCEEDED = 0
        ABORTED   = 1
        CANCELED  = 2

    class DockResult(IntEnum):
        UNDOCKED = 0
        DOCKED   = 1


    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        self._events[(19, 0)] = self._when_docking_sensor_handler

        self._when_docking_sensor: list[Event] = []

        # Getters.
        self.ipv4_address = IPv4Addresses()
        self.docking_sensor = DockingSensor()

        # Use Create 3 robot's internal position estimate
        self.USE_ROBOT_POSE = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # Event Handlers.

    async def _when_docking_sensor_handler(self, packet):
        if len(packet.payload) > 4:
            self.docking_sensor.contacts = packet.payload[4] != 0
            self.docking_sensor.sensors = (packet.payload[5],
                                           packet.payload[6],
                                           packet.payload[7])

            for event in self._when_docking_sensor:
                # TODO: Generate triggers instead of just firing for any event
                # TODO: Define dock sensor Enum
                await event.run(self)

    # Event Callbacks.

    def when_docking_sensor(self, callback: Callable[[bool], Awaitable[None]]):
        self._when_docking_sensor.append(Event(True, callback))

    # Commands.

    async def get_ipv4_address(self) -> IPv4Addresses:
        """Get the robot's ipv4 address as a IPv4Addresses, which contains wlan0, wlan1 and usb0. Returns None if anything went wrong."""
        dev, cmd, inc = 100, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            self.ipv4_address.wlan0 = [packet.payload[0], packet.payload[1], packet.payload[2], packet.payload[3]]
            self.ipv4_address.wlan1 = [packet.payload[4], packet.payload[5], packet.payload[6], packet.payload[7]]
            self.ipv4_address.usb0 = [packet.payload[8], packet.payload[9], packet.payload[10], packet.payload[11]]
            return self.ipv4_address
        return None

    async def get_6x_ir_proximity(self):
        """Get Original IR Proximity Values and States"""
        dev, cmd, inc = 11, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IHHHHHH', packet.payload)
            ir_proximity = IrProximity()
            ir_proximity.sensors = list(unpacked[1:])
            return ir_proximity
        return None

    async def get_packed_ir_proximity(self):
        """DEPRECATED function for new Get IR Proximity Values and States"""
        print('Warning: get_packed_ir_proximity() has been deprecated, please use get_ir_proximity() instead')
        await self.get_7x_ir_proximity()

    async def get_7x_ir_proximity(self):
        """Get Packed IR Proximity Values and States"""
        dev, cmd, inc = 11, 2, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            ir_proximity = IrProximity()
            #ir_proximity.state = payload[4]
            ir_proximity.sensors = [
                (payload[ 5] << 4) + (payload[12] >> 4),
                (payload[ 6] << 4) + (payload[12] & 0xF),
                (payload[ 7] << 4) + (payload[13] >> 4),
                (payload[ 8] << 4) + (payload[13] & 0xF),
                (payload[ 9] << 4) + (payload[14] >> 4),
                (payload[10] << 4) + (payload[14] & 0xF),
                (payload[11] << 4) + (payload[15] >> 4),
            ]
            return ir_proximity
        return None

    async def get_ir_proximity(self):
        """Version-Agnostic Get IR Proximity Values and States"""
        ir_prox = await self.get_7x_ir_proximity()
        if ir_prox is not None:
            return ir_prox

        ir_prox = await self.get_6x_ir_proximity()
        if ir_prox is not None:
            print('Warning: ir_prox() missing seventh value; you may need to update your robot')
            ir_prox.sensors.append(float('nan'))
            return ir_prox

        return None

    async def navigate_to(self, x: Union[int, float], y: Union[int, float], heading: Union[int, float] = None):
        """ If heading is None, then it will be ignored, and the robot will arrive to its destination
        pointing towards the direction of the line between the destination and the origin points.
        Units:
            x, y: cm
            heading: deg
        """

        if self._disable_motors:
            return
        dev, cmd, inc = 1, 17, self.inc
        _heading = -1
        if heading is not None:
            _heading = int(heading * 10)
            _heading = bound(_heading, 0, 3599)
        payload = pack('>iih', int(x * 10), int(y * 10), _heading)
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc, payload))
        timeout = self.DEFAULT_TIMEOUT + int(math.sqrt(x * x + y * y) / 10) + 4  # 4 is the timeout for a potential rotation.
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if self.USE_ROBOT_POSE and packet:
            return self.pose.set_from_packet(packet)
        else:
            if heading is not None:
                self.pose.set(x, y, heading)
            else:
                self.pose.set(x, y, math.degrees(math.atan2(y - self.pose.y, x - self.pose.x)) + self.pose.heading)

            return self.pose

    async def dock(self):
        """Request a docking action."""
        dev, cmd, inc = 1, 19, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(60)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': self.DockStatus(unpacked[1]), 'result': self.DockResult(unpacked[2])}
        return None

    async def undock(self):
        """Request an undocking action."""
        dev, cmd, inc = 1, 20, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(30)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': self.DockStatus(unpacked[1]), 'result': self.DockResult(unpacked[2])}
        return None

    async def get_docking_values(self):
        """Get docking values."""
        # TODO: Harmonize access with cached value from events
        dev, cmd, inc = 19, 1, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            unpacked = unpack('>IBBBBHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'contacts': unpacked[1], 'IR sensor 0': unpacked[2],
                    'IR sensor 1': unpacked[3], 'IR sensor 2': unpacked[4]}
        return None

    async def get_version_string(self) -> str:
        """Get version as a human-readable string."""
        ver = await self.get_versions(0xA5)
        try:
            major = ver[1]
            minor = ver[2]
            patch = ver[9]
            if major < 32 or major > 126:
                major = str(major)
            else:
                major = chr(major)

            return '.'.join([major, str(minor), str(patch)])
        except IndexError:
            return None
