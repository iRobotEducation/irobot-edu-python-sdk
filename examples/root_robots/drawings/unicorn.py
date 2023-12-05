#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

robot = Root(Bluetooth())

@event(robot.when_play)
async def bella(robot):
    # Snout
    await robot.set_marker_down()
    await robot.move(2.3)
    await robot.turn_right(90)
    await robot.arc_left(60, 3.4)
    await robot.turn_right(180)
    await robot.arc_right(60, 3.4)
    await robot.move(9.4)
    await robot.arc_right(50, 3.4)
    await robot.turn_right(145)
    await robot.arc_left(75, 4.8)
    await robot.turn_right(180)
    await robot.arc_right(75, 4.8)
    await robot.turn_right(35)
    await robot.arc_right(100, 3.4)
    await robot.move(12.62)

    # Horn
    await robot.turn_left(90)
    await robot.move(-2)
    await robot.move(14.71)
    await robot.turn_left(165)
    await robot.move(13.2)
    await robot.turn_right(75)
    await robot.move(3.1)
    await robot.turn_right(45)
    await robot.arc_right(135, 3.4)
    await robot.turn_right(120)
    await robot.arc_left(115, 1.8)

    await robot.set_marker_and_eraser_up()
    await robot.move(3)

    # Mane
    await robot.set_marker_down()
    await robot.arc_right(210, 13.2)
    await robot.arc_left(60, 6.85)
    await robot.turn_right(90)
    await robot.arc_right(145, 5.58)
    await robot.arc_left(190, 8.85)
    await robot.turn_left(90)

    await robot.set_marker_and_eraser_up()
    await robot.move(8)

    # Eye
    await robot.set_marker_down()
    await robot.turn_right(30)
    await robot.arc_right(135, 2)

    await robot.set_marker_and_eraser_up()
    await robot.turn_left(85)
    await robot.move(6.5)
    await robot.turn_right(90)

    # Nostril
    await robot.set_marker_down()
    await robot.arc_left(180, 0.5)

    await robot.set_marker_and_eraser_up()
    await robot.move(-20)

robot.play()