#!/usr/bin/env python

import asyncio
import websockets
import json
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3)

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

def data_package_process(data):
    import gzip
    import base64

    compressed = gzip.compress(data[2])
    # print(compressed)

    _data = {
        'index': data[0],
        'ret': data[1],
        'frame': base64.b64encode(compressed).decode('utf-8')
    }

    json_data = json.dumps(_data)
    return json_data


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

                    # TODO : 이미지 처리 및 결과 전송

                    # decompressed_frame = cv2.imdecode(np.frombuffer(base64.b64decode(compressed_frame), dtype=np.uint8), cv2.IMREAD_COLOR)
                    # decompressed_frame = base64.decode(gzip.decompress(compressed_frame.encode('utf-8')))

                    # --------------

                    # cv2.imwrite('test.jpg', reshaped_frame)

                    # asyncio.run_coroutine_threadsafe(async_show(data.copy()), asyncio.get_event_loop())
                    # async_show(data.copy())

                    # task1 = asyncio.create_task(async_show(data.copy()))
                    # await task1

                    # 포즈 저장
                    task1 = asyncio.create_task(detect_mediapipe_pose(data.copy()))
                    await task1

                    # 이미지 저장(테스트)
                    task2 = asyncio.create_task(write_img(data.copy()))
                    await task2

                    # print(data[2].shape)
                    result_img = detect_person_img(data.copy(), ys, write=False)

                    if result_img is not None:
                        # cv2.imshow(f'Webcam {data[0]}', result_img)
                        # cv2.waitKey(1)
                        # data[0] : index
                        # data[1] : ret
                        # result_img : 분류 결과 이미지 1장
                        _data = [data[0], data[1], result_img]

                        packet = data_package_process(_data)

                        await websocket.send(packet)
                        # pass

                    del parsed_data, data, result_img, _data, packet
                except Exception as e:
                    # print("json parsing error")
                    print(e)
                    pass
                

                # 이미지를 보낼때 처리
                # await websocket.send("client send 이미지 처리 완료, 이미지 전달함")
                # print(f">>> 이미지 처리 완료, 이미지 전달함")
        except KeyboardInterrupt:
            # clean up resources here
            pass

#region task 1 - mediapipe pose

async def detect_mediapipe_pose(imgdata):
    import cv2
    await asyncio.sleep(0.005)

    img = imgdata[2]

    results = pose.process(img)

    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    cv2.imwrite(f'webcam {imgdata[0]} pose.jpg', img)
    pass

#endregion

#region task 2
def yolo_instance():
    """
    yolo 인스턴스 생성
    """
    from yolo_segmentation import YOLOSegmentation

    ys = YOLOSegmentation("yolov8s-seg.pt")

    # ys.detect
    return ys


def detect_person_img(data, ys, write=False):
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
#endregion

async def main(ys):
    await receive_stream_data(ys)

if __name__ == "__main__":

    ys = yolo_instance()

    print(type(ys))
    asyncio.run(main(ys))