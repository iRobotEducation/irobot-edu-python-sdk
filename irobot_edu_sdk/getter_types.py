#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

import math
from typing import List

# Getter classes used both for Root's getters and for the params on
# its event callbacks. These classes are Root specific.


class Pose:
    def __init__(self, x=0, y=0, heading=90):
        self.x = x
        self.y = y
        self.heading = heading  # [deg]

    def move(self, distance):
        self.x += distance * math.cos(math.radians(self.heading))
        self.y += distance * math.sin(math.radians(self.heading))

    def turn_left(self, angle):
        self.heading += angle


class Movement:
    def __init__(self, distance=0, angle=0):
        self.distance = distance
        self.angle = self.minimize_angle(angle)  # [deg]

    @staticmethod
    def minimize_angle(angle):
        result = angle
        while result > 180:
            result -= 360
        while result < -180:
            result += 360
        return result


class IrProximity:
    def __init__(self):
        self.sensors: List[int] = []


class ColorSensor:
    def __init__(self):
        # contains the 32 areas from the real sensor
        self.colors: List[int] = []


class Bumpers:
    def __init__(self):
        self.left = False
        self.right = False


class TouchSensors:
    def __init__(self):
        self.front_left = False
        self.front_right = False
        self.back_right = False
        self.back_left = False


class CliffSensor:
    def __init__(self):
        self.disable_motors = False


class LightSensors:
    def __init__(self):
        self.state: int = 0
        self.left: int = 0
        self.right: int = 0


class IPv4Addresses:
    def __init__(self):
        self.wlan0: List[int] = []
        self.wlan1: List[int] = []
        self.usb0: List[int] = []


class MotorStall:
    def __init__(self):
        self.motor: int = 0
        self.cause: int = 0


class Battery:
    def __init__(self):
        self.millivolts: int = 0
        self.percent: int = 0
