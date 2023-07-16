import cv2
import device
import threading
import socket
import time
import webcam_list
import concurrent.futures
import numpy as np

import asyncio
from common.data_ import data_unpack_process, data_package_process
from common.enum_ import ePoses, eSegs

import common.Convert.Transformation as Transformation

print(f"this is _webcam_main")

CAM_COUNT = 4 # 웹캠 개수

isDebug = True # 디버그 모드
RUN_POSE = True # 포즈 검출 실행 여부
RUN_SEG = True # 영역 검출 실행 여부
poseFlag = ePoses.CVZONE # 포즈 검출 시행시 어떤 모듈을 사용할지 결정
segFlag = eSegs.YOLO # 영역 검출 시행시 어떤 모듈을 사용할지 결정

# pose 데이터를 카메라 별로 저장, 갱신하기 위한 변수
pose_datas = {}

CAM_WIDTH = 640
CAM_HEIGHT = 480

camera1 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0]))
camera2 = Transformation.Camera(position=np.array([0.365, 0, -0.915]), rotation=np.array([0, -21.653, 0]))
camera3 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0]))
camera4 = Transformation.Camera(position=np.array([0, 0, -1]), rotation=np.array([0, 0 , 0]))
cameras = [camera1, camera2, camera3, camera4]

# 데이터를 전달하기 위한 패킷 데이터
packet_data = {}
"""
{
  'pose_string' : [포즈 문자열]
  'cam1_img' : [1번 카메라 이미지]
  'cam2_img' : [2번 카메라 이미지]
  'cam3_img' : [3번 카메라 이미지]
  'cam4_img' : [4번 카메라 이미지]
}
"""

frame_buffer = {}
sendQueue = asyncio.Queue() # 가공 완료 데이터 전송용 큐

program_is_running = True
lock = threading.Lock()

def capture_frames(index, camIndex):
    """
    멀티스레드 환경에서 웹캠을 열고 프레임을 전송한다.
    """
    cap = cv2.VideoCapture(index)
    # TODO 추후 패킷 타임스탬프 에러 해결할때 오픈하기
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

    while True:
        # Check the global flag
        # with lock:
        if not program_is_running:
            break
        
        # print(f'capture_frames {index}', end='') # thread 확인용

        ret, frame = cap.read()

        if ret:
            # print(frame.shape) # (480, 640, 3)
            # print(type(frame)) # <class 'numpy.ndarray'>
            # print(index, frame.shape)
            
            if isDebug:
                cv2.imwrite(f"frame {camIndex}.jpg", frame)

            # update the frame buffer with the latest frame
            # frame_buffer[index] = frame
            frame_buffer[camIndex] = frame


            # # key: 'ESC'    
            # key = cv2.waitKey(20)
            # if key == 27:
            #     break
        else:
            break


        time.sleep(1/5)

    cap.release() 
    cv2.destroyAllWindows()



def process_frame(camIndex, imgData, isDebug=False):
    """
    단일 프레임을 처리한다.
    """

    # print(f'process_frame {camIndex}', end='') # thread 확인용

    from common.detect_pose import detect_pose
    from common.detect_seg import detect_seg

    pose_img_string = None
    seg_img = None

    # 포즈 처리 (검출 안되면 None, 검출되면 ,로 구분된 문자열)
    if RUN_POSE:
        pose_img_string = detect_pose(imgData, poseFlag, debug=isDebug)
        pose_datas[camIndex] = pose_img_string
        # print(f'{camIndex} : {pose_img_string}')

    # 영역 처리
    if RUN_SEG:
        seg_img = detect_seg(imgData, segFlag, debug=isDebug)
        seg_img = cv2.flip(seg_img, 0)


    # # TODO : Debug
    # seg_img = None

    if isDebug:
        ## cv2.imwrite(f"pose {camIndex}.jpg", pose_img_string) # MEDIAPIPE은 이미지 전달함. 제외 고민

        ## print(pose_img_string) # CVZONE은 문자열화된 리스트 전달함
        # cv2.imwrite(f"seg {camIndex}.jpg", seg_img)
        pass

    # LEGACY
    # if seg_img is None:
    #     # print('디버깅중')
    #     # return None
    #     seg_img = ''

    camKey = f'img_{camIndex}'
    packet_data[camKey] = seg_img   # 패킷 데이터 저장 
    # packet_data[camIndex] = [seg_img, pose_img_string

    # if pose_img_string is None:
    #     pose_img_string = ''

    # return [camIndex, True, seg_img, pose_img_string]

