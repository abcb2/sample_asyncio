import asyncio


async def main():
    await asyncio.sleep(1)
    await moge()


async def moge():
    print("hoge")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
