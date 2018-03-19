import asyncio
from socket import socketpair
import time
from random import randint

rsock1, wsock1 = socketpair()
loop = asyncio.get_event_loop()


def tf(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", t)


def reader():
    data = rsock1.recv(100)
    if data.decode() == "Ping!":
        print(tf(time.gmtime()), "\t", "Pong!")
        print("---------------")


def sender(mess="Ping!"):
    print(tf(time.gmtime()), "\t", mess)
    wsock1.send(mess.encode())
    loop.call_later(randint(2, 5), sender)


loop.add_reader(rsock1, reader)
loop.call_later(1, sender)
loop.run_forever()
