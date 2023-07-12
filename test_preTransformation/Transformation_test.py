import numpy as np
import quaternion

def rotation_matrix_x(theta):
    """
    Returns the rotation matrix for a rotation around the x-axis by theta radians.
    """
    theta = np.radians(theta)

    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

def rotation_matrix_y(theta):
    """
    Returns the rotation matrix for a rotation around the y-axis by theta radians.
    """
    theta = np.radians(theta)

    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def rotation_matrix_z(theta):
    """
    Returns the rotation matrix for a rotation around the z-axis by theta radians.
    """
    theta = np.radians(theta)

    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

def rotation_matrix(rotations):
    """
    Returns the rotation matrix for rotations around the x, y, and z axes.
    """
    rx, ry, rz = np.radians(rotations)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])

    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])

    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])

    # The rotation matrix for rotations about the x, y, and z axes
    R = np.dot(Rz, np.dot(Ry, Rx))

    return R

class Camera:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.rotation_radians = np.radians(rotation)
        self.rotation_quat = quaternion.from_euler_angles(*self.rotation_radians)

# TODO: 카메라 1개 기준 코드 수행

# # Position of the camera
# camera_position = np.array([0, 0, 0])
# # Rotation of the camera
# camera_rotation = np.array([45, 0, 0])  # In degrees

# 1 카메라 클래스 기반 인스턴스 생성 (카메라 위치, 카메라 각도를 가짐)
camera1 = Camera(position=np.array([1, 1, 1]), rotation=np.array([45, 0, 0]))

# 2 각도와 위치를 변환할 점들의 리스트를 가져옵니다.
point_positions = np.array([[1.28, 0.72, 1],
                           [1.28, -0.72, 1],
                           [-1.28, -0.72, 1],
                           [-1.28, 0.72, 1],])

# Rotation matrices for each axis
rotation_mats = [rotation_matrix_x, rotation_matrix_y, rotation_matrix_z]

# 3 각 점(point)별로 반복을 실행하여 각도 변환, 위치 이동을 수행합니다.
results = np.array([])
for point in point_positions:
    # 회전: Rotate the point by the same amount as the camera rotation
    _point_position = None
    
    # #1 #2의 내용과 동일한 내용
    # for axis, angle in enumerate(camera1.rotation):
    #     print(axis, angle, camera1.position)
    #     if angle != 0:  # Only perform rotation if the angle is not 0
    #         rotation_mat = rotation_mats[axis](angle)
    #         _point_position = np.dot(rotation_mat, point) # + camera1.position

    # #2 XXX : z축 포함한 회전시 짐벌락 문제 발생. 일단 이 방법으로 진행
    R = rotation_matrix(camera1.rotation)
    _point_position = np.dot(R, point) + camera1.position

    # #3 XXX : x축을 포함한 회전시 문제 발생
    # # Convert the point position to a quaternion
    # point_position_quat = quaternion.quaternion(0, *point)
    # # Apply the rotation to the point position
    # rotated_point_position = camera1.rotation_quat * point_position_quat * camera1.rotation_quat.inverse()
    # # Extract the rotated point position
    # rotated_point_position = np.array([rotated_point_position.x, rotated_point_position.y, rotated_point_position.z])
    # _point_position = rotated_point_position

    # #4 XXX : x축을 포함한 회전시 문제 발생
    # qx = quaternion.from_rotation_vector(np.radians(camera1.rotation)[0] * np.array([1, 0, 0]))
    # qy = quaternion.from_rotation_vector(np.radians(camera1.rotation)[1] * np.array([0, 1, 0]))
    # qz = quaternion.from_rotation_vector(np.radians(camera1.rotation)[2] * np.array([0, 0, 1]))

    # camera_rotation_quat = qz * qy * qx

    # # Convert the point position to a quaternion
    # point_position_quat = quaternion.quaternion(0, *point)

    # # Apply the rotation to the point position
    # rotated_point_position = camera_rotation_quat * point_position_quat * camera_rotation_quat.inverse()

    # # Extract the rotated point position
    # rotated_point_position = np.array([rotated_point_position.x, rotated_point_position.y, rotated_point_position.z])

    # _point_position = rotated_point_position

    if _point_position is not None:
        results = np.append(results, _point_position)
    else:
        results = np.append(results, point)

# print(camera1.rotation_quat)
# print(point_position)
# print(point_position + camera1.position)

results = results.reshape(-1, 3)

print(results)
