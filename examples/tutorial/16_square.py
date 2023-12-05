#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Want to draw a square?

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def draw_square(robot):
    await robot.set_marker_down()  # Will have no effect on Create 3.

    # The "_" means that we are not using the temporal variable to get any value when iterating.
    # So the purpose of this "for" loop is just to repeat 4 times the actions inside it:
    for _ in range(4):
        await robot.move(6)  # cm
        await robot.turn_left(90)  # deg
    await robot.set_marker_and_eraser_up()  # Will have no effect on Create 3.

robot.play()
