import asyncio
import logging
import passh
import functools
import re
import os
import sys
import yaml
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
    def __init__(self, config):
        self.config = config
        self.loop = asyncio.get_event_loop()
        self.task_list = []

        for t in config['targets']:
            logging.warning(t)
            passh._SSH = (
                'ssh', '-t', '-t', '-p', t['port'], '-i',
                t['key_secret'], '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6'
            )
            passh._INSECURE_OPTS = (
                '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'IdentitiesOnly=yes'
            )

            cmd_tail = self._create_cmd(t, 'sudo tail -f ')
            tail_task = asyncio.Task(self.tail(cmd_tail, t["host"], t["out_path"]), loop=self.loop)

            # time of last data modification, human-readable, see: `man stat`
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

    def _extract_date(self, stat_date_str):
        m = re.search(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).+$", stat_date_str)
        if m:
            stat_date = m.group(1)
            stat_date_dt = dt.strptime(stat_date, "%Y-%m-%d %H:%M:%S")
            return stat_date_dt
        else:
            raise Exception("RegexError: {}".format(stat_date_str))

    async def watch(self, cmd, tail_task, cmd_tail, host, out_path, watch_interval=10.0, rotation_trigger_interval=125):
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
        # logging.debug(protocol.result[0])
        # logging.debug(type(protocol.result[0]))
        if len(protocol.result) == 1:
            try:
                """
                リモートのログがローテートしてもwatchタスクは都度SSHアクセスしているので
                リモートのログに書き込みが続く限りはmtimeは更新され続ける
                tailのためのSSHは張りっぱなしなので、リモートのログがローテートした場合は
                古いFileDescripterを読み続けてしまい、結果、ローカルにログの取り込みができない。
                故にlocalのmtimeはこうしんされない。
                ローカルのログのmtimeとリモートのログのmtimenのdeltaがしきい値を超えた場合、
                tailタスクをキャンセルして再度スケジュールし、SSHを貼り直す。
                """
                remote_log_dt = self._extract_date(protocol.result[0])
                local_log_dt = dt.fromtimestamp(os.stat(out_path).st_mtime)
                logging.warning("remote:{}, local:{}".format(
                    dt.strftime(remote_log_dt, "%Y-%m-%d %H:%M:%S"),
                    dt.strftime(local_log_dt, "%Y-%m-%d %H:%M:%S")
                ))
                delta = remote_log_dt - local_log_dt
                if delta.total_seconds() > rotation_trigger_interval:
                    tail_task.cancel()
                    tail_task = asyncio.Task(self.tail(cmd_tail, host, out_path), loop=self.loop)
                else:
                    logging.warning("Not Rotate: delta_total_sec is {}:{}".format(out_path, delta.total_seconds()))
            except Exception as e:
                logging.exception(e)
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


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise Exception("need config_file arg, `python remote_tail.py config/hoge.yml`")

        config_path = sys.argv[1]
        if not os.path.exists(config_path):
            raise Exception("does not exist {}".format(config_path))
        with open(config_path) as f:
            config = yaml.load(f)
        r = RemoteTail(config)
        r.run()
    except KeyboardInterrupt as e:
        r.loop.close()
        # print("KeyboardInterrupt")
        # r.task_tail.cancel()
        # r.exit_future.set_result(True)
        # # print(r.tasks)
        # # r.tasks.cancel()
        # r.loop.close()
