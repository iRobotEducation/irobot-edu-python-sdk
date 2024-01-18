#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2024 iRobot Corporation. All rights reserved.
#

"""
The Console class implements the Backend interface methods using the console, treating stdin/stdout as a robot.

At first glance, this seems pretty useless, but the intent is for use with a microprocessor board running
a variant of Python for microcontrollers where you want to communicate over the port which usually allows
access to the REPL.
"""

import sys, select
from asyncio import sleep
from binascii import hexlify, unhexlify
from .backend import Backend
from ..packet import Packet

class Console(Backend):
    def __init__(self):
        self.spoll = select.poll()
        self.spoll.register(sys.stdin, select.POLLIN)

    async def connect(self):
        print('connect')
        pass
        #await sleep(1)
        #while not self.is_connected():
        #    await sleep(0)

    async def is_connected(self) -> bool:
        return True
        #return self._usb.isconnected()

    async def disconnect(self):
        print('disconnect')
        pass
        #self._usb.close()

    async def read_packet(self) -> Packet:
        string = ''
        while not (string.endswith(b'\n') and len(string) >= 40):
            await sleep(0)
            while not self.spoll.poll(0):
                await sleep(0)
            string += sys.stdin.read(1)
        return Packet.from_bytes(unhexlify(string[-41:-1]))

    async def write_packet(self, packet: Packet):
        print(hexlify(packet.to_bytes()).decode())
