#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

"""
This is a USB class that implements the Backend interface methods.

It is only compatible with a MicroPython board.
"""

from uasyncio import sleep
from binascii import hexlify, unhexlify
from pyb import USB_VCP
from .backend import Backend
from ..packet import Packet


class USB(Backend):
    def __init__(self):
        self._usb = USB_VCP()
        self._usb.init()
        self._usb.setinterrupt(-1)

    async def connect(self):
        await sleep(1)  # pyboard needs a moment to wait for USB
        while not self.is_connected():
            await sleep(0)

    async def is_connected(self) -> bool:
        return self._usb.isconnected()

    async def disconnect(self):
        self._usb.close()

    async def read_packet(self) -> Packet:
        string = b''
        while not (string.endswith(b'\n') and len(string) > 40):
            await sleep(0)
            while not self._usb.any():
                await sleep(0)
            string += self._usb.read(1)
        return Packet.from_bytes(unhexlify(string[-41:-1]))

    async def write_packet(self, packet: Packet):
        string = hexlify(packet.to_bytes()) + b'\n'
        self._usb.write(string)
