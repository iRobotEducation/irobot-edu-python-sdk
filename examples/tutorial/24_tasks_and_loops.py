#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# The tasks triggerd by robot.play() can contain loops, even infinite ones.
# This example will allow you to experiment with "competing" loops that run in parallel.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def play(robot):
    x = 0
    while True:
        x += 1
        print('x = ', x)
        # When a task has a loop that doesn't call any other async function using await, it may be very demanding for the computer's CPU.
        # So, if it will not be calling any robot method (which are called with await), it must include a call to hand_over inside the loop:
        await hand_over()


@event(robot.when_play)
async def play(robot):
    y = 1000
    while True:
        y += 1
        print('y = ', y)
        await hand_over()

# This will trigger all the functions decoreated with the @event(robot.when_play).
robot.play()
