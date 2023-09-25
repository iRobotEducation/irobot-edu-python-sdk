#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

import argparse
import logging
from typing import Union
import sys


def bound(value: Union[int, float], low: Union[int, float], high: Union[int, float]) -> int:
    _value, _low, _high = int(value), int(low), int(high)
    return min(_high, max(_low, _value))


def stop_program():
    # Need to do something to catch the SystemExit exception.
    sys.exit()


# Returns True if running on a web (Pyodide) environment.
def is_web():
    return sys.platform == 'emscripten'


# Convenient argparse components for adding common command-line argument placeholders,
# for user to specify robot type, bluetooth, or serial. These values can then be used by an application.
# Suggested usage, in your code to make use of this:
#    parser = argparse.ArgumentParser(description='This is my program to interface with specified robots.',
#                                     parents=[utils.robot_backend_argument_parser], ...)  <= THIS 'parents' USAGE
#    parser.add_argument('--your-arg', ...)
#    ...
# Bluetooth-only is broken out for convenience as
#    parser = argparse.ArgumentParser(...
#                                     parents=[utils.robot_bluetooth_argument_parser], ...)  <= THIS 'parents' USAGE
# See additional example usage in 'examples_turtle' directory
SUPPORTED_ROBOTS = ('robot', 'generic', 'none', 'root', 'create3')
DEFAULT_ROBOT = SUPPORTED_ROBOTS[0]
robot_bluetooth_argument_parser = argparse.ArgumentParser(description='Bluetooth option: {}'.format(__name__),
                                                          add_help=False)

# This (arcane) construct accepts an "optional" `--bluetooth` argument.
# This can be specified as a flag like `--bluetooth` or with string like `--bluetooth ROBOT_NAME`
# See Python docs at https://docs.python.org/3/library/argparse.html#nargs near `nargs='?'` for more information
# => if --bluetooth not passed: args.bluetooth_name will be `None` (specified by `default=None`)
# => if "--bluetooth" (passed without argument) will be `''` (empty-string, specified by `const=''`)
# => if "--bluetooth FOO" (with argument value "FOO") passed, will be `'FOO'`
# The combination of all of this can be used to determine if and how to connect to a Robot.
robot_bluetooth_argument_parser.add_argument('--bluetooth', metavar='NAME', dest='bluetooth_name', required=False,
                                             default=None, nargs='?', const='',
                                             help='As a flag, open Bluetooth® connection to any available robot. With argument as `--bluetooth="..."` connect to specified robot by name.')

robot_backend_argument_parser = argparse.ArgumentParser(description='Backend options: {}'.format(__name__),
                                                        add_help=False,
                                                        parents=[robot_bluetooth_argument_parser])
robot_backend_argument_parser.add_argument('--robot-type', metavar='TYPE', dest='robot_type', required=False,
                                           default='robot', choices=SUPPORTED_ROBOTS,
                                           help=f'Connect to robot of specified type: {SUPPORTED_ROBOTS}')
robot_backend_argument_parser.add_argument('--serial', metavar='DEVICE', dest='serial_device', required=False,
                                           default=None,
                                           help='Use USB Serial connection: specify device such as /dev/ttyACM0')


# Some helper functions for common logging setup.
# The conventional `logging.basicConfig()` wreaks havoc and can make a lot of noise with library loggers,
# such as bleak and asyncio, when run at `DEBUG` level.
# This usage avoids that and repeated boilerplate code for args, formatter, and handler.
# Suggested usage, in your code to make use of this:
#    parser = argparse.ArgumentParser(description='This is my program that also uses logging.',
#                                     parents=[utils.log_level_argument_parser], ...)  <= THIS 'parents' USAGE
#    parser.add_argument('--your-arg', ...)
#    ...
#    args = parser.parse_args()
#    my_logger = utils.get_logger(__name__, args.log_level)
# Additional loggers can be retrieved either with utils.get_logger() or my_logger.getChild()
# Can be combined with robot_backend_argument_parser by adding to `parents=[...]` list.

# Default argument values
ROBOTLOG_BASE_LOGGER_NAME = 'RobotLog'
DEFAULT_LOG_LEVEL_NAME = 'INFO'
LOG_LEVEL_NAME_OPTIONS = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR']
DEFAULT_FORMAT_STRING = '%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s'
AUGMENTED_FORMAT_STRING = '%(levelname) -7s: %(asctime)sZ %(module)s.%(funcName)s:%(lineno)d %(message)s'


def get_logger(name, level=logging.INFO, format_string=AUGMENTED_FORMAT_STRING):
    """Set up a separable logger with usable defaults, or as additionally configured
    with specified parameters"""
    _base_logger = logging.getLogger(ROBOTLOG_BASE_LOGGER_NAME)
    if not _base_logger.handlers:
        # Create and populate Handler and Formatter if not already
        # This will be done effectively once on first import
        # Create a handler and populate its format
        ch = logging.StreamHandler(sys.stdout)
        _base_logger.addHandler(ch)
        formatter = logging.Formatter(format_string)
        _base_logger.handlers[0].setFormatter(formatter)
        _base_logger.debug('ROBOTLOG INIT: populating formatting for base logger %s', ROBOTLOG_BASE_LOGGER_NAME)
        _base_logger.debug("All loggers in the system: %s", logging.getLogger().manager.loggerDict.keys())
    logger = logging.getLogger(ROBOTLOG_BASE_LOGGER_NAME).getChild(name)
    # Set to requested level or a reasonable default of INFO; can be specified like logging.INFO or 'INFO'
    logger.setLevel(level)
    logger.debug("{}: Returning logger named {} at level {}".format(__name__, logger.name,
                                                                    logging.getLevelName(level) if isinstance(level, int) else level))
    return logger


log_level_argument_parser = argparse.ArgumentParser(description='Logging options: {}'.format(__name__),
                                                    add_help=False)
log_level_argument_parser.add_argument('--log', dest='log_level', metavar='LEVEL', required=False,
                                       choices=LOG_LEVEL_NAME_OPTIONS, default=DEFAULT_LOG_LEVEL_NAME,
                                       help='Set log level verbosity; options: {}'.format(LOG_LEVEL_NAME_OPTIONS))


if __name__ == '__main__':
    raise RuntimeError('{}: module not intended to be run as toplevel'.format(__file__))
