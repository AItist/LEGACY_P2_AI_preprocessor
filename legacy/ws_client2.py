import asyncio
import websockets

async def receive_websocket_events():
    async with websockets.connect('ws://localhost:3000/websocket/websocket') as websocket:
        while True:
            event = await websocket.recv()
            print('Received event:', event)

asyncio.get_event_loop().run_until_complete(receive_websocket_events())
