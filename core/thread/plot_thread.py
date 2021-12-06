# -*- coding: utf-8 -*-
# @Time    : 2021/11/29 15:32
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : plot_thread.py
# @Software: PyCharm
import os
import time

from PyQt5.QtCore import QThread, pyqtSlot
from tools.log import logging

edit = ["x_edit", "y_edit", "height_edit", "roll_edit", "pitch_edit", "yaw_edit"]


class PlotThread(QThread):
    def __init__(self, ui_obj, draw_name=None):
        super().__init__()
        self._close = False
        self.count = 0
        self.ui_obj = ui_obj
        self.draw_name = draw_name
        self.data = None
        # self.init_plot()
        # flight_data_path = os.path.join(get_project_path(), conf_dic["path"]["flight_data"])
        # self.data = LoadFlightData(flight_data_path)
        self.flag = False

    # def init_plot(self):
    #     for i_obj in objs:
    #         logging.debug("初始化{}视图".format(i_obj[:-5]))
    #         getattr(self.ui_obj, i_obj).create_figure()
    #         logging.debug("绘制{}视图第一帧".format(i_obj[:-5]))
    #         getattr(self.ui_obj, i_obj).draw_fig(y_name=dict(zip(objs, labels)).get(i_obj),
    #                                              x_name="帧", label=i_obj[:-5])

    # logging.debug("三维图像展示")
    # self.ui_obj.tracks_show.create_3d_figure()
    # self.ui_obj.tracks_show.draw_3d_fig()
    @pyqtSlot(float)
    def get_2d_data(self, data):
        # logging.debug("获取一次数据{}".format(self.draw_name))
        # self.set_flag()
        self.data = data

    @pyqtSlot(list)
    def get_3d_data(self, data):
        self.data = data
        # logging.debug("3d data {}".format(data))

    def update(self):
        if self.draw_name:
            self.count += 1
            getattr(self.ui_obj, self.draw_name).update_fig(self.count, self.data)
            # x_draw - > x_edit
            if self.draw_name in ["x_draw", "y_draw", "height_draw"]:
                getattr(self.ui_obj, self.draw_name.split("_")[0]+"_edit").setText(
                    "{:>6.2f}".format(self.data)
                )
            else:
                getattr(self.ui_obj, self.draw_name.split("_")[0] + "_edit").setText(
                    "{:>6.4f}".format(self.data)
                )

        else:
            logging.debug("3维绘图更新")
            self.ui_obj.tracks_show.update_3d_fig(self.data[0], self.data[1], self.data[2])

    # self.ui_obj.tracks_show.update_3d_fig(data[0], data[1], data[2])

    def set_flag(self):
        self.flag = True

    def close(self):
        self._close = True
    def run(self):
        while not self._close:
            if self.data:
                logging.debug("更新一次绘图{},第{}帧".format(self.draw_name, self.count))
                start = time.time()
                self.update()
                self.data = None
                end = time.time()
                if end - start < 0.066:
                    time.sleep(0.066 - (end - start))
            else:
                time.sleep(0.03)
