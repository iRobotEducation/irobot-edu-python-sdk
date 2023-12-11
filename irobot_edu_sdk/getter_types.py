#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

import math
from typing import List
from struct import unpack

from .packet import Packet

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

    def arc(self, angle, radius):
        angle *= -1
        radius *= -1

        chord = radius * 2 * math.sin(math.radians(angle/2))
        self.x += chord * math.cos(math.radians(self.heading + (angle/2)))
        self.y += chord * math.sin(math.radians(self.heading + (angle/2)))

        self.heading += angle

    def set(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

    def set_from_packet(self, packet):
        if packet:
            payload = packet.payload
            #timestamp = unpack('>I', payload[0:4])[0]
            self.x = unpack('>i', payload[4:8])[0] / 10
            self.y = unpack('>i', payload[8:12])[0] / 10
            self.heading = unpack('>h', payload[12:14])[0] / 10
            return self
        return None

    def __str__(self):
        return f"Pose ({self.x:.2f}, {self.y:.2f}, {self.heading:.1f}°)"


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
    SENSORS_COUNT = 32
    def __init__(self, colors=[]):
        # contains the 32 areas from the real sensor
        self.colors: List[int] = self.expand_to_width(colors)

    def expand_to_width(self, colors):
        """
        This function takes a list of colors and expands them to the number of zones in the robot's sensor array.
        """
        zones = []
        zones_count = len(colors)

        if zones_count <= 0 or zones_count > self.SENSORS_COUNT:
            return zones

        pixels_per_zone = self.SENSORS_COUNT // zones_count
        remaining_pixels = self.SENSORS_COUNT % zones_count

        for i in range(0, zones_count):
            newZone = [colors[i]] * pixels_per_zone
            zones += newZone

        # try to distribute the remaining pixels (if any) in a symmetric way:
        if remaining_pixels != 0:
            if zones_count % 2 == 0:
                if remaining_pixels % 2 == 0:
                    # picks the color of the corresponding zone to generate the extra pixels
                    # first zone
                    zones = [colors[0]] * (remaining_pixels // 2) + zones
                    # last zone
                    zones += [colors[zones_count - 1]] * (remaining_pixels // 2)
                else:
                    # pixels can not be distributed symmetrically
                    raise ValueError('Invalid sensor detection zones count.')
            else:
                # picks the color from the central zone to generate the extra pixels
                extraPixels = [colors[zones_count // 2]] * (remaining_pixels)
                for i in extraPixels:
                    zones.insert(len(zones) // 2, i)  # central zone

        return zones

    def matches(self, friend):
        if len(self.colors) != len(friend.colors):
            return False

        for me, you in zip(self.colors, friend.colors):
            if me == you:
                return True
        return False


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


class DockingSensor:
    def __init__(self):
        self.contacts = None
        self.sensors = (None, None, None)


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
