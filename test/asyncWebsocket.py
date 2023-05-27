import asyncio
import websockets

class Processor:
    """
    데이터 처리를 관리하는 클래스
    self.queue: 데이터를 저장하는 asyncio Queue가 있습니다.
    """
    def __init__(self):
        self.queue = asyncio.Queue()
        self.condition = asyncio.Condition()

    async def process(self):
        """
        큐에 항목이 하나 이상 있을 때까지 기다린 다음 처리하는 비동기 메서드입니다.
        이 간단한 예에서는 데이터에 2를 곱합니다.
        """
        async with self.condition:
            await self.condition.wait_for(lambda: self.queue.qsize() > 0)
            data = await self.queue.get()
        # Process your data here. This is your func function.
        processed_data = data * 2  # Simple processing for the example
        return processed_data

    async def consume(self, websocket):
        """
        websocket에서 데이터를 수신하고 대기열에 추가하는 비동기 메서드.
        새로운 데이터가 추가될 때마다 대기중인 모든 작업에 self.condition으로 알립니다.
        """
        async for data in websocket:
            # Receive data from the websocket and add it to our queue
            await self.queue.put(int(data))

            # Notify all tasks waiting for the condition that it has been met
            async with self.condition:
                self.condition.notify_all()

    async def produce(self, websocket):
        """
        큐에서 데이터를 처리하고 다시 websocket으로 보내는 비동기 메서드.
        """
        while True:
            # Process the data from the queue
            processed_data = await self.process()

            # Send the processed data to the websocket
            await websocket.send(str(processed_data))

    async def websocket_handler(self, websocket, path):
        """
        소비자 및 생산자 작업을 시작하고 그 중 하나가 완료될 때까지 기다리는 비동기 메서드입니다.
        하나의 작업이 완료되면(예: websocket이 닫힌 경우) 다른 작업을 취소합니다.
        """
        consumer_task = asyncio.ensure_future(self.consume(websocket))
        producer_task = asyncio.ensure_future(self.produce(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

# 이 코드는 localhost 포트 8765에서 서버를 시작합니다.
# 연결된 WebSocket 클라이언트에서 데이터를 수신하고 데이터를 처리한 다음 다시 보냅니다.

# 이것은 매우 간단한 예입니다. 프로덕션 환경에서 오류 처리 및 로그인을 추가해야 할 수 있습니다.
# `process()` 또한 처리 방식을 실제 데이터 처리 코드로 바꿔야 합니다.
start_server = websockets.serve(Processor().websocket_handler, 'localhost', 8765)

asyncio.run(start_server)
