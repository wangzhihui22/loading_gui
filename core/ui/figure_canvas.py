"""
* @Author: Wang.Zhihui  
* @Date: 2020-02-26 01:35:47  
* @Last Modified by:   Wang.Zhihui  
* @Last Modified time: 2020-02-26 01:35:47  
* @function:   绘制二维三维曲线
"""

# 自定义类 QmyFigureCanvas，父类QWidget
# 创建了FigureCanvas和NavigationToolbar，组成一个整体
# 便于可视化设计
import sys
from queue import Queue

from numpy import array
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QTimer, QMargins
from PyQt5.QtWidgets import QWidget
from matplotlib import rcParams
import matplotlib.figure as figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.style as mplStyle  # 一个模块

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D  # 一定不能注释

from PyQt5.QtWidgets import QVBoxLayout
from tools.log import logging
from tools.read_parameter import conf_dic
import matplotlib.image as img
from collections import deque


class QmyFigureCanvas(QWidget):

    def __init__(self, parent=None, toolbarVisible=True, showHint=False):
        # 类初始化
        super().__init__(parent)
        self.showHint = showHint
        self.toolbarVisible = toolbarVisible
        mplStyle.use("classic")  # 使用样式，必须在绘图之前调用,修改字体后才可显示汉字
        rcParams['font.sans-serif'] = ['KaiTi', 'SimHei']  # 显示汉字为 楷体， 汉字不支持 粗体，斜体等设置
        rcParams['font.size'] = 15
        rcParams['axes.unicode_minus'] = False  # 减号unicode编码
        self.xmajorFormatter = FormatStrFormatter('%1.1f')
        self.figure = None  # 二维图的画图对象
        self.ax_3d = None  # 三维画图的对象
        # 坐标轴序列
        self.x = deque()
        self.y = deque()
        self.z = deque()
        self.fig_img = None
        logging.debug("画布初始化完成")

    def limit_length(self):
        if len(self.x) >= conf_dic["plot_length"]:
            self.x.popleft()
            self.y.popleft()
        if len(self.z) >= conf_dic["plot_length"]:
            self.z.popleft()

    #  ==============自定义功能函数========================
    def create_figure(self):
        """
        创建二维画图的画布 ，一般都是这个步骤
        先得到一个mpl.figure.Figure对象 figure
        然后把该对象加入到 Qt留出来的空白画图区
        设置画图为 1 幅
        """
        logging.debug("创建二维画布")
        self.figure = figure.Figure(dpi=40)
        fig_canvas = FigureCanvas(self.figure)  # 创建FigureCanvas对象，必须传递一个Figure对象
        self.figure.subplots_adjust(left=None, bottom=None, right=1, top=1)
        # self.figure.subplots_adjust(bottom=0.17)
        self.ax1 = self.figure.add_subplot(1, 1, 1)
        # (1,1,1)代表为横着为1幅竖着为1幅，第1幅  若是竖着两个子图的第一幅 则为（2，1，1）
        # 设置坐标轴标签的格式这里  self.xmajorFormatter = FormatStrFormatter('%1.1f')，必须这样
        self.ax1.xaxis.set_major_formatter(self.xmajorFormatter)
        self.ax1.yaxis.set_major_formatter(self.xmajorFormatter)
        layout = QVBoxLayout(self)
        layout.addWidget(fig_canvas)  # 添加FigureCanvas对象到空白处
        layout.setContentsMargins(0, 0, 0, 0)  # 这个一般都这么写
        layout.setSpacing(0)

    # 绘制二维曲线
    def draw_fig(self, y_name, x_name, label):  # 初始化绘图
        self.ax1.cla()  # 动态图，更新图要删除上一幅，必须  # , label=label
        self.line_fig = self.ax1.plot(self.x, self.y, '-', linewidth=1)[0]  # 绘制一条曲线
        # self.ax1.set_xlabel(x_name)  # X轴标题
        # self.ax1.set_ylabel(y_name)  # Y轴标题
        self.figure.canvas.draw()

    def update_fig(self, x_num, y_num):
        # self.ax1.cla()
        self.limit_length()
        self.x.append(x_num)
        self.y.append(y_num)
        x_min, x_max = self.get_range(self.x)
        y_min, y_max = self.get_range(self.y)
        self.ax1.set_xlim([x_min, x_max])  # X轴坐标范围
        self.ax1.set_ylim([y_min, y_max])  # Y轴坐标范围
        self.line_fig.set_xdata(self.x)
        self.line_fig.set_ydata(self.y)
        self.figure.canvas.draw()

    @staticmethod
    def get_range(x):
        x_min = min(x)
        x_max = max(x)
        diff = (x_max - x_min)
        if diff < 0.08:
            x_min = x_min - 0.01
            x_max = x_max + 0.01
        x_min = x_min * 0.9
        x_max = x_max * 1.1

        return x_min, x_max

    # 以下画三维，画地图都大同小异
    # 创建三维曲线
    def create_3d_figure(self):
        self.figure = figure.Figure(dpi=40)
        fig_canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(fig_canvas)  # 添加FigureCanvas对象
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # # 3维曲线初始设置
        # def init_3d_figure(self):
        self.figure.clear()
        self.figure.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax_3d = self.figure.add_subplot(1, 1, 1, projection='3d', label="plot3D")

    # 绘制三维图
    def draw_3d_fig(self):
        self.ax_3d.cla()
        self.fig_line_3d = self.ax_3d.plot3D(self.x, self.y, self.z, '-')[0]
        self.ax_3d.set_xlabel("X")
        self.ax_3d.set_ylabel("Y")
        self.ax_3d.set_zlabel("H")
        self.figure.canvas.draw()

    def update_3d_fig(self, x_num, y_num, z_num):
        # ============================注意=======================
        # set_data_3d函数 只有再matplotlib版本大于3.1.2才有
        self.limit_length()
        self.x.append(x_num)
        self.y.append(y_num)
        self.z.append(z_num)
        x_min, x_max = self.get_range(self.x)
        y_min, y_max = self.get_range(self.y)
        z_min, z_max = self.get_range(self.z)
        # minLen = min(len(x),len(y),
        #              len(z))
        # x = x[-minLen:]
        # y = y[-minLen:]
        # z = z[-minLen:]      # 原作用由于多线程会出现数据不对齐的情况，
        # 因此这里强制数据对齐，但后面找到了数据不出现对齐的原因
        self.fig_line_3d.set_data_3d(self.x, self.y, self.z)
        self.ax_3d.set_xlim([x_min, x_max])
        self.ax_3d.set_ylim([y_min, y_max])
        self.ax_3d.set_zlim([z_min, z_max])
        self.figure.canvas.draw()




"""
三维   tracks_show
x_draw
y_draw
height_draw
yaw_draw
pitch_draw
roll_draw

QmyFigureCanvas
myFigureCanvas.h



"""