#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

import random

robot = Root(Bluetooth())

@event(robot.when_touched, [True, True, True, True])
async def rps(robot):
    await robot.set_marker_and_eraser_up()
    await robot.move(16)

    action = random.randint(0, 2)

    if action == 0:
        # Scissors
        await robot.turn_right(15)
        await robot.move(15)
        await robot.turn_right(180)
        await robot.set_marker_down()
        await robot.move(20)
        await robot.arc_right(360, 3)
        await robot.set_marker_and_eraser_up()
        await robot.turn_right(180)
        await robot.move(5)
        await robot.turn_left(30)
        await robot.move(15)
        await robot.turn_right(180)
        await robot.set_marker_down()
        await robot.move(20)
        await robot.arc_left(360, 3)

    elif action == 1:
        # Rock
        await robot.reset_navigation()
        await robot.set_marker_down()
        await robot.navigate_to(-2, 6)
        await robot.navigate_to(3, 16)
        await robot.navigate_to(9, 11)
        await robot.navigate_to(13, 15)
        await robot.navigate_to(18, 9)
        await robot.navigate_to(15, 0)
        await robot.navigate_to(0, 0)

    else:
        # Paper
        await robot.set_marker_down()
        await robot.move(20)
        await robot.turn_right(90)
        await robot.move(14)
        await robot.turn_right(90)
        await robot.move(2)
        await robot.turn_left(90)
        await robot.move(2)
        await robot.turn_left(135)
        await robot.move(2.8284)
        await robot.turn_right(180)
        await robot.move(2.8284)
        await robot.turn_right(45)
        await robot.move(18)
        await robot.turn_right(90)
        await robot.move(16)

    await robot.set_marker_and_eraser_up()

robot.play()