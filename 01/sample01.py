import asyncio


def hello_world(loop):
    print("hello world")
    loop.stop()


loop = asyncio.get_event_loop()
loop.call_soon(hello_world, loop)
loop.run_forever()
loop.close()
