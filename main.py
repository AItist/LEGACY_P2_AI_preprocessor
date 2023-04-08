#!/usr/bin/env python

import asyncio
import websockets

async def receive_stream_data():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                # await websocket.send("Hello, server!")
                # print(f">>> Hello, server!")

                greeting = await websocket.recv()
                print(f"<<< {greeting}")
        except KeyboardInterrupt:
            # clean up resources here
            pass


async def main():
    await receive_stream_data()

if __name__ == "__main__":
    asyncio.run(main())