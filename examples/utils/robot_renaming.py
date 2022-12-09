#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021 iRobot Corporation. All rights reserved.
#

try:
    from worker_comm import stop_program
except ImportError:
    from irobot_edu_sdk.utils import stop_program

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3

# No need to change this line if using a Root robot.
robot = Create3(Bluetooth())

# Change this string by the robot's new name.
new_name = 'MyRobot'


@event(robot.when_play)
async def play(robot):
    old_name = await robot.get_name()
    await robot.set_name(new_name)
    print('Renamed:', old_name, '->', new_name)
    stop_program()

robot.play()
