import asyncio

async def async_loop():
    while True:
        print("async loop")
        await asyncio.sleep(1)

async def async_count_loop():
    count = 0
    while True:
        count += 1
        print(f"async count loop number {count}")
        await asyncio.sleep(2)

async def main():
    coro1 = async_loop()
    coro2 = async_count_loop()
    await asyncio.gather(
        coro1,
        coro2,
    )

asyncio.run(main())