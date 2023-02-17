#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Root

robot = Root(Bluetooth())

@event(robot.when_light_seen, [Root.LIGHT_DARK])
async def dark(robot):
    print('Event: Dark')

@event(robot.when_light_seen, [Root.LIGHT_BRIGHT])
async def bright(robot):
    print('Event: Bright')

@event(robot.when_light_seen, [Root.LIGHT_RIGHT_BRIGHTER_THAN_LEFT])
async def roverl(robot):
    print('Event: R > L')

@event(robot.when_light_seen, [Root.LIGHT_LEFT_BRIGHTER_THAN_RIGHT])
async def loverr(robot):
    print('Event: L > R')

@event(robot.when_play)
async def play(robot):
    while True:
        print(await robot.get_light_values())

robot.play()
