import cv2
import device
import threading
import socket
import time
import webcam_list
import concurrent.futures

import asyncio
from common.data_ import data_unpack_process, data_package_process
from common.enum_ import ePoses, eSegs

print(f"this is _webcam_main")

isDebug = False
poseFlag = ePoses.CVZONE
segFlag = eSegs.YOLO

frame_buffer = {}
sendQueue = asyncio.Queue() # 가공 완료 데이터 전송용 큐

def capture_frames(index, camIndex):
    """
    멀티스레드 환경에서 웹캠을 열고 프레임을 전송한다.
    """
    cap = cv2.VideoCapture(index)

    while True:
        ret, frame = cap.read()

        if ret:
            # print(frame.shape) # (480, 640, 3)
            # print(type(frame)) # <class 'numpy.ndarray'>
            # cv2.imshow(f"frame {camIndex}", frame)
            
            # TODO: 디버깅
            cv2.imwrite(f"frame {index}.jpg", frame)

            # update the frame buffer with the latest frame
            # TODO: 웹캠 오기 전까지 디버깅용으로 index 저장
            frame_buffer[index] = frame
            # frame_buffer[camIndex] = frame


            # # key: 'ESC'    
            # key = cv2.waitKey(20)
            # if key == 27:
            #     break
        else:
            break


        time.sleep(1/60)

    cap.release() 
    cv2.destroyAllWindows()

def process_frame(camIndex, imgData, isDebug=False):
    """
    단일 프레임을 처리한다.
    """
    from common.detect_pose import detect_pose
    from common.detect_seg import detect_seg

    # 포즈 처리 (검출 안되면 None, 검출되면 ,로 구분된 문자열)
    pose_img_string = detect_pose(imgData, poseFlag, debug=isDebug)

    # 영역 처리
    seg_img = detect_seg(imgData, segFlag, debug=isDebug)

    if isDebug:
        print(pose_img_string) # CVZONE은 문자열화된 리스트 전달함
        # cv2.imwrite(f"pose {camIndex}.jpg", pose_img_string) # MEDIAPIPE은 이미지 전달함. 제외 고민

        cv2.imwrite(f"seg {camIndex}.jpg", seg_img)
        pass

    if seg_img is None:
        return None

    if pose_img_string is None:
        pose_img_string = ''

    return [camIndex, True, seg_img, pose_img_string]

def process_frames():
    """
    Observe the state of frame_buffer and print the frames.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            if frame_buffer:  # check if frame_buffer is not empty
                futures = []
                for camIndex, imgData in list(frame_buffer.items()):
                    # print(key, value.shape)
                    if imgData is not None:
                        future = executor.submit(process_frame, camIndex, imgData, isDebug)
                        futures.append(future)
                
                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()  # get the result (will raise an exception if the function failed)
                        # print(result)

                        if result is None:
                            print(f"Exception while processing frame 11: {result}")
                            continue

                        if result[3] == '':
                            print(f"Exception while processing frame 22 text is empty")
                            continue

                        packet = data_package_process(result)


                        # TODO: 웹소켓 전달, 테스트
                        sendQueue.put_nowait(packet)

                    except Exception as e:
                        print(f"Exception while processing frame 33: {e}")

                # for key, value in frame_buffer.items():
                #     if value is not None:  # check if the value is not None
                #         print(key, value.shape)
            time.sleep(1/240)

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

                # print(f"recv count : {debugCount}")

                # condition 쓰면 동기화됨..
                # async with condition:
                #     condition.notify_all()

                # if sendQueue.qsize() > 0:
                #     print('qsize : ', sendQueue.qsize())
                #     for i in range(sendQueue.qsize()):
                #         packet = await sendQueue.get()
                #         await websocket.send(packet)
                time.sleep(0.5)
                pass
        except Exception as e:
            print(e)

if __name__ == "__main__":
    webcam_lst = webcam_list.get_all_webcams()
    webcam_lst = webcam_list.get_available_webcams(webcam_lst)

    # print(webcam_lst)
    threads = []

    for index, camIndex in webcam_lst.items():
        """
        개별 웹캠의 입력을 받아온다.
        """
        print(index, camIndex)
        t = threading.Thread(target=capture_frames, args=(index, camIndex))
        t.start()
        threads.append(t)

    # Start the process_frames function in a new thread
    t = threading.Thread(target=process_frames)
    t.start()
    threads.append(t)

    # asyncio.run(async_websocket())

    for t in threads:
        t.join()

    cv2.destroyAllWindows()