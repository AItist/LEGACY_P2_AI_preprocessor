import asyncio

class AsyncClass:
    async def async_method(self):
        await asyncio.sleep(1)  # This could be any async operation
        print("Async method completed")

# Usage:
async def main():
    async_instance = AsyncClass()
    asyncio.Task(async_instance.async_method())

# Run the async main function until completion
if __name__ == '__main__':  # Python 3.7+
    asyncio.run(main())
    print('hello')
