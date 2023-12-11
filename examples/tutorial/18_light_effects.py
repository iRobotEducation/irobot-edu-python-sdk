#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Bored of just turning the robot's lights on and off? Here are the light effects!

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())

time = 2


@event(robot.when_play)
async def play(robot):
    while True:
        await robot.set_lights_spin_rgb(255, 255, 0)
        await robot.wait(time)
        await robot.set_lights_blink_rgb(255, 50, 60)
        await robot.wait(2*time)
        await robot.set_lights_on_rgb(0, 0, 255)
        await robot.wait(time)
        await robot.set_lights_off()
        await robot.wait(time)

robot.play()
