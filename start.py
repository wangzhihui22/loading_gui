# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:06
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : start.py
# @Software: PyCharm
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from core.ui.landing_ground_station import QWelcomeWindow

env_path = os.path.join(os.path.dirname(__file__), '..')
if env_path not in sys.path:
    sys.path.append(env_path)
#  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QWelcomeWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
