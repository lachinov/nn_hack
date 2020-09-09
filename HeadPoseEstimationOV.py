from typing import *
import numpy as np
import cv2
from openvino.inference_engine import IECore, IENetwork

import Model


class HeadPoseEstimationOV(Model.BaseModel):
    def __init__(self,name, xml_path, bin_path, batch_size, image_key):

        self.name = name
        self.xml_path = xml_path
        self.bin_path = bin_path
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
        results = self.FaceDetectionExecutable.infer(inputs={self.FaceDetectionInputLayer: image})

        batch[self.name+'_headpose'] = np.concatenate([results['angle_y_fc'],results['angle_p_fc'],results['angle_r_fc']],axis=1)

        return batch