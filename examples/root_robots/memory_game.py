#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2023 iRobot Corporation. All rights reserved.
#
#          ____    ____  ________  ____    ____   ___   _______   ____  ____ 
#         |_   \  /   _||_   __  ||_   \  /   _|.'   `.|_   __ \ |_  _||_  _|
#           |   \/   |    | |_ \_|  |   \/   | /  .-.  \ | |__) |  \ \  / /  
#           | |\  /| |    |  _| _   | |\  /| | | |   | | |  __ /    \ \/ /   
#          _| |_\/_| |_  _| |__/ | _| |_\/_| |_\  `-'  /_| |  \ \_  _|  |_   
#         |_____||_____||________||_____||_____|`.___.'|____| |___||______|  
#                     ______       _       ____    ____  ________ 
#                   .' ___  |     / \     |_   \  /   _||_   __  |
#                  / .'   \_|    / _ \      |   \/   |    | |_ \_|
#                  | |   ____   / ___ \     | |\  /| |    |  _| _ 
#                  \ `.___]  |_/ /   \ \_  _| |_\/_| |_  _| |__/ |
#                   `._____.'|____| |____||_____||_____||________|
#
#  Repeat the pattern played by the robot by tapping the touch sensors in the correct order.
#
#                                  ./@@@@@@@@@@\.
#                               /@@@@@/  __  \@@@@@\
#                           /@@@@/     /@@@@\     \@@@@\
#                       /@@@@/        |@....@|        \@@@@\
#                   /@@@@/ .@@@\      |@....@|      /@@@. \@@@@\
#               /@@@@/  @@@()@@@       \@..@/       @@@()@@@  \@@@@\
#           /@@@@/      @@@@@@@@        |@@|        @@@@@@@@      \@@@@\
#        /@@@/          \@@@'           |@@|           `@@@/          \@@@\
#      @@@/                             |@@|                             \@@@
#     /@@/        ╭──────────────╮      |@@|      ╭──────────────╮        \@@\
#    |@@|         │              │      |@@|      │              │         |@@|
#    |@@|         │    GREEN     │      |@@|      │     RED      │         |@@|
#    |@@|         │              │      |@@|      │              │         |@@|
#    |@@|         ╰──────────────╯    /@@@@@@\    ╰──────────────╯         |@@|
#    |@@|    _______________________.@/......\@._______________________    |@@|
#    |@@|  /@@@@@@@@@@@@@@@@@@@@@@@@@@`......`@@@@@@@@@@@@@@@@@@@@@@@@@@\  |@@|
#    |@@|  \@@@@@@@@@@@@@@@@@@@@@@@@@@........@@@@@@@@@@@@@@@@@@@@@@@@@@/  |@@|
#    |@@|                           `@\....../@'                           |@@|
#    |@@|         ╭──────────────╮    \@@@@@@/    ╭──────────────╮         |@@|
#    |@@|         │              │      |@@|      │              │         |@@|
#    |@@|         │    YELLOW    │      |@@|      │     BLUE     │         |@@|
#    |@@|         │              │      |@@|      │              │         |@@|
#     \@@\        ╰──────────────╯      |@@|      ╰──────────────╯        /@@/
#      @@@\                             |@@|                             /@@@
#        \@@@\                          |@@|                          /@@@/
#           \@@@@\                      |@@|                      /@@@@/
#               \@@@@\                  |@@|                  /@@@@/
#                   \@@@@\              |@@|              /@@@@/
#                       \@@@@\          |@@|          /@@@@/
#                           \@@@@\      \@@/      /@@@@/
#                               \@@@@@\      /@@@@@/
#                                  `\@@@@@@@@@@/'

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Root
import random

was_touched = False
last_touched = "NONE"
robot = Root(Bluetooth())  # Will connect to the first robot found.

@event(robot.when_touched, [True, False,    # Front-left touched
                            False, False])
async def front_left(robot):
    global last_touched, was_touched
    if was_touched == True:
        return # Ignore duplicate touches
    last_touched = "GREEN"
    was_touched = True

@event(robot.when_touched, [False, True,    # Front-right touched
                            False, False])
async def front_right(robot):
    global last_touched, was_touched
    if was_touched == True:
        return # Ignore duplicate touches
    last_touched = "RED"
    was_touched = True

@event(robot.when_touched, [False, False,    # Rear-left touched
                            True, False])
async def rear_left(robot):
    global last_touched, was_touched
    if was_touched == True:
        return # Ignore duplicate touches
    last_touched = "YELLOW"
    was_touched = True

@event(robot.when_touched, [False, False,    # Rear-right touched
                            False, True])
async def rear_right(robot):
    global last_touched, was_touched
    if was_touched == True:
        return # Ignore duplicate touches
    last_touched = "BLUE"
    was_touched = True
        
async def play_color(color):
    if color == "GREEN":
        await robot.set_lights_rgb(0,255,0)
        await robot.play_note(391, 0.25)
        await robot.set_lights_rgb(0,0,0)
    elif color == "RED":
        await robot.set_lights_rgb(255,0,0)
        await robot.play_note(329, 0.25)
        await robot.set_lights_rgb(0,0,0)
    elif color == "YELLOW":
        await robot.set_lights_rgb(255,255,0)
        await robot.play_note(261, 0.25)
        await robot.set_lights_rgb(0,0,0)
    elif color == "BLUE":
        await robot.set_lights_rgb(0,0,255)
        await robot.play_note(195, 0.25)
        await robot.set_lights_rgb(0,0,0)
    elif color == "LOSE":
        for _ in range(3):
            await robot.set_lights_rgb(255,0,0)
            await robot.play_note(74, 0.25)
            await robot.set_lights_rgb(0,0,0)

@event(robot.when_play)
async def play(robot):
    global last_touched, was_touched
    colors = ["GREEN", "RED", "YELLOW", "BLUE"]
    solution = []

    print("Starting game!")
    while True:
        # Add to solution
        solution.append(random.choice(colors))

        # Play solution
        await robot.wait(0.5)
        for c in solution:
            await play_color(c)
        
        for c in solution:
            # Wait for next touch
            while not was_touched:
                await robot.wait(0.1)
            
            # Check touch against solution
            if last_touched == c:
                await play_color(last_touched)
            else:
                await play_color("LOSE")
                print("Game over! Score:", len(solution)-1)
                return

            # Reset for next touch
            was_touched = False 
        
robot.play()
