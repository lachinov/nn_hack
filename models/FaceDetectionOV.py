from typing import *
import numpy as np
import cv2
from openvino.inference_engine import IECore, IENetwork

from . import Model


class SSD_OV(Model.BaseModel):
    def __init__(self,name, xml_path, bin_path, batch_size, detection_threshold, image_key):

        self.name = name
        self.xml_path = xml_path
        self.bin_path = bin_path
        self.detection_threshold = detection_threshold
        self._batch_size = batch_size
        self.image_key = image_key

        # https://github.com/odundar/openvino_python_samples/blob/master/openvino_face_detection.py
        # OpenVinoIE.add_extension('/opt/intel/openvino/inference_engine/lib/intel64/libcpu_extension.so', "CPU")
        self.FaceDetectionNetwork = IENetwork(model=xml_path, weights=bin_path)
        self.FaceDetectionNetwork.batch_size = self._batch_size
        # Get Input Layer Information
        self.FaceDetectionInputLayer = next(iter(self.FaceDetectionNetwork.inputs))
        print("Face Detection Input Layer: ", self.FaceDetectionInputLayer)
        # Get Output Layer Information
        self.FaceDetectionOutputLayer = next(iter(self.FaceDetectionNetwork.outputs))
        print("Face Detection Output Layer: ", self.FaceDetectionOutputLayer)
        # Get Input Shape of Model
        self.FaceDetectionInputShape = self.FaceDetectionNetwork.inputs[self.FaceDetectionInputLayer].shape
        print("Face Detection Input Shape: ", self.FaceDetectionInputShape)
        # Get Output Shape of Model
        self.FaceDetectionOutputShape = self.FaceDetectionNetwork.outputs[self.FaceDetectionOutputLayer].shape
        print("Face Detection Output Shape: ", self.FaceDetectionOutputShape)

    def initialize(self):
        OpenVinoIE = IECore()
        self.FaceDetectionExecutable = OpenVinoIE.load_network(network=self.FaceDetectionNetwork,
                                                               device_name='CPU')
    def infer_shape(self) -> Iterable[int]:
        return self.FaceDetectionInputShape

    def batch_size(self) -> int:
        return self._batch_size

    def preprocess(self, batch:dict) -> dict:
        assert (len(batch[self.image_key].shape)==3)

        N, C, H, W = self.infer_shape()
        resized = cv2.resize(batch[self.image_key], (W, H))
        resized = resized.transpose((2, 0, 1))

        batch[self.name + '_'+self.image_key] = resized
        return batch

    def __call__(self, batch:dict) -> dict:
        image = batch[self.name + '_'+self.image_key]
        size = image.shape[0]
        results = self.FaceDetectionExecutable.infer(inputs={self.FaceDetectionInputLayer: image})['detection_out']


        index = results[0,0,:,2] > self.detection_threshold
        results = results[0,0,index,:]

        bboxes_list = []
        scores_list = []
        for i in range(size):
            index = results[:,0] == i
            image_results = results[index,:]

            bboxes = image_results[:,3:]
            conf = image_results[:,2]
            bboxes_list.append(bboxes)
            scores_list.append(conf)

        batch[self.name+'_boxes'] = bboxes_list
        batch[self.name+'_scores'] = scores_list

        return batch