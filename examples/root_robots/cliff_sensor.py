#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2024 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root

robot = Root(Bluetooth())

@event(robot.when_cliff_sensor, [True])
async def cliff(robot):
    print('There\'s a cliff!')

robot.play()
