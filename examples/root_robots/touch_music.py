#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())

duration = 0.15


@event(robot.when_touched, [True, False,
                            False, False])
async def touched(robot):
    await robot.set_lights_rgb(255, 0, 0)
    await robot.play_note(Note.A4, duration)


@event(robot.when_touched, [False, True,
                            False, False])
async def touched(robot):
    await robot.set_lights_rgb(0, 255, 0)
    await robot.play_note(Note.C5_SHARP, duration)


@event(robot.when_touched, [False, False,
                            True, False])
async def touched(robot):
    await robot.set_lights_rgb(0, 0, 255)
    await robot.play_note(Note.E5, duration)


@event(robot.when_touched, [False, False,
                            False, True])
async def touched(robot):
    await robot.set_lights_rgb(255, 255, 255)
    await robot.play_note(Note.A5, duration)


@event(robot.when_touched, [True, True,
                            True, True])
async def touched(robot):
    print('ANY sensor touched')


@event(robot.when_play)
async def play(robot):
    await robot.say("Hello!")

robot.play()
