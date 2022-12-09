#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

from ..packet import Packet


class Backend:
    async def connect(self):
        """Connect to robot"""
        raise NotImplementedError()

    async def is_connected(self) -> bool:
        """Returns True if robot is connected"""
        raise NotImplementedError()

    async def disconnect(self):
        """Disconnect from robot"""
        raise NotImplementedError()

    async def write_packet(self, packet: Packet):
        """Write one packet to the robot"""
        raise NotImplementedError()

    async def read_packet(self) -> Packet:
        """Read one packet from the robot"""
        raise NotImplementedError()
