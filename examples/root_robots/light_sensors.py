#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

# A simple example to learn about light sensor events.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Root

robot = Root(Bluetooth())

@event(robot.when_light_seen, [Root.LightEvent.DARKER])
async def dark(robot):
    print('Event: Darker')

@event(robot.when_light_seen, [Root.LightEvent.BRIGHTER])
async def bright(robot):
    print('Event: Brighter')

@event(robot.when_play)
async def play(robot):
    while True:
        print(await robot.get_light_values())

robot.play()
