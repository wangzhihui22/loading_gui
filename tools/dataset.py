# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 20:31
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : dataset.py
# @Software: PyCharm
import glob
import os

import cv2.cv2

img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']


class LoadImages:
    def __init__(self, path):
        if os.path.isdir(path):
            files = sorted(glob.glob(os.path.join(path, '*.*')))  # dir
        else:
            raise Exception(f'ERROR: {path} does not exist')
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


if __name__ == '__main__':
    path = r"/db/images"
    # a = r'E:\OneDrive\code\loading\db\images\img_Drone1_0_0_1632635711007055400.png'
    # i = cv2.imread(a)
    data = LoadImages(path)
    for i, img in data:
        cv2.imshow("img", img)
        cv2.waitKey(0)
