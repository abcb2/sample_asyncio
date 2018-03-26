import asyncio
from pprint import pprint


class RemoteTail():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.rotate_flag = False
        self.futures = set()
        self.future = self.loop.create_future()
        self.future.add_done_callback(self.tail())

    def run(self):
        self.loop.run_until_complete(asyncio.wait([self._run()]))
        self.loop.close()

    async def _run(self):
        await self.tail()
        await self.watch_rotate()
        await self.future

    async def tail(self):
        if self.future.done():
            self.future = self.loop.create_future()
        print("Start tail")
        await asyncio.sleep(1.0)
        print(1.0)
        # await asyncio.sleep(3.0)
        # print(3.0)

        if self.future.done():
            print("----------------->")
            print(self.future.result())
        else:
            print("=================>")
            print("not done")

    async def watch_rotate(self):
        await asyncio.sleep(1.5)
        print("detect!!")
        self.rotate_flag = True
        self.future.set_result("set result to future")


r = RemoteTail()
r.run()

# async def rotate_watcher():
#     future = loop.create_future()
#     await asyncio.sleep(1.5)
#     print("detect!!")
#     detect_rotate(future)
#
#
# def detect_rotate(future):
#     r.rotate_flag = True
#     future.set_result("rotated!!")
#
#
# def create_future():
#     return asyncio.Future()


# loop = asyncio.get_event_loop()
# tasks = [r.run()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
