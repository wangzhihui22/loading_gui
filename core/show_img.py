# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 16:01
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : show_img.py
# @Software: PyCharm
import time

import cv2
from PyQt5.QtCore import QThread, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel

from tools.log import logging


class ShowImageThread(QThread):
    update_signal = pyqtSignal(bool)

    def __init__(self, ui_obj):
        super(ShowImageThread, self).__init__()
        self._working = False
        self.ui_obj = ui_obj
        self.target_queue = ui_obj.target_queue
        self.show_img_lbl = QLabel(ui_obj)
        self.ui_obj.img_show.addWidget(self.show_img_lbl)

    def pause(self):
        if self._working:
            self._working = False

    def rouse(self):  # 唤醒
        if not self._working:
            self._working = True

    def set_img(self):
        # 获取一张图片，并且进行处理
        logging.info("展示检测后圖片队列大小:{} ".format(self.target_queue.qsize()))
        img, _ = self.target_queue.get()
        # 每获取一张图片，就发一个信号
        self.update_signal.emit(True)

        # logging.info("圖片队列大小:{} ".format(img.shape))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pyqt = QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3,
                          QImage.Format_RGB888)
        pixmap = QPixmap(img_pyqt)
        w = self.show_img_lbl.width()
        h = self.show_img_lbl.height()
        pixmap = pixmap.scaled(QSize(w, h), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.show_img_lbl.setScaledContents(True)
        self.show_img_lbl.setPixmap(pixmap)

    def run(self):
        while True:
            if self._working:
                self.set_img()
            else:
                logging.info("展示线程睡眠")
                time.sleep(0.1)
