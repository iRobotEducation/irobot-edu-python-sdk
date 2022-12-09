#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Let's draw a simple spiral using "turtle geometry" commands (turn and move) commands.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def spiral(robot):
    await robot.set_marker(Root.MARKER_DOWN)  # Will have no effect on Create 3.
    for i in range(0, 40):
        await robot.turn_left(2*i + 10)
        await robot.move(5)
    await robot.set_marker(Root.MARKER_UP)  # Will have no effect on Create 3.

robot.play()
