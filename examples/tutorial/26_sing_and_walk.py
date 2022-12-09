#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# More robot parallel tasks!

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

backend = Bluetooth()
robot = Root(backend)
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def walk(robot):
    while True:
        print('walk')
        await robot.move(6)
        await robot.move(-6)


@event(robot.when_play)
async def sing(robot):
    notes = [
        (Note.E4, Note.QUARTER),
        (Note.F4_SHARP, Note.QUARTER),

        (Note.G4, Note.HALF),
        (Note.F4_SHARP, Note.QUARTER),
        (Note.E4, Note.QUARTER),
        (Note.D4_SHARP, Note.HALF),
        (Note.E4, Note.QUARTER),
        (Note.F4_SHARP, Note.QUARTER),

        (Note.B3, Note.HALF),
        (Note.C4_SHARP, Note.QUARTER),
        (Note.D4_SHARP, Note.QUARTER),
        (Note.E4, Note.HALF),
        (Note.D4, Note.QUARTER),
        (Note.C4, Note.QUARTER),

        (Note.B3, Note.HALF),
        (Note.A3, Note.QUARTER),
        (Note.G3, Note.QUARTER),
        (Note.F3_SHARP, Note.WHOLE),

        (Note.G3, Note.QUARTER),
        (Note.G3, Note.WHOLE),
    ]
    while True:
        for note in notes:
            await robot.play_note(note[0], note[1])


robot.play()
