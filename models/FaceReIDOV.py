from typing import *
import numpy as np
import cv2
from openvino.inference_engine import IECore, IENetwork

from . import Model
from . import utils


class FaceReIDOV(Model.BaseModel):
    REFERENCE_LANDMARKS = np.array([
        (30.2946 / 96, 51.6963 / 112),  # left eye
        (65.5318 / 96, 51.5014 / 112),  # right eye
        (48.0252 / 96, 71.7366 / 112),  # nose tip
        (33.5493 / 96, 92.3655 / 112),  # left lip corner
        (62.7299 / 96, 92.2041 / 112)]  # right lip corner
    )
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
        face = batch[self.image_key]

        h, w, c = batch[self.image_key].shape

        landmarks = np.array(batch['landmarks_detection_landmarks']).reshape((-1,2))
        landmarks = landmarks

        points = np.zeros(shape=(5,2))
        points[0] = (landmarks[0]+landmarks[1])/2
        points[1] = (landmarks[2]+landmarks[3])/2
        points[2] = landmarks[4]
        points[3] = landmarks[8]
        points[4] = landmarks[9]

        face = utils.transform_face(face,landmarks=points, destination_landmarks=self.REFERENCE_LANDMARKS)

        N, C, H, W = self.infer_shape()
        resized = cv2.resize(face, (W, H))
        resized = resized.transpose((2, 0, 1))

        batch[self.name + '_'+self.image_key] = resized
        return batch

    def __call__(self, batch:dict) -> dict:
        image = batch[self.name + '_'+self.image_key]

        results = self.FaceDetectionExecutable.infer(inputs={self.FaceDetectionInputLayer: image})[self.FaceDetectionOutputLayer]

        batch[self.name+'_embedding'] = results.reshape((image.shape[0],-1))

        return batch