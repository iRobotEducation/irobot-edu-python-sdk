#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

robot = Root(Bluetooth())

@event(robot.when_play)
async def easy_as(robot):
    # Base
    await robot.set_marker_down()
    await robot.turn_right(135)
    await robot.move(8)
    await robot.turn_left(45)
    await robot.move(25)
    await robot.turn_left(45)
    await robot.move(8)
    await robot.turn_left(135)
    await robot.move(-3)
    await robot.move(42)
    await robot.turn_right(90)
    await robot.move(2.5)

    # Crimps
    for _ in range(10):
        await robot.arc_right(180, 1.24)
        await robot.arc_left(180, 0.75)

    # Top
    await robot.arc_right(180, 1.24)
    await robot.move(2.5)
    await robot.move(-2.5)
    await robot.arc_right(-90, 1.24)
    await robot.turn_left(120)
    await robot.arc_left(120, 23)

    await robot.set_marker_and_eraser_up()
    await robot.arc_left(-60, 23)
    await robot.turn_left(90)
    await robot.move(3)

    # Vents
    await robot.set_marker_down()
    await robot.move(3)
    await robot.move(-1.5)

    await robot.set_marker_and_eraser_up()
    await robot.turn_right(90)
    await robot.move(6)
    await robot.set_marker_down()
    await robot.turn_right(135)
    await robot.move(3)

    await robot.set_marker_and_eraser_up()
    await robot.turn_right(45)
    await robot.move(8)
    await robot.set_marker_down()
    await robot.turn_right(45)
    await robot.move(3)

    await robot.set_marker_and_eraser_up()
    await robot.move(-9)
    await robot.turn_left(135)
    await robot.move(4)

    # Steam
    await robot.set_marker_down()
    await robot.turn_left(60)
    await robot.arc_right(120, 2)
    await robot.arc_left(120, 2)

    await robot.set_marker_and_eraser_up()
    await robot.turn_left(45)
    await robot.move(7)
    await robot.set_marker_down()
    await robot.turn_left(135)
    await robot.arc_right(120, 2)
    await robot.arc_left(120, 2)

    await robot.set_marker_and_eraser_up()
    await robot.turn_left(30)
    await robot.move(14)
    await robot.set_marker_down()
    await robot.turn_left(160)
    await robot.arc_right(120, 2)
    await robot.arc_left(120, 2)

    # Drive away
    await robot.set_marker_and_eraser_up()
    await robot.move(24)

robot.play()