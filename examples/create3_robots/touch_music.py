#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())

duration = 0.15


@event(robot.when_touched, [True, False])  # (.) button.
async def touched(robot):
    await robot.set_lights_on_rgb(255, 0, 0)
    await robot.play_note(Note.A4, duration)


@event(robot.when_touched, [False, True])  # (..) button.
async def touched(robot):
    await robot.set_lights_on_rgb(0, 255, 0)
    await robot.play_note(Note.C5_SHARP, duration)


@event(robot.when_touched, [True, True])
async def touched(robot):
    print('ANY sensor touched')


@event(robot.when_play)
async def play(robot):
    await robot.play_note(Note.A5, duration)

robot.play()
