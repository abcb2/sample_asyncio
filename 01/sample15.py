import asyncio
from pprint import pprint


async def my_count(id_, n):
    for i in range(n):
        print("ID: {}, {}".format(id_, i))
        await asyncio.sleep(0.2)
    print("FINISH {}".format(id_))


async def canceler():
    await asyncio.sleep(0.5)
    for t in asyncio.Task.all_tasks(loop):
        # pprint(t)
        t.cancel()


loop = asyncio.get_event_loop()
futures = []

for i in range(5):
    futures.append(my_count(i, 5))
futures.append(canceler())

try:
    loop.run_until_complete(asyncio.wait(futures))
except asyncio.CancelledError:
    print("OOPS")
loop.close()
