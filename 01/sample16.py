import asyncio
jfrom pprint import pprint


class RemoteTail():
    def __init__(self):
        self.rotate_flag = False


r = RemoteTail()


async def tailer(future):
    await asyncio.sleep(1)
    print(1)
    print("rotate_flag: ", r.rotate_flag)

    await asyncio.sleep(2)
    print(2)
    print("rotate_flag: ", r.rotate_flag)

    await asyncio.sleep(3)
    print(3)
    return await future


async def rotate_watcher(future):
    # loop.call_later(0.5, watcher, future)
    await asyncio.sleep(1.5)
    print("detect!!")
    detect_rotate(future)


def detect_rotate(future):
    r.rotate_flag = True
    future.set_result("rotated!!")


loop = asyncio.get_event_loop()
future = loop.create_future()
tasks = [tailer(future), rotate_watcher(future)]
loop.run_until_complete(asyncio.wait(tasks))
print(future.result())
loop.close()
