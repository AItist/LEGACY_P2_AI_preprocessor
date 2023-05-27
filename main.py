import asyncio
from common.asyncioStack import AsyncioStack as asyncStack

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3)

def yolo_instance():
    """
    yolo 인스턴스 생성
    """
    from yolo_segmentation import YOLOSegmentation

    ys = YOLOSegmentation("yolov8s-seg.pt")

    # ys.detect
    return ys

ys = yolo_instance()

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

async def detect_mediapipe_pose(imgdata):
    import cv2
    await asyncio.sleep(0.005)

    img = imgdata[2]

    results = pose.process(img)

    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    cv2.imwrite(f'webcam {imgdata[0]} pose.jpg', img)

    return img
    pass



async def detect_person_img(data, ys, write=False):
    """
    이미지에서 사람을 검출한다.
    data[0] : index
    data[1] : ret
    data[2] : img
    ys : yolo_segmentation 객체

    return : 사람 검출된 이미지 / 검출된 사람이 없으면 None
    """
    import cv2
    img = data[2]

    # print(111)
    bboxes, classes, segmentations, scores = ys.detect(img)
    # print(222)  # 위에 detect되는 개체도 없으면 이 코드 라인이 실행이 안됨.

    count = 0
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        # print("bbox:", bbox, "class id:", class_id, "seg:", seg, "score:", score)

        # class id 0은 사람
        if class_id == 0:    
            count += 1
            (x, y, x2, y2) = bbox
            
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)

            cv2.polylines(img, [seg], True, (0, 0, 255), 4)

            cv2.putText(img, str(class_id), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # 사람 한번도 검출 안된거면 None 리턴
    if count == 0:
        return None

    if write:
        cv2.imwrite('test.jpg', img)
    return img

# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------

# queue = asyncio.Queue()
stack = asyncStack()
condition = asyncio.Condition()

async def async_websocket():
    import websockets
    
    count = 0

    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                data = await websocket.recv()
                # count += 1
                await stack.push(data)
                # await stack.push(count)

                async with condition:
                    condition.notify_all()
        except Exception as e:
            print(e)


async def async_check():
    import json
    import time

    while True:
        async with condition:
            # await condition.wait_for(lambda: queue.qsize() > 0)
            await condition.wait_for(lambda: stack.len() > 0)
            # data = await queue.get()
            data = await stack.pop()
        # queue.task_done()
        
        try:
            parsed_data = json.loads(data)
            # print(parsed_data)
            
            _data = data_unpack_process(parsed_data)

            start = time.time()
            pose_img, seg_img = await asyncio.gather(
                detect_mediapipe_pose(_data.copy()),
                detect_person_img(_data.copy(), ys),
            )
            end = time.time()
            print(f"async check /detect time : {end - start}")

        except Exception as e:
            print(e)

        print(f"async check /current /stacked {stack.len()}")
        # print(f"async check /current {data} /stacked {stack.len()}")
        await stack.clear()
        print(f"async check /current /stacked {stack.len()}")
        # print(f"async check /current {data} /stacked {stack.len()}")

        # await asyncio.sleep(2)

async def main():
    coro1 = async_websocket()
    coro2 = async_check()
    await asyncio.gather(
        coro1,
        coro2,
    )

asyncio.run(main())