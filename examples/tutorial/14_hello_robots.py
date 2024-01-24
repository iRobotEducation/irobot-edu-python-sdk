#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# This is the minimum program for using the iRobot Edu Python SDK.

# Let's import all the relevant elements from the SDK.
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# Choose your robot!
robot = Root(Bluetooth())  # Will connect to the first robot found.
#robot = Create3(Bluetooth())


# Functions decorated with @event triggered by events.
# A robot.when_play event is triggered when the robot.play() method is called.
# It is important that event functions are declated as async.
@event(robot.when_play)
async def play(robot):  # The name of the function can be any valid Python function name.
    print('play!')  # Put your code here!

# This starts the robot's event system. It will do 2 things:
#
# 1. Trigger all the functions decorated with @event(robot.when_play).
# 2. Start listening for other events, such as the ones triggered by the robot's sensors.
#
robot.play()
