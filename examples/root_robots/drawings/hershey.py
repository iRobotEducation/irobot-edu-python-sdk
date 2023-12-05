#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

# Write arbitrary text using the Hershey vector fonts. Set the "size" and "text" below.
text = "Hi!"
size = 16

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root

# This example only runs on the web version of the iRobot Edu SDK.
# Running in a native Python install will give a SyntaxError.
# To solve this, delete the next two lines and install "Hershey-Fonts" with your favorite package manager.
import micropip
await micropip.install("Hershey-Fonts")
from HersheyFonts import HersheyFonts

robot = Root(Bluetooth())

font = HersheyFonts()
font.load_default_font()
font.normalize_rendering(size)

def swap_coords(x, y, x1, y1, x2, y2):
# Returns True if (x2, y2) is closer than (x1, y1) to (x, y)
    try:
        dist1 = ((x-x1)**2 + (y-y1)**2)**0.5
        dist2 = ((x-x2)**2 + (y-y2)**2)**0.5
        return dist1 > dist2
    except TypeError:
        return False

@event(robot.when_play)
async def write(robot):
    await robot.reset_navigation()
    prev_x = None
    prev_y = None

    for (x1, y1), (x2, y2) in font.lines_for_text(text):
        if swap_coords(prev_x, prev_y, x1, y1, x2, y2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if x1 != prev_x or y1 != prev_y:
            await robot.set_marker_and_eraser_up()
            await robot.navigate_to(x1, y1)
            await robot.set_marker_down()
        await robot.navigate_to(x2, y2)
        prev_x = x2
        prev_y = y2

robot.play()
