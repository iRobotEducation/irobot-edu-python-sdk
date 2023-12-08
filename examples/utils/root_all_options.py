#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2023 iRobot Corporation. All rights reserved.
#

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root
from irobot_edu_sdk.music import Note
ColorID = Root.ColorID

# robot is the instance of the robot that will allow us to call its methods and to define events with the @event decorator.
robot = Root(Bluetooth())  # Will connect to the first robot found.
speed = 10.0


def f(value):
    return format(value, '.2f')


async def print_pos(robot):
    pos = await robot.get_position()
    print('🐢 (x  y  heading) = (', f(pos.x),  f(pos.y), f(pos.heading), ')')


@event(robot.when_bumped, [True, False])  # [left, right]
# Please note that the 'robot' parameter is not related with the 'robot' instance: robot is what can be used inside the event's function.
async def bumped(robot):  # The name of this function can be any valid Python function name.
    print('Left bumper pressed')
    await robot.set_lights_on_rgb(255, 0, 0)  # red
    await robot.set_wheel_speeds(-speed, speed)


@event(robot.when_bumped, [False, True])
async def bumped(robot):
    print('Right bumper pressed')
    await robot.set_lights_on_rgb(0, 255, 0)  # green.
    await robot.set_wheel_speeds(speed, -speed)


@event(robot.when_bumped, [True, True])
async def bumped(robot):
    print('Any bumper pressed; bumper state is', await robot.get_bumpers())


@event(robot.when_bumped, [True, True])
async def bumped(robot):
    for _ in range(4):
        await robot.play_note(440, 0.25)  # A4
        await robot.play_note(Note.A5, 0.75)


@event(robot.when_touched, [True, False,    # Front touch sensors.
                            False, False])  # Back touch sensors.
async def touched(robot):
    print('Front-left sensor touched (task 1)')
    print('Raw Color Sensor Values')
    for c in Root.ColorLighting:
        print(c, await robot.get_color_values(c, Root.ColorFormat.ADC_COUNTS))

    print('Parsed Color Sensor Values')
    print("IDs", await robot.get_color_ids())


@event(robot.when_touched, [True, True,
                            True, True])
async def touched(robot):
    print('Any touch sensor touched; touch state is', await robot.get_touch_sensors())


@event(robot.when_touched, [True, False,
                            False, False])
async def touched(robot):
    print('Front-left sensor touched (task 2)')
    await robot.set_marker(robot.MarkerPos.DOWN)
    await robot.turn_right(90)
    await robot.navigate_to(5, 10)
    await print_pos(robot)
    await robot.reset_navigation()
    await print_pos(robot)


@event(robot.when_touched, [False, True,
                            False, False])
async def touched(robot):
    print('Front-right sensor touched')
    await robot.set_lights_spin_rgb(255, 255, 0)
    await robot.move(2)
    await robot.arc_right(90, 4)
    await robot.arc_right(-90, 4)
    await robot.move(-2)


@event(robot.when_touched, [False, False,
                            True, False])
async def touched(robot):
    print('Rear-left sensor touched')
    await robot.set_marker(robot.MarkerPos.UP)


@event(robot.when_touched, [False, False,
                            False, True])
async def touched(robot):
    print('Rear-right sensor touched')
    await robot.set_marker(robot.MarkerPos.DOWN)


@event(robot.when_color_scanned, [ColorID.GREEN])
async def left(robot):
    print("Color sensor sees green!")


@event(robot.when_color_scanned, [ColorID.BLUE])
async def left(robot):
    print("Color sensor sees blue!")


@event(robot.when_color_scanned, [ColorID.RED])
async def left(robot):
    print("Color sensor sees red!")


@event(robot.when_color_scanned, [ColorID.BLACK])
async def left(robot):
    print("Color sensor sees black!")


@event(robot.when_light_seen, [Root.LightEvent.DARKER])
async def dark(robot):
    print('Things got darker; sensor values are', await robot.get_light_values())


@event(robot.when_light_seen, [Root.LightEvent.BRIGHTER])
async def bright(robot):
    print('Things got brighter; sensor values are', await robot.get_light_values())


@event(robot.when_play)
async def play(robot):
    print('play 1')
    await robot.set_lights_on_rgb(100, 100, 255)


@event(robot.when_play)
async def play(robot):
    print('play 2')
    battery = await robot.get_battery_level()
    print('Name:', await robot.get_name())
    print('Version:', await robot.get_version_string())
    print('Battery:', battery[0], 'mV; ', battery[1], '%')
    print('Serial #:', await robot.get_serial_number())
    print('SKU:', await robot.get_sku())
    # await robot.set_name('NewName')  # Uncomment this line if you want to try renaming your robot.


@event(robot.when_play)
async def play(robot):
    print('play 2')
    for _ in range(4):
        await robot.set_lights_on_rgb(100, 100, 255)
        await robot.wait(1)
        await robot.set_lights_on_rgb(0, 255, 80)
        await robot.wait(1)


# Triggers all the "when_play" events as parallel tasks.
robot.play()
