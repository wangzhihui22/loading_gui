# -*- coding: utf-8 -*-
# @Time    : 2021/11/18 14:12
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : plot_figure.py
# @Software: PyCharm
from tools.log import logging
from tools.read_parameter import get_conf

objs = ["x_draw", "y_draw", "height_draw", "yaw_draw", "pitch_draw", "roll_draw"]
labels = ["距离", "侧偏", "高度", "俯仰角", "偏航角", "滚转角"]


class Plot:
    def __init__(self, ui_obj):
        logging.debug("总初始化绘图类")
        self.ui_obj = ui_obj
        self.init_plot()

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



    def update(self, data):
        assert (len(data) == 7), "更新数据必须等于7"
        # ["x_draw", "y_draw", "height_draw", "yaw_draw", "pitch_draw", "roll_draw"]
        logging.debug("更新二维绘图")
        for i in range(len(objs)):
            getattr(self.ui_obj, objs[i]).update(data[0], data[i+1])

        logging.debug("更新三维绘图")
        self.ui_obj.tracks_show.update_3d_fig(data[1], data[2], data[3])




