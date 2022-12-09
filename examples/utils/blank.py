#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())  # Will connect to the first robot found.
#robot = Root(Bluetooth())


@event(robot.when_play)
async def play(robot):
    print('play!')  # Put your code here!

robot.play()
