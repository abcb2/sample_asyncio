import asyncio
from socket import socketpair
import time
from random import randint


def tf(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", t)


@asyncio.coroutine
def wait_for_data(loop):
    rsock, wsock = socketpair()

    reader, writer = yield from asyncio.open_connection(sock=rsock, loop=loop)
    loop.call_soon(wsock.send, "abc".encode())

    data = yield from reader.read(100)

    print("Received:", data.decode())
    writer.close()

    wsock.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(wait_for_data(loop))
loop.close()
