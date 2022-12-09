#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2022 iRobot Corporation. All rights reserved.
#

try:
    from asyncio import sleep
    from time import time
    from typing import Any, Optional
except ImportError:
    from uasyncio import sleep
    from utime import time


class Completer():
    def __init__(self):
        self.clear()

    def clear(self):
        self._flag = False
        self._data = None

    async def wait(self, timeout: Optional[int] = None) -> Optional[Any]:
        start = int(time())
        while not self._flag:
            if timeout and int(time()) - start > timeout:
                break
            await sleep(0)
        return self.value()

    def is_complete(self) -> bool:
        return self._flag

    def complete(self, data=None):
        self._flag = True
        self._data = data

    def value(self) -> Optional[Any]:
        return self._data
