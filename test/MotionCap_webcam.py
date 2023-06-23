import cv2
from cvzone.PoseModule import PoseDetector
import socket

# cap = cv2.VideoCapture('test/Video.mp4')
cap = cv2.VideoCapture(0)

# Pose Detector
detector = PoseDetector()

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

posList = []
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)

    if bboxInfo:
        lmString = ''
        for lm in lmList:
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
        # print(len(lmString))
        # print(lmString)
        # print()

        # posList.append(lmString)
        sock.sendto(str.encode(str(lmString)), serverAddressPort)

        



    # print(len(posList))
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # key = cv2.waitKey(1)
    # if key == ord('s'):
    #     with open("AnimationFile.txt", 'w') as f:
    #         f.writelines(["%s\n" % item for item in posList])