import asyncio
import os
import signal


async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
coro = hello_world()
print(type(coro))
print(asyncio.iscoroutine(coro))
loop.run_until_complete(coro)
loop.close()
