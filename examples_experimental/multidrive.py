#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2024 iRobot Corporation. All rights reserved.
#

import math

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Root

backend1 = Bluetooth('R00T')
backend2 = Bluetooth('Root')
wheel = Root(backend1)
robot = Root(backend2)

accel = False

@event(wheel.when_play)
async def play(wheel):
    global accel
    print('play wheel!')  # Put your code here!
    while True:
        accel = await wheel.get_accelerometer()

@event(robot.when_play)
async def play(robot):
    global accel
    print('play robot!')  # Put your code here!
    while True:
        try:
            angle = abs(math.atan2(-accel[0], accel[1]))
            speed = 10 - min(abs(accel[2] / 100), 10)
        except TypeError: # other robot hasn't published yet
            angle = math.pi / 2
            speed = 0

        # normalize to [-2, 2] from left to right
        angle /= (0.2 * math.pi)
        angle -= 2

        vl = max(min((  angle  + 1) * speed, 10), -10)
        vr = max(min(((-angle) + 1) * speed, 10), -10)

        await robot.set_wheel_speeds(vl, vr)

wheel.play()
#robot.play() - only want to have one call to play since it's blocking; doesn't matter which object you call from
