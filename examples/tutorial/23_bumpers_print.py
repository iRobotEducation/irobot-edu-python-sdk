#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# An event triggered by the robot's sensors, such as its bumpers, can also run multiple tasks.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_bumped, [True, False])
async def bumped(robot):
    print('LEFT')


@event(robot.when_bumped, [False, True])
async def bumped(robot):
    print('RIGHT')


@event(robot.when_bumped, [])  # An empty list means that if ANY of the bumpers detect a collition, this task will be triggered.
async def bumped(robot):
    print('ANY')


@event(robot.when_play)
async def play(robot):
    print("Try clicking on the robot's bumpers")

robot.play()
