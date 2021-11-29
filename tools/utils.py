from math import cos, sin, pi, atan2, asin, sqrt
from scipy.spatial.transform import Rotation as R
import numpy as np


def euler2quaternion(euler):
    # 欧拉角转成四元数
    # 输入为 x, y, z
    r = R.from_euler('xyz', euler, degrees=False)
    quaternion = r.as_quat()
    # 输出的为 (x, y, z, w)
    return quaternion


def quaternion2euler(w, x, y, z):
    # 四元数转成欧拉角
    # 输入为：(x, y, z, w)
    quaternion = (x, y, z, w)
    r = R.from_quat(quaternion)
    euler = r.as_euler('xyz', degrees=False)
    return euler


def euler2rotation(euler):
    # 欧拉角(x, y, z)转换为旋转矩阵   弧度
    r = R.from_euler('xyz', euler, degrees=False)
    rotation_matrix = r.as_matrix()
    return rotation_matrix


def rot_mat2euler(rot_m):
    # 选择矩阵转欧拉角
    theta_z = atan2(rot_m[1, 0], rot_m[0, 0]) * 180.0 / pi
    theta_y = atan2(-1.0 * rot_m[2, 0], sqrt(rot_m[2, 1] ** 2 + rot_m[2, 2] ** 2)) * 180.0 / pi
    theta_x = atan2(rot_m[2, 1], rot_m[2, 2]) * 180.0 / pi
    return np.array([theta_x, theta_y, theta_z], dtype=np.double)


def quaternion2rot_mat(q0, q1, q2, q3):
    # 四元数q=(q0,q1,q2,q3)到旋转矩阵
    r11, r12, r13 = 1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)
    r21, r22, r23 = 2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)
    r31, r32, r33 = 2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)
    return np.array([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]], dtype=np.double)


def radian2angle(r):
    return r * 180 / pi


def angle2radian(a):
    return a * pi / 180


if __name__ == '__main__':
    uav2mac = np.array([
        [-0.1744, 0.2588, 0.9301],
        [- 0.0457, 0.9659, 0.2546],
        [- 0.9836, 0, - 0.1805],
    ])
    e = rot_mat2euler(uav2mac).tolist()
    print(e)
