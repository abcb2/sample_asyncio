import asyncio


def hello_world():
    print("hello world")
    loop = asyncio.get_event_loop()
    loop.stop()


loop = asyncio.get_event_loop()
loop.call_soon(hello_world)
loop.run_forever()
loop.close()
