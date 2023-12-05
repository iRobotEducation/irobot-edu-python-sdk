#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

robot = Root(Bluetooth())

@event(robot.when_play)
async def my_gourd(robot):
    await robot.move(8)

    # Flesh
    await robot.set_marker_down()
    await robot.set_lights_blink_rgb(255, 64, 0)
    await robot.turn_left(90)
    await robot.arc_left(45, 8)
    await robot.turn_right(90)
    await robot.arc_left(90, 8)
    await robot.arc_left(90, 20)
    await robot.arc_left(90, 8)
    await robot.turn_right(90)
    await robot.arc_left(90, 8)
    await robot.turn_right(90)
    await robot.arc_left(90, 8)
    await robot.arc_left(90, 20)
    await robot.arc_left(90, 8)
    await robot.turn_right(90)
    await robot.arc_left(45, 8)
    await robot.arc_left(20, 8)

    # STEM Stem
    await robot.set_lights_blink_rgb(0, 255, 0)
    await robot.turn_right(90)
    await robot.arc_right(90, 12)
    await robot.turn_right(90)
    await robot.move(5)
    await robot.turn_right(90)
    await robot.arc_left(90, 8)

    # Vine
    await robot.turn_left(90)
    await robot.move(3)
    await robot.arc_left(375, 1)
    await robot.move(3)
    await robot.arc_left(375, 1)
    await robot.move(2)

    # Get into position
    await robot.set_lights_off()
    await robot.set_marker_and_eraser_up()
    await robot.move(-24)
    await robot.turn_left(40)

    '''
    What will your coded jack-o-lantern look like?
    Add more below to carve a face with code!
    '''

robot.play()