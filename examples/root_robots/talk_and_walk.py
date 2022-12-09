#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

backend = Bluetooth()
robot = Root(backend)


@event(robot.when_play)
async def walk(robot):
    while True:
        print('walk')
        await robot.move(6)
        await robot.move(-6)


@event(robot.when_bumped, [])
async def talk(robot):
    while True:
        print('talk')
        await robot.say("It's a beautiful day in the neighborhood")


robot.play()
