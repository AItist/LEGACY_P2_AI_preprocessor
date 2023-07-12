import numpy as np
import quaternion

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
        self.rotation = rotation # euler angle

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

    def rotate(self, point):
        """
        Returns the rotated point by the same amount as the camera rotation.
        """
        R = rotation_matrix(self.rotation)
        return np.dot(R, point)
    
    def translate(self, point):
        """
        Returns the translated point by the same amount as the camera position.
        """
        return point + self.position
    
    def transform(self, point):
        """
        Returns the transformed point by the same amount as the camera position and rotation.
        """
        return self.translate(self.rotate(point))
    
    def transform_points(self, points):
        """
        Returns the transformed points by the same amount as the camera position and rotation.
        """
        return np.array([self.transform(point) for point in points])
    
    def transform_points2(self, points):
        """
        Returns the transformed points by the same amount as the camera position and rotation.
        """
        results = np.array([])
        for point in points:
            results = np.append(results, self.transform(point))
        return results.reshape(-1, 3)


# TODO: 카메라 1개 기준 코드 수행
if __name__ == '__main__':
    # 1 카메라 클래스 기반 인스턴스 생성 (카메라 위치, 카메라 각도를 가짐)
    camera1 = Camera(position=np.array([1, 1, 1]), rotation=np.array([0, 0, 0]))

    # 2 각도와 위치를 변환할 점들의 리스트를 가져옵니다.
    point_positions = np.array([[1.28, 0.72, 1],
                            [1.28, -0.72, 1],
                            [-1.28, -0.72, 1],
                            [-1.28, 0.72, 1],])

    transformed_points = camera1.transform_points(point_positions)
    print(transformed_points)

    # transformed_points2 = camera1.transform_points2(point_positions)
    # print(transformed_points2)
