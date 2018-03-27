import asyncio
import logging
import passh
import os
import functools
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

port = os.getenv('PASSH_PORT')
key_secret = os.getenv('PASSH_KEY')
user = os.getenv('PASSH_USER')
_host = os.getenv("PASSH_HOST")
log_path = os.getenv("PASSH_LOG_PATH")

passh._SSH = ('ssh', '-p', port, '-i', key_secret, '-T', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6')
passh._INSECURE_OPTS = (
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
    '-o', 'IdentitiesOnly=yes'
)

logging.warning("PORT:{}\nKEY:{}\nUSER:{}\nHOST:{}\nLOG:{}\n".format(
    port, key_secret, user, _host, log_path
))

arg = 'sudo tail -f ' + log_path
host = user + "@" + _host

cmd = list(passh._SSH)
cmd.extend(passh._INSECURE_OPTS)
cmd.append(host)
cmd += [arg]


class RemoteTail(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.task_tail = asyncio.Task(self.tail(), loop=self.loop)
        self.task_watch = asyncio.Task(self.watch(), loop=self.loop)

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

    async def tail(self):
        use_stdout = False
        exit_future = self.loop.create_future()
        proc = self.loop.subprocess_exec(
            functools.partial(
                passh.PAsshProtocol, _host, exit_future, use_stdout,
            ), *cmd, stdin=None)
        transport, protocol = await proc
        logging.warning("---------------->")
        logging.warning(transport)
        logging.warning(protocol)
        logging.warning("----------------<")
        await exit_future
        transport.close()

    async def tail_bak(self):
        print("Start tail")
        for n in range(1, 5):
            await asyncio.sleep(n)
            print("slept {}".format(n))


r = RemoteTail()
r.run()
