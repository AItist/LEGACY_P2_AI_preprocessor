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

                # 이미지를 받을때 처리
                greeting = await websocket.recv()
                print(f"<<< {greeting}")

                # TODO: 이미지 처리 구간
                

                # 이미지를 보낼때 처리
                # await websocket.send("client send 이미지 처리 완료, 이미지 전달함")
                # print(f">>> 이미지 처리 완료, 이미지 전달함")
        except KeyboardInterrupt:
            # clean up resources here
            pass


async def main():
    await receive_stream_data()

if __name__ == "__main__":
    asyncio.run(main())