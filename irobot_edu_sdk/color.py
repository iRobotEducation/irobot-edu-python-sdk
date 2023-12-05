#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

from .utils import bound


class Color:
    def __init__(self, red: int, green: int, blue: int):
        """ red, green and blue parameters must be between 0 and 255 """
        self.red = bound(red, 0, 255)
        self.green = bound(green, 0, 255)
        self.blue = bound(blue, 0, 255)
