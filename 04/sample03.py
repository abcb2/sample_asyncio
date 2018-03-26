import asyncio
import passh
import os
import logging
import functools
from os.path import exists
import sys
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
)

arg = 'tail -f ' + log_path
host = user + "@" + _host

cmd = list(passh._SSH)
cmd.extend(passh._INSECURE_OPTS)
cmd.append(host)
cmd += [arg]

# p = passh.PAssh([user + "@" + host], args)
# # pprint(vars(p))
# p._loop.run_until_complete(p.wait())

loop = asyncio.get_event_loop()
exit_future = asyncio.Future(loop=loop)

@asyncio.coroutine
def task1():
    use_stdout = False
    proc = loop.subprocess_exec(
        functools.partial(
            passh.PAsshProtocol, "-", exit_future, use_stdout,
        ), *cmd, stdin=None)
    transport, protocol = yield from proc
    print("---------------->")
    print(transport)
    print(protocol)
    print("----------------<")
    yield from exit_future
    print("Exit!!")
    transport.close()


async def task2():
    print("in task2")
    await asyncio.sleep(2)
    if True:
        print("oops")
        # task1.cancel()
        for task in asyncio.Task.all_tasks(loop):
            print(task)
    await task2()


tasks = [task1(), task2()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
