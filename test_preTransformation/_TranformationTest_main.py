import time
import numpy as np
import Conversion_TestCase1 as case
# 2: O: 카메라 인스턴스를 생성한다.
from Transformation import Camera
# 중점을 계산합니다.
import LineSegments3_np as line3

CAMERA_COUNT = 4

# 1: 테스트케이스에서 각 카메라에서 입력받은 3차원 좌표를 numpy array로 변환한 변수를 가져온다.
test_data1 = np.array([[0, 0, 1],
                      [0, 0.5857, 3.4142],
                    [1.28, 0.72, 1],
                    [1.28, -0.72, 1],
                    [-1.28, -0.72, 1],
                    [-1.28, 0.72, 1],])

test_data2 = np.array([[0, 0, 2],
                      [0, 0.5857, 3.4142],
                    [1.28, 0.72, 1],
                    [1.28, -0.72, 1],
                    [-1.28, -0.72, 1],
                    [-1.28, 0.72, 1],])

test_data3 = np.array([[0, 0, 2],
                      [0, 0.5857, 3.4142],
                    [1.28, 0.72, 1],
                    [1.28, -0.72, 1],
                    [-1.28, -0.72, 1],
                    [-1.28, 0.72, 1],])

test_data4 = np.array([[0, 0, 2],
                      [0, 0.5857, 3.4142],
                    [1.28, 0.72, 1],
                    [1.28, -0.72, 1],
                    [-1.28, -0.72, 1],
                    [-1.28, 0.72, 1],])

# TODO : 임시 테스트 데이터 투입
case.cam1_points = test_data1
case.cam2_points = test_data2
cam3_points = test_data3
cam4_points = test_data4


# 카메라 인스턴스는 글로벌 변수로 다룬다 (설치 환경에 고정되는 특징)
camera1 = Camera(position=np.array([0, 0, 0]), rotation=np.array([0, 0 , 0]))
camera2 = Camera(position=np.array([-1, 0, 0]), rotation=np.array([0, 45, 0]))
camera3 = Camera(position=np.array([1, 0, 0]), rotation=np.array([0, -45, 0]))
camera4 = Camera(position=np.array([0, 1, 0]), rotation=np.array([0, 45 , 0]))


# print(case.cam1_points)
def set_midpoints_with_1camera():
    transformed_points1 = camera1.transform_points(case.cam1_points)

    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([camera1.position, row]) for row in transformed_points1]

    return transformed_points1



def set_midpoints_with_2cameras():
    transformed_points1 = camera1.transform_points(case.cam1_points)
    transformed_points2 = camera2.transform_points(case.cam2_points)

    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([camera1.position, row]) for row in transformed_points1]
    new_array2 = [np.array([camera2.position, row]) for row in transformed_points2]

    midpoint_result = np.array([])
    for i, (a1, a2) in enumerate(zip(new_array1, new_array2)):
        # point_line1 = a1
        # point_line2 = a2
        # lines = [point_line1, point_line2]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    midpoint_result = midpoint_result.reshape(-1, 3)
    # for i in midpoint_result:
    #     print(i)

    return midpoint_result



def set_midpoints_with_3cameras():
    transformed_points1 = camera1.transform_points(case.cam1_points)
    transformed_points2 = camera2.transform_points(case.cam2_points)
    transformed_points3 = camera3.transform_points(cam3_points)


    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([camera1.position, row]) for row in transformed_points1]
    new_array2 = [np.array([camera2.position, row]) for row in transformed_points2]
    new_array3 = [np.array([camera3.position, row]) for row in transformed_points3]

    midpoint_result = np.array([])
    for i, (a1, a2, a3) in enumerate(zip(new_array1, new_array2, new_array3)):
        # point_line1 = a1
        # point_line2 = a2
        # point_line3 = a3
        # lines = [point_line1, point_line2, point_line3]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2, a3])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    midpoint_result = midpoint_result.reshape(-1, 3)
    # for i in midpoint_result:
    #     print(i)

    return midpoint_result


def set_midpoints_with_4cameras():
    transformed_points1 = camera1.transform_points(case.cam1_points)
    transformed_points2 = camera2.transform_points(case.cam2_points)
    transformed_points3 = camera3.transform_points(cam3_points)
    transformed_points4 = camera4.transform_points(cam4_points)


    # 카메라에 대응하는 변환된 좌표 배열을 생성한다.
    new_array1 = [np.array([camera1.position, row]) for row in transformed_points1]
    new_array2 = [np.array([camera2.position, row]) for row in transformed_points2]
    new_array3 = [np.array([camera3.position, row]) for row in transformed_points3]
    new_array4 = [np.array([camera4.position, row]) for row in transformed_points4]

    midpoint_result = np.array([])
    for i, (a1, a2, a3, a4) in enumerate(zip(new_array1, new_array2, new_array3, new_array4)):
        # point_line1 = a1
        # point_line2 = a2
        # point_line3 = a3
        # lines = [point_line1, point_line2, point_line3]
        # points = line3.calculate_midpoints(lines)

        points = line3.calculate_midpoints([a1, a2, a3, a4])
        midpoint = line3.final_midpoint(points)

        midpoint_result = np.append(midpoint_result, midpoint)

    midpoint_result = midpoint_result.reshape(-1, 3)
    # for i in midpoint_result:
    #     print(i)

    return midpoint_result


import time

start = time.time()
if CAMERA_COUNT == 1:
    print("Camera count is 1")
    midpoints = set_midpoints_with_1camera()
    pass
elif CAMERA_COUNT == 2:
    print("Camera count is 2")
    midpoints = set_midpoints_with_2cameras()
elif CAMERA_COUNT == 3:
    print("Camera count is 3")
    midpoints = set_midpoints_with_3cameras()
elif CAMERA_COUNT == 4:
    print("Camera count is 4")
    midpoints = set_midpoints_with_4cameras()
    pass
end = time.time()

print(midpoints)
print(f'elapsed time : {end - start}')