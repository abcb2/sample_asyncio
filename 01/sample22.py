import asyncio
import passh
from pprint import pprint


class RemoteTail():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.task_tail = asyncio.Task(self.tail(), loop=self.loop)
        self.task_watch = asyncio.Task(self.watch(), loop=self.loop)

    def run(self):
        self.loop.run_forever()
        self.loop.close()

    async def watch(self):
        print("Start watch")
        await asyncio.sleep(2.5)
        detect_flag = True

        if detect_flag and self.task_tail.cancel():
            self.task_tail = asyncio.Task(self.tail(), loop=self.loop)

        self.task_watch = asyncio.Task(self.watch(), loop=self.loop)

    async def tail(self):
        print("Start tail")
        for n in range(1, 5):
            await asyncio.sleep(n)
            print("slept {}".format(n))


r = RemoteTail()
r.run()
