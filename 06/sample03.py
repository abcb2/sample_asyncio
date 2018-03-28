import asyncio
import logging
import passh
import functools
import re
from datetime import datetime as dt

logging.basicConfig(level=logging.DEBUG)


class TailProtocol(passh.PAsshProtocol):
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


class RotateWatchProtocol(passh.PAsshProtocol):
    def __init__(self, hostname: str,
                 exit_future: asyncio.Future, use_stdout: bool):
        super().__init__(hostname, exit_future, use_stdout)
        self.result = []

    def flush_line(self, buf: bytearray, out):
        pos = buf.rfind(b'\n')
        if pos == -1:
            return

        for line in buf[0:pos + 1].splitlines(True):
            if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.", line.decode('utf-8')):
                self.result.append(line.decode('utf-8'))
        out.flush()
        del buf[0:pos + 1]


class RemoteTail(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.task_list = []

        # need to configure targets
        targets = [
            {"host": "HOST", "port": "PORT", "user": "USER",
             "key_secret": "SECRET",
             "log_path": "/path/to/log",
             "out_path": "/path/to/log"},
        ]

        for t in targets:
            logging.warning(t)
            passh._SSH = (
                'ssh', '-t', '-t', '-p', t['port'], '-i',
                t['key_secret'], '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6'
            )
            passh._INSECURE_OPTS = (
                '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'IdentitiesOnly=yes'
            )

            cmd_tail = self._create_cmd(t, 'tail -f ')
            tail_task = asyncio.Task(self.tail(cmd_tail, t["host"], t["out_path"]), loop=self.loop)

            cmd_watch = self._create_cmd(t, 'stat -c %y ')
            asyncio.Task(self.watch(cmd_watch, tail_task, cmd_tail, t["host"], t["out_path"]), loop=self.loop)

    def _create_cmd(self, t, cmd_str):
        arg = cmd_str + t['log_path']
        host = t['user'] + "@" + t['host']
        cmd = list(passh._SSH)
        cmd.extend(passh._INSECURE_OPTS)
        cmd.append(host)
        cmd += [arg]
        return cmd

    def run(self):
        self.loop.run_forever()
        self.loop.close()

    async def watch(self, cmd, tail_task, cmd_tail, host, out_path, watch_interval=3.0, rotation_trigger_interval=900):
        await asyncio.sleep(watch_interval)
        logging.warning("WATCH")
        use_stdout = False
        exit_future = self.loop.create_future()
        proc = self.loop.subprocess_exec(
            functools.partial(
                RotateWatchProtocol, host, exit_future, use_stdout
            ), *cmd, stdin=None)
        transport, protocol = await proc
        await exit_future
        transport.close()
        logging.debug(protocol.result[0])
        logging.debug(type(protocol.result[0]))
        if len(protocol.result) == 1:
            m = re.search(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).+$", protocol.result[0])
            if m:
                stat_date = m.group(1)
                stat_date_dt = dt.strptime(stat_date, "%Y-%m-%d %H:%M:%S")
                now_dt = dt.now()
                delta = now_dt - stat_date_dt
                if delta.total_seconds() > rotation_trigger_interval:
                    logging.warning("Rotate!!! delta is {}".format(delta.total_seconds()))
                    tail_task.cancel()
                    tail_task = asyncio.Task(self.tail(cmd_tail, out_path), loop=self.loop)
                else:
                    logging.debug("Not Rotate: delta_total_sec is {}".format(delta.total_seconds()))
            else:
                logging.warning("RegexError: {}".format(protocol.result[0]))
        else:
            logging.warning("ResultNumError: {}".format(protocol.result))

        task = asyncio.Task(self.watch(cmd, tail_task, cmd_tail, host, out_path), loop=self.loop)

    async def tail(self, cmd, host, outputfile):
        use_stdout = False
        exit_future = self.loop.create_future()
        proc = self.loop.subprocess_exec(
            functools.partial(
                TailProtocol, host, exit_future, use_stdout, outputfile
            ), *cmd, stdin=None)
        transport, protocol = await proc
        await exit_future
        transport.close()


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
