import asyncio
import logging
import passh
import os
import functools
import signal
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

port = os.getenv('PASSH_PORT')
key_secret = os.getenv('PASSH_KEY')
user = os.getenv('PASSH_USER')
_host = os.getenv("PASSH_HOST")
log_path = os.getenv("PASSH_LOG_PATH")
out_path = "./moge2.txt"

targets = [
    {"host": _host, "port": port, "user": user, "key_secret": key_secret, "log_path": log_path, "out_path": out_path},
]

logging.warning("PORT:{}\nKEY:{}\nUSER:{}\nHOST:{}\nLOG:{}\n".format(
    port, key_secret, user, _host, log_path
))


class MyPAsshProtocol(passh.PAsshProtocol):
    def __init__(self, hostname: str,
                 exit_future: asyncio.Future, use_stdout: bool, outputfile: str):
        super().__init__(hostname, exit_future, use_stdout)
        self.outputfile = outputfile

    def flush_line(self, buf: bytearray, out):
        # out = open("./hoge.txt", "a")
        out = open(self.outputfile, "a")
        self._prefix = ""
        pos = buf.rfind(b'\n')
        if pos == -1:
            return
        b = bytearray()
        for line in buf[0:pos + 1].splitlines(True):
            b.extend(self._prefix)
            b.extend(line)
            # out.write(b)
            out.write(b.decode('utf-8'))
            b.clear()
        out.flush()
        del buf[0:pos + 1]
        out.close()


class RemoteTail(object):
    passh._SSH = ('ssh', '-t', '-p', port, '-i', key_secret, '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6')
    passh._INSECURE_OPTS = (
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'IdentitiesOnly=yes'
    )

    def __init__(self):
        cmd = self._create_cmd()
        outputfile = "moge.txt"
        logging.warning("{}, {}".format(cmd, outputfile))

        self.loop = asyncio.get_event_loop()
        self.task_tail = asyncio.Task(self.tail(cmd, outputfile), loop=self.loop)
        self.task_watch = asyncio.Task(self.watch(), loop=self.loop)
        self.exit_future = self.loop.create_future()

    def _create_cmd(self):
        arg = 'tail -f ' + log_path
        host = user + "@" + _host
        cmd = list(passh._SSH)
        cmd.extend(passh._INSECURE_OPTS)
        cmd.append(host)
        cmd += [arg]
        return cmd

    def run(self):
        self.loop.run_forever()
        self.loop.close()

    async def watch(self):
        logging.info("Start watch")
        await asyncio.sleep(2.5)
        detect_flag = True

        if detect_flag and self.task_tail.cancel():
            self.task_tail = asyncio.Task(self.tail(), loop=self.loop)

        self.task_watch = asyncio.Task(self.watch(), loop=self.loop)

    async def tail(self, cmd, outputfile):
        use_stdout = False
        proc = self.loop.subprocess_exec(
            functools.partial(
                MyPAsshProtocol, _host, self.exit_future, use_stdout, outputfile
            ), *cmd, stdin=None)
        transport, protocol = await proc
        await self.exit_future
        transport.close()

    async def tail_bak(self):
        print("Start tail")
        for n in range(1, 5):
            await asyncio.sleep(n)
            print("slept {}".format(n))


try:
    r = RemoteTail()
    r.run()
except KeyboardInterrupt as e:
    r.loop.close()
    # print("KeyboardInterrupt")
    # r.task_tail.cancel()
    # r.exit_future.set_result(True)
    # # print(r.tasks)
    # # r.tasks.cancel()
    # r.loop.close()
