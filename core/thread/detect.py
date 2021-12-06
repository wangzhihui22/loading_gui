# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 16:28
# @Author  : Wang.Zhihui
# @Email   : w-zhihui@qq.com
# @File    : detect.py
# @Software: PyCharm
import os.path
import time

from PyQt5.QtCore import QThread

from tools.dataset import LoadImages

from tools.log import logging
from tools.path import get_project_path
from tools.read_parameter import conf_dic

from lib.polygon_yolov5.runway_detect import init_model, run_detect


class DetectBase:
    def __init__(self):
        path = conf_dic["path"]["model_path"]
        path = os.path.join(get_project_path(), path)

        self.weights = path
        self.imgsz = 640
        self.device = '0'
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.classes = None
        self.agnostic_nms = False
        self.max_det = 1000

        self.model, self.imgsz, self.names, self.device, self.stride = init_model(weights=self.weights,
                                                                                  imgsz=self.imgsz, device=self.device)

    def detect_run(self, img):
        # try:
        detections = run_detect(model=self.model,
                                img0=img,
                                imgsz=self.imgsz,
                                stride=self.stride,
                                names=self.names,
                                device=self.device,
                                conf_thres=self.conf_thres,
                                iou_thres=self.iou_thres,
                                classes=self.classes,
                                agnostic_nms=self.agnostic_nms,
                                max_det=self.max_det
                                )
        return detections
        # except:
        #     logging.error("检测出错，返回None")
        #     return None


class DetectThread(QThread):
    # detect_result_signal = pyqtSignal(list)

    def __init__(self, net_obj, target_queue=None):
        super(DetectThread, self).__init__()

        img_path = os.path.join(get_project_path(), conf_dic["path"]["img_path"])
        self.dataset = LoadImages(img_path)

        self.net_obj = net_obj
        self.target_queue = target_queue
        self._close = False
        self._working = False
        self._count = 0

    def close(self):
        self._close = True

    def pause(self):
        if self._working:
            self._working = False

    def rouse(self):  # 唤醒
        if not self._working:
            self._working = True

    def run(self):
        # while not self.target_queue.empty():
        #     self.target_queue.get()
        while not self._close:
            if self._working:
                start = time.time()
                try:
                    path, img_rgb = next(self.dataset)
                    img, ret = self.net_obj.detect_run(img_rgb)
                    logging.info("结果放入队列")
                    self.target_queue.put((img, ret))
                    logging.debug("检测线程完成一张图片检测")
                except StopIteration:
                    logging.info("检测图片结束")
                    self.dataset.reset()
                end = time.time()
                if end - start < 0.066:
                    time.sleep(0.066 - (end-start))
            else:
                logging.info("检测线程睡眠")
                time.sleep(0.1)
            # [('person', '69.61', (209.58120727539062, 239.00148010253906, 309.14349365234375, 402.7058410644531))]
            # 这里不没帧都发
            # self._count += 1
            # if self._count == 16:
            #     self.detect_result_signal.emit([ret, image])  # 这里只负责把结果发出去，具体操作由使用房控制
            #     self._count = 0


if __name__ == '__main__':
    runway = DetectBase()
    th = DetectThread(runway)
    th.start()
    time.sleep(10000)
