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

passh._SSH = ('ssh', '-p', port, '-i', key_secret, '-T', '-o', 'LogLevel=ERROR', '-o', 'ConnectTimeout=6')
passh._INSECURE_OPTS = (
    '-o', 'StrictHostKeyChecking=no',
    '-o', 'UserKnownHostsFile=/dev/null',
)

args = ['tail -f ' + log_path]
p = passh.PAssh([user + "@" + host], args)
# pprint(vars(p))
p._loop.run_until_complete(p.wait())
