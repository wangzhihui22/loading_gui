# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 14:44
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : landing_ground_station.py.py
# @Software: PyCharm

import sys
import os
from queue import Queue

from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from core.ui.plot_figure import Plot

env_path = os.path.join(os.path.dirname(__file__), '../../..')
if env_path not in sys.path:
    sys.path.append(env_path)
from core.thread.detect import DetectBase, DetectThread
from core.thread.show_img import ShowImageThread
from tools.log import logging
from tools.path import get_project_path


class QWelcomeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        project_path = get_project_path()
        ui_file_path = os.path.join(project_path, 'lib/qt/main_window.ui')
        loadUi(ui_file_path, self)
        ico_path = os.path.join(project_path, 'db/icon/uav.ico')
        self.setWindowIcon(QIcon(ico_path))
        logging.info("初始化按钮")
        self.init_btn()
        self.target_queue = self.create_queue(15)
        logging.info("加载runway识别网络")
        self.net = self.load_net()
        logging.info("初始化视景线程")
        self.show_img_tread = self.init_show_img()
        logging.info("初始化检测线程")
        self.detect_tread = self.init_detect()
        logging.info("初始化绘图")
        self._plot = self.plot()
        # 信号与槽函数绑定
        self.show_img_tread.update_signal.connect(self._plot.update_flight_values)

    def init_btn(self):
        self.start_btn.clicked.connect(self.start_simulation)
        self.pause_btn.clicked.connect(self.pause_simulation)
        self.save_btn.clicked.connect(self.save_data)

    def start_simulation(self):
        logging.info("开始按钮按下，开始仿真系统")
        self.show_img_tread.rouse()
        self.detect_tread.rouse()

    def pause_simulation(self):
        logging.info("暂停按钮按下，暂停仿真系统")
        self.show_img_tread.pause()
        self.detect_tread.pause()

    def save_data(self):
        pass

    def plot(self):
        return Plot(self)

    # 创建队列
    @staticmethod
    def create_queue(num):
        return Queue(num)

    # 加载网络函数
    @staticmethod
    def load_net():
        return DetectBase()

    def init_detect(self):
        detect_tread = DetectThread(self.net, self.target_queue)
        detect_tread.daemon = True
        detect_tread.start()
        return detect_tread

    def init_show_img(self):
        show_img_tread = ShowImageThread(self)
        show_img_tread.daemon = True
        show_img_tread.start()
        return show_img_tread

    def closeEvent(self, event):

        dlg_title = u"警告"
        str_info = u"无人机着陆仿真系统正在运行，是否要关闭？"
        default_btn = QMessageBox.NoButton
        result = QMessageBox.question(self, dlg_title, str_info,
                                      QMessageBox.Yes | QMessageBox.No, default_btn)
        if result == QMessageBox.Yes:
            self.detect_tread.close()
            self.show_img_tread.close()
            self._plot.close()
            event.accept()
        else:
            event.ignore()


#  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QWelcomeWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
