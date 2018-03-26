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
host = os.getenv("PASSH_HOST")
log_path = os.getenv("PASSH_LOG_PATH")

_SSH = ('ssh', '-p', port, '-i', key_secret, '-T', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6')
_INSECURE_OPTS = (
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
)


class PAssh2(passh.PAssh):
    def __init__(self, hosts: list, args: list, *, infile=None, use_stdout: bool = False,
                 nprocs: int = 100, insecure=False):
        # pprint(passh._SSH)
        super().__init__(hosts, args)

    @asyncio.coroutine
    def _run1(self, host: str):
        exit_future = asyncio.Future(loop=self._loop)
        stdin = None
        if self._infile is not None:
            stdin = open(self._infile, 'rb')
            exit_future.add_done_callback(lambda x: stdin.close())
        cmd = list(_SSH)
        if self._secure:
            cmd.extend(_INSECURE_OPTS)
        cmd.append(host)
        cmd += self._args
        proc = self._loop.subprocess_exec(
            functools.partial(
                passh.PAsshProtocol, host, exit_future, self._use_stdout,
            ), *cmd, stdin=stdin)
        transport, protocol = yield from proc
        yield from exit_future
        transport.close()
        if transport.get_returncode() != 0:
            self._failures.append(host)
            return
        if self._use_stdout:
            self._outputs[host] = protocol.get_stdout()


args = ['tail -f ' + log_path]
p = PAssh2([user + "@" + host], args)
# pprint(vars(p))
p._loop.run_until_complete(p.wait())
