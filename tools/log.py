# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:27
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : log.py
# @Software: PyCharm
import os.path

from loguru import logger

from tools.path import get_project_path
from tools.read_parameter import conf_dic


def set_log():
    level = conf_dic["log_level"]
    log_path = os.path.join(get_project_path(), "./db/log/log_{time}.log")
    logger.add(log_path,
               # format="{time} {level} {message}",
               level=level,
               encoding='utf-8',
               enqueue=True)
    return logger


logging = set_log()
