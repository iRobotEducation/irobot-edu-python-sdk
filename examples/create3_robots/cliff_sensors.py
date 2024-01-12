#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2024 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3

robot = Create3(Bluetooth())

@event(robot.when_cliff_sensor, [True, False, False, False])
async def play(robot):
    print('Left')

@event(robot.when_cliff_sensor, [False, True, False, False])
async def play(robot):
    print('Front Left')

@event(robot.when_cliff_sensor, [False, False, True, False])
async def play(robot):
    print('Front Right')

@event(robot.when_cliff_sensor, [False, False, False, True])
async def play(robot):
    print('Right')

@event(robot.when_cliff_sensor, [True, True, True, True])
async def play(robot):
    print('There\'s a Cliff!')

robot.play()
