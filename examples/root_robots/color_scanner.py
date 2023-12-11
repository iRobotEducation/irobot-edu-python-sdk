#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#

# This example uses the robot like a wand scanner; see what the robot sees!

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Robot, Root
ColorID = Root.ColorID

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    colors = {ColorID.WHITE: Fore.WHITE + Back.WHITE + Style.BRIGHT + format(ColorID.WHITE, 'x'),
              ColorID.BLACK: Fore.BLACK + Back.WHITE + Style.NORMAL + format(ColorID.BLACK, 'x'),
              ColorID.RED: Fore.RED + Back.RED + Style.BRIGHT + format(ColorID.RED, 'x'),
              ColorID.GREEN: Fore.GREEN + Back.GREEN + Style.BRIGHT + format(ColorID.GREEN, 'x'),
              ColorID.BLUE: Fore.BLUE + Back.BLUE + Style.BRIGHT + format(ColorID.BLUE, 'x'),
              ColorID.ORANGE: Fore.YELLOW + Back.BLACK + Style.NORMAL + format(ColorID.ORANGE, 'x'),
              ColorID.YELLOW: Fore.YELLOW + Back.YELLOW + Style.BRIGHT + format(ColorID.YELLOW, 'x'),
              ColorID.MAGENTA: Fore.MAGENTA + Back.MAGENTA + Style.BRIGHT + format(ColorID.MAGENTA, 'x'),
              ColorID.LIME: Fore.GREEN + Back.BLACK + Style.BRIGHT + format(ColorID.LIME, 'x'),
              ColorID.CYAN: Fore.CYAN + Back.BLACK + Style.BRIGHT + format(ColorID.CYAN, 'x'),
              ColorID.VIOLET: Fore.MAGENTA + Back.BLACK + Style.NORMAL + format(ColorID.VIOLET, 'x'),
              ColorID.CERISE: Fore.RED + Back.BLACK + Style.NORMAL + format(ColorID.CERISE, 'x'),
              ColorID.LOW_INTENSITY: Fore.BLACK + Back.BLACK + Style.BRIGHT + format(ColorID.LOW_INTENSITY, 'x'),
              ColorID.LOW_SATURATION: Fore.WHITE + Back.BLACK + Style.NORMAL + format(ColorID.LOW_SATURATION, 'x'),
              'unk': Fore.RED + Back.CYAN + Style.NORMAL + '?',
              'eol': Style.RESET_ALL}
except ImportError:
    colors = {ColorID.WHITE: '⬜',
              ColorID.BLACK: '⬛',
              ColorID.RED: '🟥',
              ColorID.GREEN: '🟩',
              ColorID.BLUE: '🟦',
              ColorID.ORANGE: '🟠',
              ColorID.YELLOW: '🟨',
              ColorID.MAGENTA: '🟪',
              ColorID.LIME: '🟢',
              ColorID.CYAN: '🔵',
              ColorID.VIOLET: '🟣',
              ColorID.CERISE: '🔴',
              ColorID.LOW_INTENSITY: '🔳',
              ColorID.LOW_SATURATION: '🔲',
              'unk': '🟤',
              'eol': ''}

robot = Root(Bluetooth())

@event(robot.when_play)
async def sense(robot):
    await robot.set_wheel_speeds(1, 1)

    while True:
        try:
            for c in (await robot.get_color_ids())[::-1]:
                # Note -- the [::-1] reverses the order of the tuple,
                # which is necessary to make it look correct in the console.
                if c in ColorID:
                    print(colors[c], end='')
                else:
                    print(colors['unk'], end='')
            print(colors['eol'])

        except TypeError:
            print("Waiting for first color sensor event.")

        await robot.wait(0.25)

robot.play()
