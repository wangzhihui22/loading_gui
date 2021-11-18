# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:24
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : path.py.py
# @Software: PyCharm
import os

cur_path = os.path.dirname(__file__)


def get_project_path():
    return os.path.join(cur_path, "../")


