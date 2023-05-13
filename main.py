#!/usr/bin/env python

import asyncio
import websockets
import json

async def async_show(data):
    import cv2
    await asyncio.sleep(0.005)
    cv2.imshow(f'Webcam {data[0]}', data[2])
    del data

async def write_img(data):
    import cv2
    await asyncio.sleep(0.005)
    cv2.imwrite(f'webcam {data[0]}.jpg', data[2])
    del data

def data_unpack_process(data):
    import base64
    import gzip
    import numpy as np

    index = data['index']
    ret = data['ret']
    compressed_frame = data['frame']

    decoded_frame = base64.b64decode(compressed_frame.encode('utf-8'))
    # print(decoded_frame)

    decompressed_frame = gzip.decompress(decoded_frame)
    # print(decompressed_frame)

    restored_frame = np.frombuffer(decompressed_frame, dtype=np.uint8)
    # print(restored_frame.shape)

    height, width, channels = 480, 640, 3
    reshaped_frame = np.reshape(restored_frame, (height, width, channels))
    # print(reshapd_frame.shape)

    data = [index, ret, reshaped_frame]

    return data

    # print(data)
    # del data
    pass

async def detect_img(data):

    return 'result is here'


async def receive_stream_data(ys):
    import cv2
    import base64
    import numpy as np

    import gzip

    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                # await websocket.send("Hello, server!")
                # print(f">>> Hello, server!")

                # 이미지를 받을때 처리
                data = await websocket.recv()
                # print(data)

                # 이미지 처리
                try:
                    parsed_data = json.loads(data)

                    data = data_unpack_process(parsed_data)

                    # decompressed_frame = cv2.imdecode(np.frombuffer(base64.b64decode(compressed_frame), dtype=np.uint8), cv2.IMREAD_COLOR)
                    # decompressed_frame = base64.decode(gzip.decompress(compressed_frame.encode('utf-8')))

                    # --------------

                    # cv2.imwrite('test.jpg', reshaped_frame)

                    # asyncio.run_coroutine_threadsafe(async_show(data.copy()), asyncio.get_event_loop())
                    # async_show(data.copy())

                    # task1 = asyncio.create_task(async_show(data.copy()))
                    # await task1

                    task2 = asyncio.create_task(write_img(data.copy()))
                    await task2

                    # task3 = asyncio.create_task(detect_img(data.copy()))
                    # result_data = await task3
                    # print('Result : ', result_data)

                    # print(data[2].shape)
                    read_img(data.copy())

                    # del data

                    # cv2.imshow(f'Webcam {index}', reshaped_frame)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                except:
                    print("json parsing error")

                # print(greeting['index'])

                # TODO: 이미지 처리 구간
                

                # 이미지를 보낼때 처리
                # await websocket.send("client send 이미지 처리 완료, 이미지 전달함")
                # print(f">>> 이미지 처리 완료, 이미지 전달함")
        except KeyboardInterrupt:
            # clean up resources here
            pass

def yolo():
    from yolo_segmentation import YOLOSegmentation

    ys = YOLOSegmentation("yolov8s-seg.pt")

    return ys

# 이미지 읽어오기 잘 되나?
def read_img(data):
    import cv2
    # img = cv2.
    # img = cv2.imread(data[2])
    # cv2.
    # cv2.imread
    # img = cv2.cvtColor(data[2], cv2.COLOR_RGB2BGR)
    img = data[2]
    # print(img.shape)
    # print
    cv2.imwrite('test.jpg', img)
    # cv2.imshow('test', img)
    pass

async def main(ys):
    await receive_stream_data(ys)

if __name__ == "__main__":

    ys = yolo()

    print(type(ys))
    asyncio.run(main(ys))