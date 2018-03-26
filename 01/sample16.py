import asyncio
from pprint import pprint


async def myfuture():
    future = loop.create_future()
    # do something
    result = "yes"
    loop.call_later(2, future.set_result, result)
    return (await future)


async def myfuture2():
    await asyncio.sleep(2)


loop = asyncio.get_event_loop()
f = myfuture2()
print(f)
l = loop.run_until_complete(asyncio.wait([f]))
print(l)
print(f)
loop.close()
