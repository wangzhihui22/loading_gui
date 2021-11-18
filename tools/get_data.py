# -*- coding: utf-8 -*-
# @Time    : 2021/11/18 15:10
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : get_data.py
# @Software: PyCharm
import os.path

from tools.path import get_project_path


class GetData:
    def __init__(self):
        path = "db/imu/airsim_rec.txt"
        path = os.path.join(get_project_path(), path)
        self.all_data = self.read_data(path)

    def read_data(self, path):

        return None


    def get_frame(self):
        pass


