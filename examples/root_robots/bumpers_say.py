#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())


@event(robot.when_bumped, [True, False])
async def bumped(robot):
    await robot.say("Hello!")


@event(robot.when_bumped, [False, True])
async def bumped(robot):
    await robot.say("Bye!")


@event(robot.when_bumped, [True, True])
async def bumped(robot):
    print('ANY')

robot.play()
