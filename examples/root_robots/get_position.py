#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# This program is just used for testing the navigation with a single move.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())


def f(value):
    return format(value, '.2f')


async def print_pos(robot):
    pos = await robot.get_position()
    print('🐢 (x  y  heading) = (', f(pos.x),  f(pos.y), f(pos.heading), ')')


@event(robot.when_play)
async def play(robot):
    await robot.set_lights_rgb(30, 255, 100)
    await robot.play_note(Note.A5, .5)

    distance = 5

    await robot.navigate_to(distance, distance)
    await print_pos(robot)
    await robot.reset_navigation()
    await print_pos(robot)
    await robot.navigate_to(distance, distance)
    await print_pos(robot)

    await robot.turn_left(90)
    await print_pos(robot)
    await robot.move(-distance)
    await print_pos(robot)

    await robot.set_lights_rgb(30, 255, 100)

robot.play()
