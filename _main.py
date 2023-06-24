import asyncio
from common.asyncioStack import AsyncioStack as asyncStack
from common.data_ import data_unpack_process, data_package_process
from common.enum_ import ePoses, eSegs

isDebug = True
poseFlag = ePoses.MEDIAPIPE
segFlag = eSegs.YOLO

stack = asyncStack() # 웹소켓으로 받은 데이터 저장용 스택
sendQueue = asyncio.Queue() # 가공 완료 데이터 전송용 큐

async def async_websocket():
    """
    비동기로 웹소켓 연결
    """
    import websockets
    
    debugCount = 0

    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                data = await websocket.recv()
                debugCount += 1
                await stack.push(data)

                # print(f"recv count : {debugCount}")

                # condition 쓰면 동기화됨..
                # async with condition:
                #     condition.notify_all()

                if sendQueue.qsize() > 0:
                    print('qsize : ', sendQueue.qsize())
                    for i in range(sendQueue.qsize()):
                        packet = await sendQueue.get()
                        await websocket.send(packet)

        except Exception as e:
            print(e)

async def async_detection():
    import json
    import time
    from common.detect_pose import async_detect_pose
    from common.detect_seg import async_detect_seg

    while True:
        # async with condition:
        #     # await condition.wait_for(lambda: queue.qsize() > 0)
        #     await condition.wait_for(lambda: stack.len() > 0)
        #     # data = await queue.get()
        #     data = await stack.pop()

        # await condition.wait_for(lambda: stack.len() > 0)
        # data = await stack.pop()
        await asyncio.sleep(0.005)

        # stack에 하나라도 없으면 continue
        if stack.len() < 1:
            continue

        # print(f'stack len : {stack.len()}')

        data = await stack.pop()
        await stack.clear()

        try:
            parsed_data = json.loads(data)
            # print(parsed_data)
            
            _data = data_unpack_process(parsed_data)

            start = time.time()
            pose_img, seg_img = await asyncio.gather(
                async_detect_pose(_data.copy(), poseFlag, debug=isDebug),
                async_detect_seg(_data.copy(), segFlag, debug=isDebug),
            )
            end = time.time()
            print(f"async check /detect time : {end - start}")

            if seg_img is not None:

                result_data = [_data[0], _data[1], seg_img, pose_img]

                packet = data_package_process(result_data)

                await sendQueue.put(packet)
                # print('qsize : ', sendQueue.qsize())

        except Exception as e:
            print(e)

        # print(f"async check /current /stacked {stack.len()}")
        # # print(f"async check /current {data} /stacked {stack.len()}")
        # await stack.clear()
        # print(f"async check /current /stacked {stack.len()}")
        # # print(f"async check /current {data} /stacked {stack.len()}")

        # # await asyncio.sleep(2)

async def main():
    coro1 = async_websocket()
    coro2 = async_detection()
    await asyncio.gather(
        coro1,
        coro2,
    )

asyncio.run(main())