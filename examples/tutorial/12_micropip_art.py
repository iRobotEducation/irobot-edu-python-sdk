#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2021-2022 iRobot Corporation. All rights reserved.
#

# This example only runs on the web version of the iRobot Edu SDK.
# It shows how to import a Python package from https://pypi.org/.
# One of the great things about Python, is that here are a lot packages that can be imported used in your programs.
#
# micropip will allow you to explore many of them in this Python Web Playtround!
#
# IMPORTANT: The packages that can be imported are pure-Python ones.
#            This means that they must not include native code written in C (or other languages).


# Do not auto-format: the order of these 2 lines is important and autoformatting may change it.
import micropip
await micropip.install('art') # Intalls the ASCII Art library from https://pypi.org/project/art/

# Can also specify full URL to wheel:
# await micropip.install("https://files.pythonhosted.org/packages/b5/7c/c97aba89a6c50766becfcc715edcae3ac6f78b90548a4efcb73f6901adee/art-5.3-py2.py3-none-any.whl")

import art
print(art.text2art('Robots!'))
