#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2022 iRobot Corporation. All rights reserved.
#

import sys
if 'pyodide' in sys.modules:
    from irobot_edu_sdk.backend.bluetooth_web import Bluetooth
else:
    from irobot_edu_sdk.backend.bluetooth_desktop import Bluetooth
