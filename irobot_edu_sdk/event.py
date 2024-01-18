#
# Licensed under 3-Clause BSD license available in the License file. Copyright (c) 2020-2024 iRobot Corporation. All rights reserved.
#

# TODO: Make this a conditional import on {microprocessor python}_functools once this function is supported
try:
    from functools import wraps
except ImportError:
    def wraps(wrapped, assigned=None, updated=None):
        return wrapped

try:
    import asyncio
except ImportError:
    import uasyncio as asyncio


async def hand_over():
    # Python idiomatic way of yielding control from a coroutine.
    # See https://github.com/python/asyncio/issues/284
    await asyncio.sleep(0)


class Event:
    """ This class will be used for robots other than Root, thus the naming """

    def __init__(self, condition, task):
        self.condition = condition
        self.task = task
        self.is_running = False
        # self.prev_data = None  # can be used for filtering while triggering if needed

    async def run(self, device):
        if not self.is_running:
            self.is_running = True
            await self.task(device)
            self.is_running = False


def event(method, condition=None):
    """ Convienience decorator that allows to define any function as a device event with the syntax:
        `@event(device.method, condition)`
    """
    def decorator_event(func):
        if condition != None:
            method(condition, func)
        else:
            method(func)

        @wraps(func)
        def wrapper_event(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper_event
    return decorator_event
