# iRobot® Education Python® SDK

This is an installable Python SDK for the iRobot Education robots.
It supports the iRobot® Root® rt0, Root® rt1 and Create® 3 educational robots.

This SDK uses a similar format as Learning Level 3 of the iRobot® Coding App ([code.irobot.com](https://code.irobot.com)) and the iRobot® Python Web Playground ([python.irobot.com](https://python.irobot.com)).
As such, it uses async execution and is compatible with Python® 3.9 or greater. MicroPython may work, but it is not tested.

This SDK is designed to communicate with robots via Bluetooth® Low Energy on Windows®, macOS®, and Linux® systems.
Experimental backends are provided for communicating over USB serial and USB on MicroPython boards with native USB ports.
These are not currently supported.

## Disclaimer: this is a BETA release.
The BETA version of the iRobot® Python SDK is provided “as is” to conduct testing and gather user feedback. There is no guarantee on its performance or compatibility, continued availability, or on a timeline for improvements.

Please do file [issues](https://github.com/iRobotEducation/irobot-edu-python-sdk/issues) as they are found, so that the team (or the community) can address them.


## Installation using pip

```
pip3 install irobot_edu_sdk
```


## Optional: Installation from Source

```
git clone https://github.com/iRobotEducation/irobot-edu-python-sdk.git
```

From the newly cloned SDK's directory, run:

```
pip3 install .
```


## Usage

A robot object is created from one of the communication backends.
This robot object has a number of event callbacks that can be registered and commands that can be sent to the robot.
After a program is setup, the `play()` method will start execution and block until the robot's nose or power button is pressed, the robot is disconnected, or `Ctrl-C` is pressed.


## Examples

A good way of getting started is by looking at the examples provided [here](https://github.com/iRobotEducation/irobot-edu-python-sdk/tree/main/examples).

These examples mirror the iRobot Education [Python Web Playground](http://python.irobot.com).

## Backend

### Bluetooth

iRobot Education's robots communicate using a common Bluetooth Low Energy serial protocol, the details of which can be found [here](https://github.com/iRobotEducation/root-robot-ble-protocol).

```python
from irobot_edu_sdk.backend.bluetooth import Bluetooth

# Connect to robot over Bluetooth Low Energy.
backend0 = Bluetooth('') # Connects to the first BLE robot detected.
backend1 = Bluetooth('ROOT') # Use robot named 'ROOT'
```

## ALPHA features
**The features detailed below are included as ALPHA versions, which provide limited functionality and are likely to contain several known or unknown bugs.**
**Support is not provided for ALPHA features at this time.**

### Serial

Some Root® robots support a serial port over USB.
This feature is currently not available on Create® 3 robots.

```python
from irobot_edu_sdk.backend.serial import Serial

# Connect to robot over USB-C cable.
backend = Serial('COM1')                          # Windows
backend = Serial('/dev/cu.usbmodemRT0123F456789') # macOS
backend = Serial('/dev/ttyACM0')                  # Linux
```

### MicroPython

This SDK requires MicroPython firmware that includes the `uasyncio` library -- version 1.13 or greater.
Download the latest release for your board from http://micropython.org/download.
Then, copy the `irobot_edu_sdk` directory and all contents to the `PYBFLASH` drive.

```python
from irobot_edu_sdk.backend.usb import USB

# Connect to robot from MicroPython-compatible board over USB.
backend = USB() # MicroPython-compatible board is powered from USB-C port
```

NOTE: You may need to use a USB-C to USB-A adapter or a USB-C to micro USB cable.

### Turtle programming model

This portion of the SDK provides an alternative programming interface to the SDK following the paradigm of 
[turtle graphics](https://en.wikipedia.org/wiki/Turtle_graphics).
It provides a limited, simplified, and synchronous interface to the in the spirit (and largely the syntax) of the 
[Python® turtle.Turtle class](https://docs.python.org/3/library/turtle.html).
It can be used on any robot supported by the SDK, using any supported backend. See the `README.md` file and other
example files in the `examples_turtle/` directory for more information.

## Additional information

**© 2022-2023 iRobot Corporation. All rights reserved.**
* [Terms and Conditions](https://about.irobot.com/en-us/legal/terms-and-conditions)
* [Privacy Policy](https://edu.irobot.com/privacy-policy)

## Attributions
* Python® 3 is governed by and a trademark of the Python Software Foundation.
* The Bluetooth® word mark and logos are registered trademarks owned by Bluetooth SIG, Inc. and any use of such marks by iRobot is under license.
* Windows® is a trademark of Microsoft Corporation, registered in the U.S. and other countries and regions.
* macOS® is a trademark of Apple Inc., registered in the U.S. and other countries and regions.
* Linux® is a trademark of Linus Torvalds, registered in the U.S. and other countries and regions.
* USB-C™ is a trademark of USB Implementers Forum.
* All other trademarks mentioned are the property of their respective owners.


This library is made possible thanks to other community software.
The following are direct required dependencies:
* [Bleak](https://github.com/hbldh/bleak), licensed under the MIT license, available [here](https://github.com/hbldh/bleak/blob/develop/LICENSE)
* [pySerial](https://github.com/pyserial/pyserial/), licensed under the BSD 3-Clause license, available [here](https://github.com/pyserial/pyserial/blob/master/LICENSE.txt)
* [Root Robot Python Web App](https://github.com/mogenson/root-robot-python-web-app), licensed under the MIT license, available [here](https://github.com/mogenson/root-robot-python-web-app/blob/main/LICENSE)

To build, the following is recommended:
* [Poetry](https://github.com/python-poetry/poetry), licensed under the MIT license, available [here](https://github.com/python-poetry/poetry/blob/master/LICENSE)

The iRobot Education Python SDK provided is licensed under the 3-Clause BSD license, found [here](https://github.com/iRobotEducation/irobot-edu-python-sdk/tree/main/LICENSE.txt)
