#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Let's explore how parallel tasks can be used in our programs.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())

# Any event (in this case we are using the robot.when_play event) can trigger multiple tasks that will run in parallel.


@event(robot.when_play)
async def play(robot):  # Remember the "async" keyword for events.
    print('play 1')


@event(robot.when_play)
async def play(robot):
    print('play 2')


@event(robot.when_play)
async def play(robot):  # Note that these decorated event functions, can all have the same name.
    print('play 3')


@event(robot.when_play)
async def p4(robot):  # Or they can have a different name too.
    print('play 4')

# This will trigger all the async functions decoreated with the @event(robot.when_play).
robot.play()
