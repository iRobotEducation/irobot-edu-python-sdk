#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2022 iRobot Corporation. All rights reserved.
#

import asyncio
from irobot_edu_sdk.backend.backend import Backend
from irobot_edu_sdk.packet import Packet
from worker_comm import ble_write_packet, ble_disconnect, stop_program, debug_println


class Bluetooth(Backend):
    # TODO: The whole dictionary-based system, here works for devices that do not specify anything about the physical device with wich they want to connect. All this will change once the web version gets integrated into the Flutter app-
    _ble_devices = {}
    _can_write_subscribers = []

    @staticmethod
    def bluetooth_add_device(device_id):
        if not device_id in Bluetooth._ble_devices:
            Bluetooth._ble_devices[device_id] = None

    @staticmethod
    def bluetooth_data_reception(device_id, service_id, characteristic_id, data):
        # Only adds a device if it was not previously added. It's a safer (and automatic) way of dealing with devices created on the JS-side.
        if device_id in Bluetooth._ble_devices:
            device = Bluetooth._ble_devices[device_id]
            if (device != None):
                device['callback'](data)  # Data reception callback.

    # TODO: Add Multi-device support based on the ble.js functionality of registering a canWrite per device/service/characteristic key (see the Dart version).

    @staticmethod
    def bluetooth_can_write():
        for subscriber in Bluetooth._can_write_subscribers:
            can_write = getattr(subscriber, 'can_write', None)
            if callable(can_write):
                can_write()

    # TODO: Name functionality not implemented.
    # TODO: The address param from the desktop SDK may never be implemented in the web version, so document accordingly.
    def __init__(self, name: str = None):
        self.id = ''
        self.can_write_lock = asyncio.Lock()
        Bluetooth._can_write_subscribers.append(self)
        self.DEFAULT_TIMEOUT = 0.5

    async def is_connected(self) -> bool:
        # TODO.
        # print('Bluetooth.is_connected')
        return True

    async def connect(self):
        # TODO.
        # print('Bluetooth.connect')
        pass

    async def disconnect(self):
        ble_disconnect(self.id)

    def can_write(self):
        try:
            self.can_write_lock.release()
        finally:
            pass

    async def write_packet(self, packet: Packet):
        await self.can_write_lock.acquire()
        await ble_write_packet(packet.to_bytearray())
        # TODO: Evaluate if a timeout system for releasing the lock will be added.

    # Not implemented.
    # async def read_packet(self) -> Packet

    def on_data_reception(self, callback):
        for id in Bluetooth._ble_devices:
            device = Bluetooth._ble_devices[id]
            if device == None:
                Bluetooth._ble_devices[id] = {'callback': callback, 'can_write': self.can_write}  # TODO: Use constants for the keys.
                self.id = id
                break  # TODO: For now it just gets the first one that has not been assigned.

    # TODO: Evaluate if this will be here, or moved to the robot, specially for the mutlidevice system.
    def stop_program(self):
        """Extra functionality not strictly linked to Bluetooth. But, being the Bluetooth library the one that will be loaded based on the platform where the system is running (i.e., web/desktop), then this is the place to provide this function. Basically, the idea is that robots must stop the program when their stop button is pressed. On desktop native systems, that can be handled by the robot iself, but on web, the Bluetooth library is the one that communicates with the web worker.
        """
        stop_program()
