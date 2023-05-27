import asyncio

queue = asyncio.Queue()
condition = asyncio.Condition()

async def put_data_in_queue(queue, condition):
    for i in range(5):
        await asyncio.sleep(1)  # simulate some delay
        await queue.put(i)
        print(f'Produced: {i}')

        async with condition:  # Notify all tasks waiting for the condition that it has been met
            condition.notify_all()
    pass
    # import websockets

    # uri = "ws://localhost:8080"
    # async with websockets.connect(uri) as websocket:
    #     while True:
    #         data = await websocket.recv()
    #         await queue.put(data)

    #         print(f'recv list qsize: {queue.qsize()}')
    #         pass
    #     pass
    # pass

async def check_queue_size(queue, condition):
    while True:
        async with condition:
            await condition.wait_for(lambda: queue.qsize() > 0)
            # await condition.wait_for(lambda: queue.qsize() > 0 and check == False)
            print(f'Queue size is now greater than 1: {queue.qsize()}')
            
            data = await queue.get()
            print(f'Consumed: {data}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(put_data_in_queue(queue, condition), check_queue_size(queue, condition)))