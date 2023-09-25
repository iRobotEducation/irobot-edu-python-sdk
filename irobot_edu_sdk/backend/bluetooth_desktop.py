#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

"""
This is a Bluetooth Low Energy class that implements the Backend interface methods.

It is compatible with CPython on macOS, Windows, and Linux using the Bleak library.
"""

from asyncio import sleep, Lock
from queue import SimpleQueue
from typing import Optional
from bleak import BleakClient, BleakScanner
from .backend import Backend
from ..packet import Packet


class Bluetooth(Backend):
    ROOT_ID_SERVICE = "48c5d828-ac2a-442d-97a3-0c9822b04979"
    UART_SERVICE = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    TX_CHARACTERISTIC = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    RX_CHARACTERISTIC = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, name: str = None, address: Optional[str] = None):
        """If no name is provided, connects to the first device found."""
        self._name = name
        self._address = address
        self._device = None
        self._client: Optional[BleakClient] = None
        self._queue: SimpleQueue = SimpleQueue()
        self._txlock = Lock()

    def rx_handler(self, characteristic, data):
        self._queue.put(Packet.from_bytes(bytes(data)))

    async def connect(self):
        """This method does not exit until a robot is found"""

        while not self._address:
            if self._name is not None: # If a name is given, try to connect to that
                device = await BleakScanner.find_device_by_name(self._name)
                if device:
                    self._address = device.address
                    self._device = device
            else: # If no name is given, connect to first device with Root ID service
                discovered = await BleakScanner.discover(service_uuids=[self.ROOT_ID_SERVICE, self.UART_SERVICE], return_adv=True)
                for device, adv_data in discovered.values():
                    if self.ROOT_ID_SERVICE in adv_data.service_uuids:
                        if self._name is None or self._name == device.name:
                            self._address = device.address
                            self._device = device
                            break
        if self._device:
            print(f'Connecting to {device.name} ({device.address})')
            self._client = BleakClient(self._device)
        else:
            print(f'Connecting to {self._address}')
            self._client = BleakClient(self._address)

        if await self._client.connect():
            await self._client.start_notify(self.RX_CHARACTERISTIC, self.rx_handler)

    async def is_connected(self) -> bool:
        return self._client.is_connected if self._client else False

    async def disconnect(self):
        if await self.is_connected():
            await self._client.disconnect()
        self._client = None

    async def read_packet(self) -> Packet:
        while self._queue.empty():
            await sleep(0)
        return self._queue.get()

    async def write_packet(self, packet: Packet):
        if self._client:
            async with self._txlock:
                await self._client.write_gatt_char(self.TX_CHARACTERISTIC, packet.to_bytearray(), True)
