#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#


try:
    from worker_comm import stop_program
except ImportError:
    from irobot_edu_sdk.utils import stop_program

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3

robot = Create3(Bluetooth())

@event(robot.when_play)
async def play(robot):
    print("Getting the robot's IP address...")
    address = await robot.get_ipv4_address()
    if address is not None:
        print('wlan0 = ', address.wlan0)
        print('wlan1 = ', address.wlan1)
        print('usb0 = ', address.usb0)
        print()
        ip = address.wlan0
        print("Hold Cmd or Ctrl and click on the IP address to open Create's web page:")
        print('http://' + str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3]))
        print()
    else:
        print('No IP address')
    stop_program()

robot.play()
