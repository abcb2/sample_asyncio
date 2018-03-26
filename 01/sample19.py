import asyncio
import functools
from pprint import pprint


async def hoge():
    print("yes")
    await asyncio.sleep(1)
    print("yes2")
    await asyncio.sleep(2)
    print("yes3")
    return 10


async def moge(task):
    print("oops")
    await asyncio.sleep(2)
    print("oops2")
    ret = task.cancel()
    print(ret)
    print("oops3")


loop = asyncio.get_event_loop()
coro = hoge();
task = asyncio.Task(coro, loop=loop)

loop.run_until_complete(asyncio.wait([task, moge(task)]))
loop.close()
