#!/usr/bin/env python3
#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2023 iRobot Corporation. All rights reserved.
#

# This is a simple example using the Turtle interface to a iRobot EDU Robot via Bluetooth.
# By default, set the pen down, move in a 16 cm-edged pentagon, then lift the pen up.
# Pen actions are harmlessly ignored if not supported by the target robot.
# Other polygons could be drawn by changing the constants below or using command-line options

import argparse
from dataclasses import dataclass

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import Root
from irobot_edu_sdk.robot_turtle import RobotTurtle
from irobot_edu_sdk import utils

# Default parameters for drawing the polygon -- regular pentagon with 16 cm edges
# USE COMMAND-LINE ARGUMENTS --num-sides NUM and --edge-length LEN to adjust, or see --help for information
# OR EDIT THESE TWO LINES to change the size and number of sides of the polygon!
DEFAULT_NUM_SIDES = 5
DEFAULT_EDGE_LENGTH = 16


@dataclass()
class _MyArgs:
    """Typed container for args namespace"""
    bluetooth_name: str = None
    num_sides: int = DEFAULT_NUM_SIDES
    edge_length: int = DEFAULT_EDGE_LENGTH


# Retrieve arguments; see --help for more information
my_args = _MyArgs()
parser = argparse.ArgumentParser(description='iRobot EDU Turtle interface polygon drawing',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 parents=[utils.robot_bluetooth_argument_parser])
parser.add_argument('--num-sides', '--sides', metavar='NUMBER', dest='num_sides',
                    required=False, type=int, default=DEFAULT_NUM_SIDES,
                    help='Number of sides to polygon movement')
parser.add_argument('--edge-length', '--length', metavar='CENTIMETERS', dest='edge_length',
                    required=False, type=int, default=DEFAULT_EDGE_LENGTH,
                    help='Length of each edge of polygon movement')
parser.parse_args(namespace=my_args)

# Use the above constants to draw the shape.
# Create and start the interface to the robot
if my_args.bluetooth_name:
    backend = Bluetooth(my_args.bluetooth_name)
else:
    backend = Bluetooth()
robot = Root(backend)  # connect to first of any robot type detected
print('Attempting to connect to robot; please wait (this may take several seconds)...')
rt = RobotTurtle(robot)

# Calculate the turning angle based on number-of-sides.
outer_angle = 360 / my_args.num_sides

print(f'Drawing regular polygon with {my_args.num_sides} sides, each {my_args.edge_length} cm long, with angle {outer_angle}')

rt.pendown()
for ii in range(my_args.num_sides):
    rt.forward(my_args.edge_length)
    rt.right(outer_angle)
rt.penup()

rt.stop()
