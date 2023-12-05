#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

try:
    from typing import Optional
except ImportError:
    pass
from struct import pack
import binascii


class Packet():
    """robot packet type"""
    PACKET_LEN = 20
    PAYLOAD_LEN = 16

    def __init__(self,
                 dev: int,
                 cmd: int,
                 inc: int,
                 payload: bytes = bytes(PAYLOAD_LEN),
                 crc: Optional[int] = None,
                 force_crc: bool = False):
        self.dev = dev
        self.cmd = cmd
        self.inc = inc
        assert len(payload) <= self.PAYLOAD_LEN, "invalid payload length"
        self.payload = payload + bytes(self.PAYLOAD_LEN - len(payload))
        self._crc = crc if force_crc is False else self.calc_crc()

    @classmethod
    def from_bytes(cls, raw: bytes):
        """create a new packet instance from raw bytes"""
        assert len(raw) == cls.PACKET_LEN, "invalid packet length"
        return Packet(raw[0], raw[1], raw[2], payload=raw[3:19], crc=raw[19])

    def to_bytes(self):
        """20 byte packet with crc"""
        return self.packet() + bytes([self.calc_crc()])

    def to_bytearray(self):
        """mutable 20 byte array with crc"""
        return bytearray(self.to_bytes())

    def packet(self):
        """19 byte packet without crc"""
        return pack("3B", self.dev, self.cmd, self.inc) + self.payload

    def check_crc(self):
        """check if computed crc matches stored crc"""
        return False if self._crc is None else self._crc == self.calc_crc()

    def calc_crc(self) -> int:
        """calculates crc for packet"""
        crc = 0x00
        for c in self.packet():
            for i in range(8):
                b = crc & 0x80
                if c & (0x80 >> i):
                    b ^= 0x80
                crc <<= 1
                if b:
                    crc ^= 0x07
            crc &= 0xFF
        return crc

    def __str__(self):
        return f"Packet [{self.dev:3}, {self.cmd:3}, {self.inc:3}]: " + binascii.hexlify(self.payload).decode('ascii')

    @property
    def crc(self) -> int:
        """return stored crc or calculate new crc"""
        return self._crc if self._crc is not None else self.calc_crc()
