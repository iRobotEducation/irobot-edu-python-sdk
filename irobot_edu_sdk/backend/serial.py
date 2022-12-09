#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020 iRobot Corporation. All rights reserved.
#

"""
This is a USB Serial class that implements the Backend interface methods.

It is compatible with CPython using pySerial and the MicroPython Unix port using micropython-serial.
"""

try:
    from asyncio import sleep
except ImportError:
    from uasyncio import sleep

from binascii import hexlify, unhexlify
from serial import Serial as _Serial
from .backend import Backend
from ..packet import Packet


class Serial(Backend):
    def __init__(self, port: str):
        self._serial = _Serial(port, 115200)

    async def connect(self):
        self._serial.open()

    async def is_connected(self) -> bool:
        try:
            return self._serial.isOpen()
        except AttributeError:
            return True  # no isOpen() for micropython

    async def disconnect(self):
        self._serial.close()

    async def read_packet(self) -> Packet:
        string = b''
        while not (string.endswith(b'\n') and len(string) > 40):
            await sleep(0)
            while not self._serial.inWaiting():
                await sleep(0)
            string += self._serial.read(1)
        return Packet.from_bytes(unhexlify(string[-41:-1]))

    async def write_packet(self, packet: Packet):
        string = hexlify(packet.to_bytes()) + b'\n'
        self._serial.write(string)
