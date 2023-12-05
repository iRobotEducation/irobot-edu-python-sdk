#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root

robot = Root(Bluetooth())

@event(robot.when_play)
async def cake(robot):
    # Body
    await robot.set_marker_down()
    for _ in range(4):
        await robot.move(16)
        await robot.turn_right(90)

    # Icing
    await robot.set_marker_and_eraser_up()
    await robot.move(12)
    await robot.set_marker_down()
    for _ in range(2):
        await robot.arc_right(-180, 2)
        await robot.arc_left(180, 2)

    # Candle
    await robot.set_marker_and_eraser_up()
    await robot.move(4)
    await robot.turn_left(90)
    await robot.move(7)
    await robot.turn_right(90)

    await robot.set_marker_down()
    await robot.move(6)
    await robot.turn_left(90)
    await robot.move(1)
    await robot.turn_right(90)
    await robot.move(1)
    await robot.turn_right(90)
    await robot.arc_left(135, 1)
    await robot.move(1)
    await robot.turn_left(90)
    await robot.move(1)
    await robot.arc_left(135, 1)
    await robot.turn_right(90)
    await robot.move(1)
    await robot.turn_right(90)
    await robot.move(1)
    await robot.turn_left(90)
    await robot.move(6)

    # Move away
    await robot.set_marker_and_eraser_up()
    await robot.turn_right(135)
    await robot.move(16)

@event(robot.when_play)
async def cycle(robot):
    while True:
        await robot.set_lights_on_rgb(255, 0, 0)
        await robot.wait(0.3)
        await robot.set_lights_on_rgb(255, 255, 0)
        await robot.wait(0.3)
        await robot.set_lights_on_rgb(0, 255, 0)
        await robot.wait(0.3)
        await robot.set_lights_on_rgb(0, 255, 255)
        await robot.wait(0.3)
        await robot.set_lights_on_rgb(0, 0, 255)
        await robot.wait(0.3)
        await robot.set_lights_on_rgb(255, 0, 255)
        await robot.wait(0.3)

robot.play()