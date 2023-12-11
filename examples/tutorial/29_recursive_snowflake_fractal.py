#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Want to draw something more complex?
# What about also learning a bit about recursion?

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


async def fractal(level, size):
    if level < 1:
        await robot.move(size)
    else:
        # Calling a function from within itself is called recursion.
        await fractal(level - 1, size/3)
        await robot.turn_left(60)
        await fractal(level - 1, size/3)
        await robot.turn_left(-120)
        await fractal(level - 1, size/3)
        await robot.turn_left(60)
        await fractal(level - 1, size/3)


@event(robot.when_play)
async def play(robot):
    await robot.set_lights_spin_rgb(0, 0, 255)
    await robot.set_marker_down()  # Will have no effect on Create 3.

    for _ in range(3):
        await fractal(3, 40)
        await robot.turn_left(-120)

    await robot.set_marker_and_eraser_up()  # Will have no effect on Create 3.

robot.play()
