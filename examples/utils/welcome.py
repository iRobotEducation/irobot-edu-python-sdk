#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())  # Will connect to the first robot found.
#robot = Create3(Bluetooth())

speed = 10.0


@event(robot.when_bumped, [True, False]) # Triggers when left bumper is depressed
async def bumped(robot):  # The name of this function can be any valid function name (the important part is the @event decorator)
    await robot.set_lights_rgb(0, 0, 255)
    await robot.set_wheel_speeds(-speed, speed)
# Alternative syntax (the @event decorator must be commented out)
# robot.when_bumped([True, False], when_bumper)


@event(robot.when_bumped, [False, True]) # Triggers when right bumper is depressed
async def bumped(robot):
    await robot.set_lights_rgb(255, 255, 0)
    await robot.set_wheel_speeds(speed, -speed)


@event(robot.when_bumped, [True, True]) # Triggers when either bumper is depressed
async def bumped(robot):
    while True:
        await robot.play_note(55, .1)
        await robot.wait(0.3)
        await robot.play_note(110, .1)
        await robot.wait(0.3)


@event(robot.when_play)
async def play(robot):
    await robot.set_lights_rgb(128, 0, 255)
    await robot.play_note(Note.A5, .5)  # Notes can be specified by frequency, or by using the Note class' constants.

robot.play()
