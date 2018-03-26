import asyncio
import functools
from pprint import pprint


def hoge(f):
    print("hoge")
    f.set_result("yes")


loop = asyncio.get_event_loop()


async def moge(future=None):
    print("FUTURE: {}".format(future))
    if future is None:
        print("====")
        future = asyncio.Future(loop=loop)
    if future.done() is True:
        print("-----")
        future = asyncio.Future(loop=loop)
    await asyncio.sleep(1.5)
    print("yes here")
    future.add_done_callback(_my_call_back)
    # future.add_done_callback(moge)
    await asyncio.sleep(1)
    print("yes here2")
    future.set_result("done")
    print("yes here3")


def _my_call_back(future):
    print(future)
    print(future.done())
    print(future.result())
    print("oops")
    asyncio.gather(moge())
    print(futures)


async def watcher():
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print("FIN")


futures = set()
futures.add(moge())
futures.add(watcher())
print(futures)

loop.run_until_complete(asyncio.gather(moge(), watcher()))
loop.close()
