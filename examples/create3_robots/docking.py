#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2022 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())


@event(robot.when_play)
async def play(robot):
    # Trigger an undock and then dock. Try putting this in an infinite loop!
    print('Undock')
    print(await robot.undock())
    # print('get_docking_values:', await robot.get_docking_values())
    print('Dock')
    print(await robot.dock())
    # print('get_docking_values:', await robot.get_docking_values())

@event(robot.when_play)
async def play(robot):
    # Dock sensor visualizer; could be improved with events
    while True:
        sensor = (await robot.get_docking_values())['IR sensor 0']
        r = 255 * ((sensor & 8)/8)
        g = 255 * ((sensor & 4)/4)
        b = 255 * (sensor & 1)
        await robot.set_lights_on_rgb(r, g, b)

robot.play()
