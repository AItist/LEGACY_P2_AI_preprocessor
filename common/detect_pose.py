import asyncio
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.3)

async def detect_mediapipe_pose(imgdata, debug=False):
    import cv2
    # await asyncio.sleep(0.005)

    img = imgdata[2]

    results = pose.process(img)

    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    if debug:
        cv2.imwrite(f'webcam {imgdata[0]} pose.jpg', img)

    return img
    pass