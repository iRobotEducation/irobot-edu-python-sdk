#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Very basic example for avoiding front obstacles.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())
speed = 10
th = 150


async def forward(robot):
    await robot.set_lights_on_rgb(0, 255, 0)
    await robot.set_wheel_speeds(speed, speed)


async def backoff(robot):
    await robot.set_lights_on_rgb(255, 80, 0)
    await robot.move(-20)
    await robot.turn_left(45)


def front_obstacle(sensors):
    print(sensors[3])
    return sensors[3] > th


@event(robot.when_play)
async def play(robot):
    await forward(robot)
    while True:
        sensors = (await robot.get_ir_proximity()).sensors
        if front_obstacle(sensors):
            await backoff(robot)
            await forward(robot)

robot.play()
