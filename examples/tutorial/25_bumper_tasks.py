#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Let's do something more interesting with the parallel tasks, triggered by the robot's bumpers.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Root(Bluetooth())
#robot = Create3(Bluetooth())

speed = 10.0


@event(robot.when_bumped, [True, False])
async def bumped(robot):
    print ('Left bumper triggered')
    await robot.set_lights_on_rgb(255, 0, 0)
    await robot.set_wheel_speeds(-speed, speed)


@event(robot.when_bumped, [False, True])
async def bumped(robot):
    print ('Right bumper triggered')
    await robot.set_lights_on_rgb(0, 255, 0)
    await robot.set_wheel_speeds(speed, -speed)


@event(robot.when_bumped, [True, True])
async def music(robot):
    # This function will not be called again, since it never finishes.
    # Only tasks that are not currenctly running can be triggered.
    print('Music!')
    while True:
        # No need of calling "await hand_over()" in this infinite loop, because robot methods are all called with await.
        await robot.play_note(Note.A4, .1)
        await robot.wait(0.3)
        await robot.play_note(Note.A5, .1)
        await robot.wait(0.3)


@event(robot.when_play)
async def play(robot):
    print('First When Play Task: Hello!')
    await robot.turn_left(90)
    print("First When Play Task: Bye!")


@event(robot.when_play)
async def play(robot):
    print("Second When Play Task: Hello and Goodbye!")

robot.play()
