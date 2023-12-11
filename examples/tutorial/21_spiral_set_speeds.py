#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Now let's draw another simple spiral, this time by changing the speed of the wheels incrementally.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())


@event(robot.when_play)
async def spiral(robot):
    STEPS = 20

    left_speed = -2
    await robot.set_marker_down()  # Will have no effect on Create 3.
    for i in range(0, STEPS):
        print(f"{i / STEPS * 100:.1f}% complete")

        left_speed += 0.2
        await robot.set_wheel_speeds(left_speed, 6)
        await robot.wait(1)
    await robot.stop()
    print("Done!")

robot.play()
