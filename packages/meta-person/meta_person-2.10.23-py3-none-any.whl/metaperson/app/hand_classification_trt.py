import cv2
from ..model_zoo import HandClassify


class HandClassificationTrt:
    def __init__(self,
                 trt_file="models/hand-cls.trt",
                 input_shape=(224, 224)):
        self.model = HandClassify(engine_path=trt_file, imgsz=input_shape)

    def predict(self, image):
        pred = self.model.classfy(image)
        return pred
