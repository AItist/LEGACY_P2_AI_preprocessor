import asyncio
from Webcam import available_webcam_indexes as webcams_indexes
import time

commonDelay = 0.25

async def async_show(data):
    import cv2
    await asyncio.sleep(commonDelay)
    cv2.imshow(f'Webcam {data[0]}', data[2])
    del data

async def webcams_run(indexes, debug=False):
    """ 사용 가능한 웹캠 인덱스를 받아서, 해당 웹캠으로부터 프레임을 받아옵니다.
    :param indexes: 사용 가능한 웹캠 인덱스 리스트
    :param debug: 디버그 모드
    :return: None
    참고 : examples/webcam_m_test_1.py
    """
    import cv2

    append_st = time.perf_counter()
    webcams = []
    for index in indexes:
        webcams.append((index, cv2.VideoCapture(index)))
    append_et = time.perf_counter()
    print(f'append time : {append_et - append_st}')

    

    # 사용 가능한 최대 웹캠 인덱스 + 1 만큼의 리스트를 생성합니다.
    ret_frames = [0] * (max(indexes) + 1)
    while True:

        # start = time.time()
        # await asyncio.sleep(0.01)
        # end = time.time()
        # print(f'asyncio.sleep time : {end - start}')

        # read_st = time.perf_counter()
        for i, webcam in webcams:
            # 새로운 프레임을 받아옵니다.
            ret, frame = webcam.read()
            # 받아온 프레임을 리스트에 저장합니다. 새 메모리 공간을 할당하지 않고, 기존의 메모리 공간을 재사용합니다.
            ret_frames[i] = [i, ret, frame]
        # read_et = time.perf_counter()
        # print(f'read time : {read_et - read_st}')

        show_st = time.perf_counter()
        for i in indexes:
            
            if ret_frames[i][1]:
                # 웹캠의 데이터를 서버로 전송합니다. 이 부분은 비동기화가 되어야 합니다.
                asyncio.create_task(async_show_forwarding(ret_frames[i].copy()))
                # cv2.imshow(f'Webcam {i}', ret_frames[i][2])

                # task1 = asyncio.create_task(async_show(ret_frames[i].copy()))
                # await task1
                # print(debug)
                if debug:
                    # 웹캠의 이미지를 디스플레이 합니다. 이 부분은 동기화가 되어야 합니다.
                    task1 = asyncio.create_task(async_show(ret_frames[i].copy()))
                    await task1
                else:
                    # 웹캠 출력을 하지 않을때, 아래 비동기 대기 코드를 활성화
                    await asyncio.sleep(commonDelay)

                pass

            # else:
            #     print('Error reading frame from capture device')
        show_et = time.perf_counter()
        # print(f'show time : {show_et - show_st}')

        if cv2.waitKey(1) == ord('q'):
            break

    for i, webcam in webcams:
        webcam.release()
    cv2.destroyAllWindows()




async def async_show_forwarding(data):
    import gzip
    import json
    import requests
    import base64

    # 1 압축
    loop = asyncio.get_running_loop()
    # print(type(data[2]))
    # print(data[2].shape)
    # print(data[2][0][0][0])
    compressed = await loop.run_in_executor(None, gzip.compress, data[2])

    url_base = 'http://localhost:3000/'
    response_base = requests.head(url_base)
    if response_base.status_code == 200:
        # print("Server is up")

        url = 'http://localhost:3000/ws/data'
        headers = {'Content-Type': 'application/json'}

        # print(type())
        # 2 압축 데이터 base64 인코딩해서 json 추가
        _data = {
            'index': data[0],
            'ret': data[1],
            'frame': base64.b64encode(compressed).decode('utf-8')
        }

        json_data = json.dumps(_data)

        try:
            response = requests.post(url, data=json_data, headers=headers)
        except Exception as e:
            print(e)
            pass

        # raise Exception('test')
        # print(json_data)
    else:
        # print("Server is down")
        pass


    del data, _data, json_data, compressed


if __name__ == '__main__':
    input_indexes = [0, 1, 3]
    indexes = webcams_indexes(input_indexes, debug=False)

    # print(indexes)

    # exit()
    if len(indexes) == 0:
        print('No webcams available')
        exit()

    asyncio.run(webcams_run(indexes, debug=True))

