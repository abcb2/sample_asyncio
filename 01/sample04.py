import asyncio
import os
import signal
import time


def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()


def eternal_hello():
    print("hello!")
    loop.call_soon(eternal_hello)


loop = asyncio.get_event_loop()
loop.call_soon(eternal_hello)

for signame in ("SIGINT", "SIGTERM"):
    signal_enum = getattr(signal, signame)
    loop.add_signal_handler(signal_enum, ask_exit, signame)
print("Event loop running forever, press Ctrl+C to interrupt.")
print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())

try:
    loop.run_forever()
finally:
    loop.close()
