from ..utils import BaseEngine
import numpy as np
import cv2
import time
import os
import argparse


class TrtPredictor(BaseEngine):
    def __init__(self, engine_path, imgsz=(640, 640)):
        super(TrtPredictor, self).__init__(engine_path)
        self.imgsz = imgsz
        self.mean = None
        self.std = None


class HandPredictor(BaseEngine):
    def __init__(self, engine_path, imgsz=(640, 640)):
        super(HandPredictor, self).__init__(engine_path)
        self.imgsz = imgsz
        self.mean = None
        self.std = None
        self.n_classes = 1
        self.class_names = ['hand']


class HandClassify(BaseEngine):
    def __init__(self, engine_path, imgsz=(224, 224)):
        super(HandClassify, self).__init__(engine_path)
        self.imgsz = imgsz
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        self.n_classes = 3
        self.class_names = ['hand', 'glove', 'background']


class PhoneSegment(BaseEngine):
    def __init__(self, engine_path, imgsz=(640, 640)):
        super(PhoneSegment, self).__init__(engine_path)
        self.imgsz = imgsz
        self.mean = None
        self.std = None
        self.n_classes = 1
        self.class_names = ['CUTWQ']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--engine", type=str, default="weights/hand.trt", help="TRT engine Path")
    parser.add_argument('-c', "--conf", type=float, default=0.01, help='object confidence threshold')
    parser.add_argument('-n', "--nms", type=float, default=0.45, help='iou threshold for the nms')
    parser.add_argument("-i", "--image", type=str, default="images/t1.jpg", help="image path")
    parser.add_argument("-o", "--output", type=str, default="images/hand-t1.jpg", help="image output path")
    parser.add_argument("-v", "--video", help="video path or camera index ")
    parser.add_argument("--end2end", type=bool, default=False, help="use end2end engine")

    args = parser.parse_args()
    print(args)

    pred = TrtPredictor(engine_path=args.engine)
    pred.get_fps()
    img_path = args.image
    video = args.video
    if img_path:
        s = time.time()
        origin_img = pred.detect(img_path, conf=args.conf, iou=args.nms, end2end=args.end2end)
        print("time: ", time.time() - s)
        cv2.imwrite("%s" % args.output, origin_img)
    if video:
        pred.detect_video(video, conf=args.conf, iou=args.nms, end2end=args.end2end)  # set 0 use a webcam
