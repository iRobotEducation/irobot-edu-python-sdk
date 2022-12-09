#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())


@event(robot.when_play)
async def play(robot):
    print('Try moving your hand right in front of the front-central IR sensor')
    while True:
        sensors = (await robot.get_ir_proximity()).sensors
        await robot.play_note(sensors[3], Note.QUARTER)  # sensors[3] is the central front sensor.

robot.play()
