#!/usr/bin/env python

import asyncio
import websockets

async def receive_stream_data():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        count = 0
        while count < 10:

            await websocket.send("Hello, server!")
            print(f">>> Hello, server!")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")

            count += 1

async def main():
    await receive_stream_data()

if __name__ == "__main__":
    asyncio.run(main())