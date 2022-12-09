#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

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
