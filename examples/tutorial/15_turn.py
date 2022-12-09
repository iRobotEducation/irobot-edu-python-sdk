#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Let's move the robot!

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def play(robot):
    await robot.turn_left(90)
    await robot.turn_right(90)

    # Same result as the previous 2 commands.
    await robot.turn_left(90)
    await robot.turn_left(-90)

robot.play()
