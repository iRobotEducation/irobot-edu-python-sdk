#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

import math
from typing import Union
from struct import pack, unpack
from .backend.backend import Backend
from .completer import Completer
from .packet import Packet
from .utils import bound
from .getter_types import IPv4Addresses, IrProximity, Pose
from irobot_edu_sdk.robot import Robot


class Create3(Robot):
    """Create 3 robot object."""

    DOCK_STATUS_SUCCEEDED = 0
    DOCK_STATUS_ABORTED   = 1
    DOCK_STATUS_CANCELED  = 2
    DOCK_RESULT_UNDOCKED = 0
    DOCK_RESULT_DOCKED   = 1

    def __init__(self, backend: Backend):
        super().__init__(backend=backend)

        # Getters.
        self.ipv4_address = IPv4Addresses()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

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

    async def get_ir_proximity(self):
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

    async def get_position(self):
        dev, cmd, inc = 1, 16, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(self.DEFAULT_TIMEOUT)
        if packet:
            payload = packet.payload
            timestamp = unpack('>I', payload[0:4])[0]
            x = unpack('>i', payload[4:8])[0]
            y = unpack('>i', payload[8:12])[0]
            heading = unpack('>h', payload[12:14])[0] / 10
            return Pose(x, y, heading)
        return None

    async def reset_navigation(self):
        await self._backend.write_packet(Packet(1, 15, self.inc))

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
        await completer.wait(timeout)

    async def dock(self):
        """Request a docking action."""
        dev, cmd, inc = 1, 19, self.inc
        completer = Completer()
        self._responses[(dev, cmd, inc)] = completer
        await self._backend.write_packet(Packet(dev, cmd, inc))
        packet = await completer.wait(60)
        if packet:
            unpacked = unpack('>IBBHHHHH', packet.payload)
            return {'timestamp': unpacked[0], 'status': unpacked[1], 'result': unpacked[2]}
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
            return {'timestamp': unpacked[0], 'status': unpacked[1], 'result': unpacked[2]}
        return None

    async def get_docking_values(self):
        """Get docking values."""
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
