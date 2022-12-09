#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# Navigation works differently in Root and Create 3 robots, so we need to create an instance of the specific robot class here.
robot = Root(Bluetooth())


@event(robot.when_play)
async def play(robot):
    await robot.set_lights_rgb(30, 255, 100)
    await robot.play_note(Note.A5, .5)

    distance = 16

    await robot.navigate_to(0, distance)
    await robot.navigate_to(distance, distance)
    await robot.navigate_to(distance, 0)
    await robot.navigate_to(0, 0)

    await robot.set_lights_rgb(30, 100, 255)

    distance = -distance

    await robot.navigate_to(0, distance)
    await robot.navigate_to(distance, distance)
    await robot.navigate_to(distance, 0)
    await robot.navigate_to(0, 0)

    await robot.set_lights_rgb(30, 255, 100)

robot.play()
