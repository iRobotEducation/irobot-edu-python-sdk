#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# Now let's draw another simple spiral, this time by changing the speed of the wheels incrementally.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def spiral(robot):
    left_speed = -2
    await robot.set_marker(Root.MARKER_DOWN)  # Will have no effect on Create 3.
    for _ in range(0, 40):
        left_speed += 0.2
        await robot.set_wheel_speeds(left_speed, 6)
        await robot.wait(1)
    await robot.stop()

robot.play()
