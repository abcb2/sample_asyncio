import asyncio


async def ping():
    print("ping", loop.time())
    await asyncio.sleep(2)
    await pong()


async def pong():
    print("pong", loop.time())
    await asyncio.sleep(2)
    await ping()


loop = asyncio.get_event_loop()
asyncio.ensure_future(ping())
loop.run_forever()
loop.close()
