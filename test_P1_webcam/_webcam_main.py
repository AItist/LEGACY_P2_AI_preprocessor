import cv2
import device
import threading
import socket
import time
import webcam_list

def capture_frames(index, camIndex):
    """
    멀티스레드 환경에서 웹캠을 열고 프레임을 전송한다.
    """
    cap = cv2.VideoCapture(index)

    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow("frame", frame)
            # print(index)
            
            # key: 'ESC'    
            key = cv2.waitKey(20)
            if key == 27:
                break
        else:
            break


        time.sleep(1/60)

    cap.release() 
    cv2.destroyAllWindows()

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

    for t in threads:
        t.join()

    cv2.destroyAllWindows()