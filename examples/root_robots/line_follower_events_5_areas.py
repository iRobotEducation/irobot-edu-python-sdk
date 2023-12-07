#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

# Follow a green line with five color sensor zones.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Robot, Root
ColorID = Root.ColorID

robot = Root(Bluetooth())

speed = 5.0

@event(robot.when_color_scanned, [ColorID.GREEN, ColorID.SKIP, ColorID.SKIP, ColorID.SKIP, ColorID.SKIP])
async def left_full(robot):
    await robot.set_wheel_speeds(0, speed)

@event(robot.when_color_scanned, [ColorID.SKIP, ColorID.GREEN, ColorID.SKIP, ColorID.SKIP, ColorID.SKIP])
async def left_half(robot):
    await robot.set_wheel_speeds(speed/2, speed)

@event(robot.when_color_scanned, [ColorID.SKIP, ColorID.SKIP, ColorID.SKIP, ColorID.SKIP, ColorID.GREEN])
async def right_full(robot):
    await robot.set_wheel_speeds(speed, 0)

@event(robot.when_color_scanned, [ColorID.SKIP, ColorID.SKIP, ColorID.SKIP, ColorID.GREEN, ColorID.SKIP])
async def right_half(robot):
    await robot.set_wheel_speeds(speed, speed/2)

@event(robot.when_color_scanned, [ColorID.SKIP, ColorID.SKIP, ColorID.GREEN, ColorID.SKIP, ColorID.SKIP])
async def forward(robot):
    await robot.set_wheel_speeds(speed, speed)

@event(robot.when_play)
async def when_play(robot):
    await robot.say("Following!")
    await robot.set_lights_spin_rgb(0, 0, 255)
    await robot.set_wheel_speeds(speed, speed)

robot.play()
