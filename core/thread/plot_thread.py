# -*- coding: utf-8 -*-
# @Time    : 2021/11/29 15:32
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : plot_thread.py
# @Software: PyCharm
import os
import time

from PyQt5.QtCore import QThread

from tools.dataset import LoadFlightData
from tools.log import logging
from tools.path import get_project_path
from tools.read_parameter import get_conf, conf_dic


# class Plot(QThread):
#     def __init__(self, ui_obj):
#         super().__init__()
#         logging.debug("总初始化绘图类")
#         self.ui_obj = ui_obj
#         # self.init_plot()
#         # flight_data_path = os.path.join(get_project_path(), conf_dic["path"]["flight_data"])
#         # self.data = LoadFlightData(flight_data_path)
#         # self.count = 0
#         self._flag = False
#
#     # def init_plot(self):
#     #     for i_obj in objs:
#     #         logging.debug("初始化{}视图".format(i_obj[:-5]))
#     #         getattr(self.ui_obj, i_obj).create_figure()
#     #         logging.debug("绘制{}视图第一帧".format(i_obj[:-5]))
#     #         getattr(self.ui_obj, i_obj).draw_fig(y_name=dict(zip(objs, labels)).get(i_obj),
#     #                                              x_name="帧", label=i_obj[:-5])
#
#         # logging.debug("三维图像展示")
#         # self.ui_obj.tracks_show.create_3d_figure()
#         # self.ui_obj.tracks_show.draw_3d_fig()
#
#     def update(self):
#         data = next(self.data)
#         self.count += 1
#         assert (len(data) == 6), "更新数据必须等于6"
#         # data[0], data[1], data[2] :x , y , z  滚转角 俯仰角 偏航角
#         # objs = ["x_draw", "y_draw", "height_draw"]
#         logging.debug("更新二维绘图{}".format(self.count))
#         for i in range(len(objs)):
#             getattr(self.ui_obj, objs[i]).update_fig(self.count, data[i])
#             # 更新值setText()
#             getattr(self.ui_obj, edit[i]).setText("{:>6.2f}".format(data[i])
#                                                   if i < 3
#                                                   else "{:>6.5f}".format(data[i])
#                                                   )
#         # logging.debug("更新三维绘图")
#         self.ui_obj.tracks_show.update_3d_fig(data[0], data[1], data[2])
#
#     def set_flag(self):
#         self._flag = True
#
#     def run(self):
#         while True:
#             if self._flag:
#                 self._flag = False
#                 self.update()
#             else:
#                 time.sleep(0.04)
