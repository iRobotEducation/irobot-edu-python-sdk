#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Let's draw a simple spiral using "turtle geometry" (turn and move) commands.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def spiral(robot):
    STEPS = 20
    TRANSLATE = 1 #cm

    await robot.set_marker_down()  # Will have no effect on Create 3.
    for i in range(0, STEPS):
        print(f"{i / STEPS * 100:.1f}% complete")

        await robot.turn_left(2*i + 10)
        await robot.move(TRANSLATE)
    await robot.set_marker_and_eraser_up()  # Will have no effect on Create 3.
    print("Done!")

robot.play()
