#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# This example explores the robot's LED lights.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())

time = 0.3


@event(robot.when_play)
async def play(robot):
    while True:
        await robot.set_lights_rgb(255, -2344.43, 0)  # Red: negative numbers will count as 0.
        await robot.wait(time)
        await robot.set_lights_rgb(0, 120.4, 0)  # Green: floating point numbers will be rounded.
        await robot.wait(time)
        await robot.set_lights_rgb(-1000, 0, 100)  # Blue
        await robot.wait(time)

robot.play()