def process_frames():
    """
    Observe the state of frame_buffer and print the frames.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            # with lock:
            if not program_is_running:
                break
            
            # print(f'process_frames', end='') # thread 확인용

            if frame_buffer:  # check if frame_buffer is not empty
                futures = []
                for camIndex, imgData in list(frame_buffer.items()):
                    # print(key, value.shape)
                    if imgData is not None:
                        executor.submit(process_frame, camIndex, imgData, isDebug)

                        # future = executor.submit(process_frame, camIndex, imgData, isDebug)
                        # futures.append(future)
                
                # # Wait for all futures to complete
                # for future in concurrent.futures.as_completed(futures):
                #     try:
                #         result = future.result()  # get the result (will raise an exception if the function failed)
                #         # print(result)

                #         if result is None:
                #             # TODO: 여기의 조건식이 필요한 구간 검색
                #             # print(f"Exception while processing frame 11: {result}")
                #             continue

                #         if result[3] == '':
                #             print(f"Exception while processing frame 22 text is empty")
                #             continue

                #         packet = data_package_process(result)

                        
                #         sendQueue.put_nowait(packet)

                #     except Exception as e:
                #         print(f"Exception while processing frame 33: {e}")

                # for key, value in frame_buffer.items():
                #     if value is not None:  # check if the value is not None
                #         print(key, value.shape)
            time.sleep(1/240)


import common.Convert.StringToNumpy as StringToNumpy
def _calculate_midpoints(poses):
    """
    calculate_midpoints에서 실행되는 카메라 2대 이상의 데이터 수집시 수행되는 함수
    각 카메라의 점들을 회전, 이동한 후 중점을 계산한다.
    각 두 선간의 중점 계산후 그 중점들의 중점을 계산한다.
    중점 배열을 문자열 변환한다.
    문자열을 반환한다.

    Parameters
    ----------
    poses : dict
    """
    pose_len = len(poses)

    result = {}
    try:
        # 문자열을 np.array로 변환
        for camIndex, poseString in poses.items():
            _pose = StringToNumpy.convert_string_to_numpy_array(poseString, CAM_WIDTH, CAM_HEIGHT)
            result[camIndex] = _pose
        
        midpoint_result = None

        # 중점의 리스트를 생성한다.
        if pose_len == 1:
            midpoint_result = Transformation.set_midpoints_with_1camera(cameras, result)
        if pose_len == 2:
            midpoint_result = Transformation.set_midpoints_with_2cameras(cameras, result)
        elif pose_len == 3:
            midpoint_result = Transformation.set_midpoints_with_3cameras(cameras, result)
        elif pose_len == 4:
            midpoint_result = Transformation.set_midpoints_with_4cameras(cameras, result)

        # print(midpoint_result.shape)
        # print(midpoint_result[0])

        str_arr = ','.join(map(str, midpoint_result))
        # print(str_arr)

        return str_arr

        pass
    except Exception as e:
        # 'NoneType' object has no attribute 'split'
        # print(e)
        print('calculate_midpoints error')

    pass

def _is_all_seg_data_exist(_packet_data):
    
    isAllExist = False
    for key, value in _packet_data.items():
        if key.startswith('img_'):
            if value is None:
                isAllExist = False
                break

            isAllExist = True
        pass

    return isAllExist


def calculate_midpoints():
    """
    pose_datas를 이용하여 중간점을 계산한다.
    pose_datas의 각 원소는 [카메라 인덱스, 포즈 문자열]이다.
    """
    while True:
        # with lock:
        if not program_is_running:
            break

        time.sleep(1/10)

        if len(pose_datas) < 2:
            # print(f'pose_datas len : {len(pose_datas)}')
            continue

        if _is_all_seg_data_exist(packet_data) == False:
            # print(f'is all seg data exist : {_is_all_seg_data_exist(packet_data)}')
            continue

        # print(f'before seg data exist : {_is_all_seg_data_exist(packet_data)}')

        poses = pose_datas.copy()

        midpoints = _calculate_midpoints(poses)
        
        packet_data['pose_string'] = midpoints
        # print(packet_data['pose_string'])

        # print(f'before {packet_data.keys()}')
        packet = data_package_process(packet_data.copy(), CAM_COUNT)
        print(f'packet ready : json data type({type(packet)})')

        sendQueue.put_nowait(packet)

        with lock:
            pose_datas.clear()
            packet_data.clear()
            # print(len(pose_datas))
            pass
        

        # # print(len(pose_datas))
        # if len(pose_datas) > 1:
        #     # print(2)
        #     # print(pose_datas)


    pass


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

                # print('**********************************************')
                if sendQueue.qsize() > 0:
                    # print('qsize : ', sendQueue.qsize())
                    for i in range(sendQueue.qsize()):
                        packet = await sendQueue.get()
                        await websocket.send(packet)
                time.sleep(0.05)
                pass
        except Exception as e:
            print(f"Exception while processing frame 33: {e}")

async def async_main():
    coro1 = async_websocket()
    await asyncio.gather(coro1)

if __name__ == "__main__":
    webcam_lst = webcam_list.get_all_webcams()
    webcam_lst = webcam_list.get_available_webcams(webcam_lst)
    print(f'webcam_lst : {webcam_lst} / count : {len(webcam_lst)} ')
    CAM_COUNT = len(webcam_lst)

    try:
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

        t = threading.Thread(target=calculate_midpoints)
        t.start()
        threads.append(t)

        asyncio.run(async_main())
        
    except KeyboardInterrupt:
    # except Exception:
        print("**********")
        print("KeyboardInterrupt")
        print("Interrupt")
        print("**********")
        with lock:
            program_is_running = False
        
        for t in threads:
            t.join()

        cv2.destroyAllWindows()
    

