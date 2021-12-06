# -*- coding: utf-8 -*-
# @Time    : 2021/11/18 14:12
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : plot_figure.py
# @Software: PyCharm
import os
import time
from queue import Queue

import numpy as np
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

from core.thread.plot_thread import PlotThread
from tools.dataset import LoadFlightData
from tools.log import logging
from tools.path import get_project_path
from tools.read_parameter import get_conf, conf_dic

objs = ["x_draw", "y_draw", "height_draw", "roll_draw", "pitch_draw", "yaw_draw"]
labels = ["距离", "侧偏", "高度", "俯仰角", "偏航角", "滚转角"]


data_2d_signal = ["x_draw_data_signal", "y_draw_data_signal", "height_draw_data_signal",
                  "roll_draw_data_signal", "pitch_draw_data_signal", "yaw_draw_data_signal"]


class Plot(QThread):
    x_draw_data_signal = pyqtSignal(float)
    y_draw_data_signal = pyqtSignal(float)
    height_draw_data_signal = pyqtSignal(float)
    roll_draw_data_signal = pyqtSignal(float)
    pitch_draw_data_signal = pyqtSignal(float)
    yaw_draw_data_signal = pyqtSignal(float)
    data_3d_signal = pyqtSignal(list)

    def __init__(self, ui_obj):
        super().__init__()
        logging.debug("总初始化绘图类")
        self.ui_obj = ui_obj
        self.init_plot()
        flight_data_path = os.path.join(get_project_path(), conf_dic["path"]["flight_data"])
        self.data = LoadFlightData(flight_data_path)
        self.thread = [None] * (len(objs) + 1)
        self.queue_data = [None] * (len(objs) + 1)
        self.count = 0
        self._flag = False
        self.init_thread()
        for i in range(len(data_2d_signal)):
            getattr(self, data_2d_signal[i]).connect(self.thread[i].get_2d_data)
        self.data_3d_signal.connect(self.thread[6].get_3d_data)
        self.start_thread()

    def init_plot(self):
        for i_obj in objs:
            logging.debug("初始化{}视图".format(i_obj[:-5]))
            getattr(self.ui_obj, i_obj).create_figure()
            logging.debug("绘制{}视图第一帧".format(i_obj[:-5]))
            getattr(self.ui_obj, i_obj).draw_fig(y_name=dict(zip(objs, labels)).get(i_obj),
                                                 x_name="帧", label=i_obj[:-5])

        logging.debug("三维图像展示")
        self.ui_obj.tracks_show.create_3d_figure()
        self.ui_obj.tracks_show.draw_3d_fig()

    def init_thread(self):
        for i in range(len(objs)):
            self.thread[i] = PlotThread(self.ui_obj, objs[i])
            self.thread[i].daemon = True

        self.thread[len(objs)] = PlotThread(self.ui_obj)
        self.thread[len(objs)].daemon = True

    def start_thread(self):
        for i in range(len(objs)):
            self.thread[i].start()
        self.thread[6].start()

    @pyqtSlot(bool)
    def update_flight_values(self, flag):
        try:

            data = next(self.data)
            for i in range(len(data_2d_signal)):
                getattr(self, data_2d_signal[i]).emit(data[i])
            self.data_3d_signal.emit(data[:3].tolist())
        except StopIteration:
            self.data.reset()
            logging.info("处理完毕重新处理")
        self.count += 1
    def close(self):
        for t in self.thread:
            t.close()

