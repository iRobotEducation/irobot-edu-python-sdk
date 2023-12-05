#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

robot = Root(Bluetooth())

@event(robot.when_play)
async def symbol(robot):
    # Get into position; the robot assumes it is facing "up" at the start,
    #  at the top left of the symbol inside the circle.
    await robot.turn_right(90)
    await robot.set_marker_down()

    # R
    await robot.move(6.6)
    await robot.arc_right(90, 4.98)
    await robot.arc_right(67.5, 7.68)
    await robot.turn_left(95)
    await robot.move(8.97)
    await robot.turn_right(118.5)
    await robot.move(6.64)
    await robot.turn_right(61.5)
    await robot.move(13.34)
    await robot.turn_left(139.6)
    await robot.move(12)
    await robot.turn_right(78.12)
    await robot.move(5.56)
    await robot.turn_right(101.88)
    await robot.move(6.25)

    await robot.arc_right(75, 7)
    await robot.move(5.25)
    await robot.arc_left(90, 2.15)
    await robot.arc_left(90, 1.4)
    await robot.move(4.67)
    await robot.turn_right(101.88)
    await robot.move(4.94)
    await robot.turn_left(101.88)

    # Tittle
    await robot.set_marker_and_eraser_up()
    await robot.move(5.13)
    await robot.turn_right(90)
    await robot.move(0.2)
    await robot.turn_right(90)
    await robot.set_marker_down()
    await robot.arc_right(360, 2.66)
    await robot.set_marker_and_eraser_up()

    # Circle
    await robot.move(5.5)
    await robot.turn_left(90)
    await robot.move(9.8)
    await robot.turn_right(90)
    await robot.set_marker_down()
    await robot.arc_right(360, 20)

    await robot.set_marker_and_eraser_up()

robot.play()
