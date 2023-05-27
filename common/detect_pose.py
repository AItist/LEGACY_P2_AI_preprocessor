from common.enum_ import ePoses
import asyncio

async def detect_pose(imgdata, ePoses=ePoses.MEDIAPIPE, debug=False):

    if ePoses == ePoses.MEDIAPIPE:
        import common.pose.mediapipe_ as mediapipe_
        return await mediapipe_.detect_pose(imgdata, debug=debug)
    
    """
    TODO: 새로운 포즈 인식 모델을 추가할 때마다 이곳에 추가해야 함.
    """