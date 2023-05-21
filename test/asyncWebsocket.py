import asyncio
import websockets

class Processor:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.condition = asyncio.Condition()

    async def process(self):
        async with self.condition:
            await self.condition.wait_for(lambda: self.queue.qsize() > 0)
            data = await self.queue.get()
        # Process your data here. This is your func function.
        processed_data = data * 2  # Simple processing for the example
        return processed_data

    async def consume(self, websocket):
        async for data in websocket:
            # Receive data from the websocket and add it to our queue
            await self.queue.put(int(data))

            # Notify all tasks waiting for the condition that it has been met
            async with self.condition:
                self.condition.notify_all()

    async def produce(self, websocket):
        while True:
            # Process the data from the queue
            processed_data = await self.process()

            # Send the processed data to the websocket
            await websocket.send(str(processed_data))

    async def websocket_handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.consume(websocket))
        producer_task = asyncio.ensure_future(self.produce(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

start_server = websockets.serve(Processor().websocket_handler, 'localhost', 8765)

asyncio.run(start_server)
