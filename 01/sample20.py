import asyncio


def task_generator(coro, loop):
    task = asyncio.Task(coro, loop=loop)
    return task


async def sleeper(n):
    await asyncio.sleep(n)
    print("slept {}".format(n))


loop = asyncio.get_event_loop()
task = task_generator(sleeper(1), loop=loop)
task2 = task_generator(sleeper(2), loop=loop)
task3 = task_generator(sleeper(3), loop=loop)
task3.cancel()
# ret1 = asyncio.wait_for(task, None)
# ret2 = asyncio.wait_for(task2, None)
# ret3 = asyncio.wait_for(task3, None)
# r = asyncio.wait([ret1, ret2])
# print(type(r))
# loop.run_until_complete(r)
loop.run_forever()
loop.close()
