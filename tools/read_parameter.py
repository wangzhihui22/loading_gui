# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:09
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : read_parameter.py
# @Software: PyCharm
import os
import sys

from yaml import load, FullLoader

cur_path = os.path.dirname(__file__)


def get_yaml_data(yaml_file):
    """
    读取配置文件
    :param yaml_file:  路径
    :return:  配置文件内容
    """
    # 打开yaml文件
    # print("***获取yaml配置文件数据***")
    # print("配置文件路径：", yaml_file)
    if os.path.exists(yaml_file) and (".yaml" in yaml_file or ".yml" in yaml_file):
        file = open(yaml_file, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        data = load(file_data, Loader=FullLoader)
        return data
    else:
        return None


def get_conf(path=os.path.join(cur_path, "../conf/configure.yaml")):
    ret = get_yaml_data(path)
    assert ret is not None
    return ret


conf_dic = get_conf()
