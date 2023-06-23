
def _is_camera_connected(index):
    """
    카메라가 연결되었는지 확인한다.
    """
    import cv2
    
    """Check if camera is connected"""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return False
    cap.release()
    return True

def _capture_frames_from_camera(index, debug=False):
    """
    웹캠에서 프레임이 가져와지는지 확인한다.
    """
    import cv2

    """ 웹캠이 정상적으로 사용 가능한 상태인지 확인합니다. """
    if index > 5:
        if debug:
            print(f'alert : index number {index} is over 5. can occur [getStreamChannelGroup Camera index out of range] error.')
            # print('[ERROR:0@4.459] global obsensor_uvc_stream_channel.cpp:156 cv::obsensor::getStreamChannelGroup Camera index out of range')
        return False

    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    result = False

    try:
        if not _is_camera_connected(index):
            # print(f"111 Camera {index} is not connected.")
            # print('명시적으로 캡쳐 한번 더 걸어줘야 아래 cap.read()가 의도한대로 작동함')
            pass

        ret, frame = cap.read()

        if not ret:
            # print(f"Error reading frames from camera {index}.")
            pass
        else:
            # print(f"Camera {index} is connected.")
            result = True
    except Exception as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        return result

def available_webcam_indexes(indexes, debug=False):
    """Example usage: capture frames from all connected cameras"""
    lst = []

    for i in indexes:
        camera_connected = _capture_frames_from_camera(i, debug=debug)
        if camera_connected:
            print(f"Camera {i} is connected.")
            lst.append(i)
        else:
            print(f"Camera {i} is not connected.")

    if debug:
        print(f'현재 사용 가능한 웹캠 인덱스 : {lst}')

    return lst

if __name__ == '__main__':
    input_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    available_webcam_list = available_webcam_indexes(input_indexes, False)
    # available_webcam_list = available_webcam_indexes(10, True)

    print(available_webcam_list)
