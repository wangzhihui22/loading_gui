# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 20:31
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : dataset.py
# @Software: PyCharm
import glob
import os

import cv2.cv2
import numpy as np

from tools.path import get_project_path
from tools.utils import quaternion2euler

img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']


class LoadImages:
    def __init__(self, _path):
        if os.path.isdir(_path):
            files = sorted(glob.glob(os.path.join(_path, '*.*')))  # dir
        else:
            raise Exception(f'ERROR: {_path} does not exist')
        images = [x for x in files if x.split('.')[-1].lower() in img_formats]
        self.ni = len(images)

        self.files = images

        self.count = 0

    def __iter__(self):
        self.count = 0
        return self

    def reset(self):
        self.count = 0

    def __next__(self):
        if self.count == self.ni:
            raise StopIteration
        path = self.files[self.count]

        self.count += 1
        img0 = cv2.imread(path)
        assert img0 is not None, 'Image Not Found ' + path

        return path, img0


class LoadFlightData:
    def __init__(self, path):
        # path = "db/imu/airsim_rec.txt"
        self._path = os.path.join(get_project_path(), path)
        self.flight_data = self.read_file()
        self.ni = len(self.flight_data)
        self.count = 0

    def read_file(self):
        data = []
        with open(self._path, "r") as f:
            _ = f.readline()
            line = f.readline()
            while line:
                line = line.split(" ")
                d = list(map(float, line[2:9]))

                d[0] = (1739.600 + float(line[0 + 2]))
                d[1] = (11713.300 + float(line[1 + 2]))
                d[2] = (3033.400 - float(line[2 + 2]))
                # w x y z
                euler = quaternion2euler(*d[3:])
                data.append(d[:3] + euler.tolist())
                line = f.readline()
        return np.array(data, dtype=np.double)

    def __iter__(self):
        self.count = 0
        return self

    def reset(self):
        self.count = 0

    def __next__(self):
        if self.count == self.ni:
            raise StopIteration
        self.count += 1
        return self.flight_data[self.count]


if __name__ == '__main__':
    # path = r"/db/images"
    # # a = r'E:\OneDrive\code\loading\db\images\img_Drone1_0_0_1632635711007055400.png'
    # # i = cv2.imread(a)
    # data = LoadImages(path)
    # for i, img in data:
    #     cv2.imshow("img", img)
    #     cv2.waitKey(0)

    path = r"db/imu/airsim_rec.txt"
    data = LoadFlightData(path)
    for i in data:
        print(i)
