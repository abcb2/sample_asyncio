import asyncio
from pprint import pprint


class RemoteTail():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.task_tail = asyncio.Task(self.tail(), loop=self.loop)
        self.task_watcher = asyncio.Task(self.watch(), loop=self.loop)
        # self.rotate_flag = False
        # self.futures = set()
        # self.future = self.loop.create_future()
        # self.future.add_done_callback(self.tail())

    def run(self):
        # self.loop.run_until_complete(asyncio.wait([self._run()]))
        # ret = asyncio.wait([self._run()])
        # print(ret)

        self.loop.run_forever()
        self.loop.close()

    async def _run(self):
        await self.tail()
        await self.watch_rotate()
        await self.future

    async def watch(self):
        print("Start watch")
        await asyncio.sleep(2.5)
        detect_flag = True

        if detect_flag and self.task_tail.cancel():
            self.task_tail = asyncio.Task(self.tail(), loop=self.loop)

        self.task_watcher = asyncio.Task(self.watch(), loop=self.loop)

    async def tail(self):
        print("Start tail")
        for n in range(1, 5):
            await asyncio.sleep(n)
            print("slept {}".format(n))

    async def _tail(self):
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
