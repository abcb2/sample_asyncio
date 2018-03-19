import asyncio
from socket import socketpair
import time
from random import randint


def tf(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", t)


async def reader(r):
    data = r.read(100)
    print(data.decode())


async def writer(w):
    w.writer("Ping!".encode())


async def main():
    await asyncio.sleep(1)
    rsock, wsock = socketpair()

    _reader, _ = await asyncio.open_connection(sock=rsock, loop=loop)
    _, _writer = await asyncio.open_connection(sock=wsock, loop=loop)
    await reader(_reader)
    await writer(_writer)
    print("main: ", rsock)
    print("main: ", wsock)


# @asyncio.coroutine
# def wait_for_data(loop):
#     rsock, wsock = socketpair()
#
#     reader, writer = yield from asyncio.open_connection(sock=rsock, loop=loop)
#     loop.call_soon(wsock.send, "abc".encode())
#
#     data = yield from reader.read(100)
#
#     print("Received:", data.decode())
#     writer.close()
#
#     wsock.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# loop.run_until_complete(wait_for_data(loop))
loop.close()
