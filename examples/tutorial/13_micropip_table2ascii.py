#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021 iRobot Corporation. All rights reserved.
#

# This example only runs on the web version of the iRobot Edu SDK.

# Do not auto-format: the order of these 3 lines is important and autoformatting may change it.
import micropip
await micropip.install('table2ascii')
from table2ascii import table2ascii


rt0 = 1
rt1 = 3
c3 = 2
output = table2ascii(
    header=['Model:', 'rt0', 'rt1', 'C3'],
    body=[['', rt0, rt1, c3], ['', 2*rt0, 2*rt1, 2*c3]],
    footer=['Total:', rt0+2*rt0, rt1+2*rt1, c3+2*c3],
)

print(output)
