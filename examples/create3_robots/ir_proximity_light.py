#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())


@event(robot.when_play)
async def play(robot):
    print('Try moving your hand right in front of the 3 front-central IR sensors')
    while True:
        sensors = (await robot.get_ir_proximity()).sensors
        r = 255 * sensors[2] / 4095
        g = 255 * sensors[3] / 4095
        b = 255 * sensors[4] / 4095
        await robot.set_lights_on_rgb(r, g, b)

robot.play()
