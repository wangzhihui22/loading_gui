import argparse
import logging
import time
from pathlib import Path

import os
import sys
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
env_path = os.path.join(os.path.dirname(__file__), './')
if env_path not in sys.path:
    sys.path.append(env_path)
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages, letterbox
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box, \
    polygon_non_max_suppression, polygon_scale_coords

from utils.plots import colors, plot_one_box, polygon_plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

import subprocess as sp
import os


def get_gpu_memory():
    _output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    COMMAND1 = "nvidia-smi --query-gpu=memory.free --format=csv"
    COMMAND2 = "nvidia-smi --query-gpu=memory.used --format=csv"
    COMMAND3 = "nvidia-smi --query-gpu=memory.total --format=csv"
    memory_free_info = _output_to_list(sp.check_output(COMMAND1.split()))[1:]
    memory_free_values = [int(x.split()[0]) / 1024 for i, x in enumerate(memory_free_info)]
    memory_used_info = _output_to_list(sp.check_output(COMMAND2.split()))[1:]
    memory_used_values = [int(x.split()[0]) / 1024 for i, x in enumerate(memory_used_info)]
    memory_total_info = _output_to_list(sp.check_output(COMMAND3.split()))[1:]
    memory_total_values = [int(x.split()[0]) / 1024 for i, x in enumerate(memory_total_info)]
    print(f'{"Used":18s}\t{"Free":18s}\t{"Total":18s}')
    for free, used, total in zip(memory_free_values, memory_used_values, memory_total_values):
        print(f'{used:.3f} {"GB": <6s}{used / total:<9.2%}\t{free:.3f} {"GB": <6s}{free / total:<9.2%}\t{total:.2f}')


@torch.no_grad()
def init_model(weights="polygon-yolov5s-ucas.pt",
               imgsz=640,
               device='0'):
    device = select_device(device)
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    names = model.module.names if hasattr(model, 'module') else model.names
    return model, imgsz, names, device, stride


@torch.no_grad()
def run_detect(model,
                  # path,  # BGR img0 = cv2.imread(path)
                  img0,
                  imgsz,
                  stride,
                  names,
                  device,
                  txt_path="",
                  conf_thres=0.25,
                  iou_thres=0.45,
                  classes=None,
                  agnostic_nms=False,
                  max_det=1000,
                  hide_labels=False,
                  hide_conf=False,
                  line_thickness=3,
                  save_txt=False,
                  save_conf=False
                  ):

    # img0 = cv2.imread(path)
    img = letterbox(img0, imgsz, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    t1 = time_synchronized()
    pred = model(img, augment=False)[0]
    # Apply polygon NMS
    # print()
    pred = polygon_non_max_suppression(pred, conf_thres, iou_thres,
                                       classes=classes,
                                       agnostic=agnostic_nms,
                                       max_det=max_det)

    t2 = time_synchronized()

    #   推理结束， 后期处理
    det = pred[0]
    s, im0 = "", img0.copy()
    s += '%gx%g ' % img.shape[2:]
    gn = torch.tensor(im0.shape)[[1, 0, 1, 0, 1, 0, 1, 0]]  # normalization gain xyxyxyxy
    if len(det):
        # Rescale boxes from img_size to im0 size
        det[:, :8] = polygon_scale_coords(img.shape[2:], det[:, :8], im0.shape).round()
        # Print results
        for c in det[:, -1].unique():
            n = (det[:, -1] == c).sum()  # detections per class
            s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

        for *xyxyxyxy, conf, cls in reversed(det):
            # 保存文字
            if save_txt:
                xyxyxyxyn = (torch.tensor(xyxyxyxy).view(1, 8) / gn).view(-1).tolist()  # normalized xyxyxyxy
                line = (cls, *xyxyxyxyn, conf) if save_conf else (cls, *xyxyxyxyn)  # label format
                with open(txt_path + '.txt', 'a') as f:
                    f.write(('%g ' * len(line)).rstrip() % line + '\n')

            # 画框
            c = int(cls)  # integer class
            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
            polygon_plot_one_box(torch.tensor(xyxyxyxy).cpu().numpy(),
                                 im0, label=label,
                                 color=colors(c, True),
                                 line_thickness=line_thickness)

    print(f'{s}Done. ({t2 - t1:.3f}s)')
    # cv2.imshow("img", im0)
    # cv2.waitKey(0)
    return im0, det


if __name__ == '__main__':
    model, imgsz, names, device, stride = init_model()
    ret = run_detect(model=model,
                        path=r"E:\OneDrive\code\loading\lib\polygon_yolov5\data\images\bus.jpg",
                        # BGR img0 = cv2.imread(path)
                        imgsz=imgsz,
                        stride=stride,
                        names=names,
                        device=device,
                        conf_thres=0.25,
                        iou_thres=0.45,
                        classes=None,
                        agnostic_nms=False,
                        max_det=1000
                        )
