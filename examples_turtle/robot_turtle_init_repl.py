#!/usr/bin/env python3
#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

import argparse
import atexit
import sys

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import Root
from irobot_edu_sdk.robot_turtle import RobotTurtle
from irobot_edu_sdk import utils

# Create a turtle.Turtle()-esque interface and connect using Bluetooth
# Intended to be run with interactive mode, as a REPL (Read, Execute, Print, Loop) such as
#    python3 -i robot_turtle_init_repl.py
# After executing the canonical Python prompt (">>>") will be displayed
# Then you can type a command at the prompt such as
#    >>> rt.forward(16)
# And the display will respond accordingly.
# You may also use --bluetooth DEVICE_NAME argument to connect to specified DEVICE_NAME,
# You may also use --log DEBUG for additional diagnostic information
# For example,
#    python3 -i robot_turtle_init_repl.py --log DEBUG --bluetooth MY_ROBOT_NAME
# By default (with no arguments) it will attempt to connect to the first found device at nominal INFO log level.

# Retrieve arguments; run WITHOUT interactive mode for more information
#    python3 robot_turtle_init_repl.py --help
parser = argparse.ArgumentParser(description='iRobot EDU Turtle interface REPL initializer',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 parents=[utils.log_level_argument_parser, utils.robot_bluetooth_argument_parser])
my_args = parser.parse_args()
logger = utils.get_logger('repl_init', my_args.log_level)

if my_args.bluetooth_name:  # if value is '' or None, use no argument
    logger.info('Attempting to Bluetooth Robot with specified name "%s"...', my_args.bluetooth_name)
    backend = Bluetooth(my_args.bluetooth_name)  # e.g., 'ROBOT_NAME'
else:
    logger.info('Attempting to find any available Bluetooth Robot...')
    backend = Bluetooth()  # connect to first available (unspecified) device

# The following uses the Root class interface, but should also work for Create3
# You may also change this to use `Robot(backend)` or `Create3(backend)`
# if you need particular specifics or face any issues
robot = Root(backend)
print('Attempting to connect to robot; please wait (this may take several seconds)...')
rt = RobotTurtle(robot)

if sys.flags.interactive:
    # Allow to gracefully clean up after keyboard interrupt or interactive exit
    atexit.register(rt.stop)

    print('Success! Now you may run Turtle commands on the "rt" (RobotTurtle) object such as...')
    print('    rt.forward(16)')
    print('    rt.right(90)')
else:
    print('Run this script in interactive mode instead; e.g.,')
    print(f'   python3 -i {sys.argv[0]}')
    print(f'Or run as follows for more information:')
    print(f'   python3 {sys.argv[0]} --help')
