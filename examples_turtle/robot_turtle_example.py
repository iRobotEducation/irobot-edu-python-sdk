#!/usr/bin/env python3
#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

# Basic usage:
#   python3 root_turtle_test.py --bluetooth "your_root_name"

# Select one of --bluetooth or --serial for real robot use; none implies FakeRobot
# See --help for detail

# Also allows REPL interactivity; examples are
#   python3 -i root_turtle_test.py --serial /dev/ttyACM0
#   python3 -i root_turtle_test.py --serial /dev/tty.usbmodemRT1111F222222
#   python3 -i root_turtle_test.py --bluetooth "your_root_name"

# At the ">>> " prompt you may run Turtle commands using object named "robot" such as
#   >>> robot.forward(16)
#   >>> robot.right(90)

# If you run by device via Bluetooth, it may take a few moments to connect.
# After connected in interactive mode press <ENTER> to obtain a fresh ">>> " prompt.

# Debug asyncio by adding `python3 -X dev` argument
# or running with stubbed robot (provide neither --bluetooth nor --serial)
#   python3 -X dev -i root_turtle_test.py

import argparse
import atexit
from dataclasses import dataclass
import logging
import sys

from irobot_edu_sdk import utils
from irobot_edu_sdk.robots import event, Robot, Root, Create3
from irobot_edu_sdk.robot_turtle import RobotTurtle


@dataclass()
class _MyArgs:
    """Typed container for args namespace"""
    log_level: str = utils.DEFAULT_LOG_LEVEL_NAME
    robot_type: str = utils.DEFAULT_ROBOT
    bluetooth_name: str = None
    serial_device: str = None
    do_demo: bool = False


# Get some args
# See utils file for details used in 'parents'
my_args = _MyArgs()
parser = argparse.ArgumentParser(description='iRobot EDU Turtle interface wrapper for Root and Create3',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 parents=[utils.log_level_argument_parser, utils.robot_backend_argument_parser])
parser.add_argument('--demo', action='store_true', dest='do_demo', required=False, default=False,
                    help='Perform a brief demo at startup: draw a square (always on in non-interactive mode)')
parser.parse_args(namespace=my_args)

# Initialize logging
logger = utils.get_logger(name='rt_example', level=my_args.log_level)

# Create a backend. If backend is None, attempt an anonymous "greedy" Bluetooth backend connection.
# --bluetooth can accept optional (robot name) argument
if my_args.serial_device:
    logger.info('Creating USB-Serial backend using device "%s"...', my_args.serial_device)
    from irobot_edu_sdk.backend.serial import Serial
    backend = Serial(my_args.serial_device)  # e.g., '/dev/cu.usbmodemRT1810F024681'
else:  # use Bluetooth by default or if explicitly requested by flag or name
    logger.info('Creating Bluetooth backend...')
    from irobot_edu_sdk.backend.bluetooth import Bluetooth
    if not my_args.bluetooth_name:  # if value is '' or None, use no name
        logger.info('Attempting to find any available Bluetooth Robot...')
        backend = Bluetooth()  # connect to first available (unspecified) device
    else:
        logger.info('Attempting to Bluetooth Robot with specified name "%s"...', my_args.bluetooth_name)
        backend = Bluetooth(my_args.bluetooth_name)  # e.g., 'ROOT'

# Create a Robot object
robot = None
if backend:
    logger.info('Creating RobotTurtle with robot-type "%s"', my_args.robot_type)
    if my_args.robot_type.lower().startswith('create'):
        robot = Create3(backend)
    elif my_args.robot_type.lower().startswith('root'):
        robot = Root(backend)
    elif my_args.robot_type.lower().startswith('robot') or my_args.robot_type.lower().startswith('generic'):
        # This is default, if argument not specified
        robot = Robot(backend)
    else:
        logger.error('Unsupported robot type "%s"', my_args.robot_type)

if robot is None:
    logger.error('Could not connect to robot; exiting')
    sys.exit(1)

# Create a turtle.Turtle()-esque interface
print('Attempting to connect to robot; please wait (this may take several seconds)...')
rt = RobotTurtle(robot, log_level=my_args.log_level)

if not sys.flags.interactive or my_args.do_demo:
    logger.info('RobotTurtle...')
    logger.info('Drawing an example square using RobotTurtle...')

    # Only if the target robot has the capability, engage the pen
    if hasattr(robot, 'set_marker'):
        rt.pendown()

    # Move in a square
    for i in range(4):
        rt.forward(16)
        rt.right(90)

    if hasattr(robot, 'set_marker'):
        rt.penup()

    logger.info('Done with demo RobotTurtle...')

if sys.flags.interactive:
    # Allow to gracefully clean up after keyboard interrupt or interactive exit
    atexit.register(rt.stop)
    print('Success! Now you may run Turtle commands on the RobotTurtle "rt" object, such as...')
    print('    rt.forward(16)')
    print('    rt.right(90)')
    print('Try "help(rt)" for more information.')
else:
    print('To interact with the robot in interactive ("REPL") mode instead, invoke as follows...')
    print(f'   python3 -i {sys.argv[0]}')
