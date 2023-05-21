import asyncio
import time

async def make_request(num):
    # Simulate a network request with asyncio.sleep
    await asyncio.sleep(1)
    print(f'Request {num} completed')

async def main():
    # Start time
    start = time.time()

    # Create a list of tasks
    tasks = [make_request(i) for i in range(10)]

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

    # End time
    end = time.time()

    print(f'Time taken: {end-start} seconds')

# Run the async main function until completion
asyncio.run(main())
