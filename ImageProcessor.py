import os
import numpy as np

from models import FaceDetectionOV, EmotionRecognitionOV, LandmarksDetectionOV, HeadPoseEstimationOV, OpenClosedEyeOV, GazeEstimationOV

import custom_collate
from models import utils

class FrameDetectionPipeline():
    def __init__(self, ov_path, config):
        self.config = config
        self.ov_path = ov_path

        self.face_detection_model = FaceDetectionOV.SSD_OV('face_detection',
                                                      os.path.join(ov_path, config['face_detection']['path'][0]),
                                                      os.path.join(ov_path, config['face_detection']['path'][1]),
                                                      config['face_detection']['batch_size'],
                                                      config['face_detection']['detection_threshold'],
                                                      image_key='image')
        self.person_detection_model = FaceDetectionOV.SSD_OV('person_detection',
                                                        os.path.join(ov_path,
                                                                     config['person_detection']['path'][0]),
                                                        os.path.join(ov_path,
                                                                     config['person_detection']['path'][1]),
                                                        config['person_detection']['batch_size'],
                                                        config['person_detection']['detection_threshold'],
                                                        image_key='image')
        self.landmarks_detection_model = LandmarksDetectionOV.LandmarksDetectionOV('landmarks_detection',
                                                                              os.path.join(ov_path,
                                                                                           config['facial_landmarks'][
                                                                                               'path'][0]),
                                                                              os.path.join(ov_path,
                                                                                           config['facial_landmarks'][
                                                                                               'path'][1]),
                                                                              config['facial_landmarks']['batch_size'],
                                                                              image_key='face')
        self.emotion_recognition_model = EmotionRecognitionOV.EmotionRecognitionOV('emotion_recognition',
                                                                              os.path.join(ov_path, config[
                                                                                  'emotion_recognition']['path'][0]),
                                                                              os.path.join(ov_path, config[
                                                                                  'emotion_recognition']['path'][1]),
                                                                              config['emotion_recognition'][
                                                                                  'batch_size'], image_key='face')
        self.headpose_estimation_model = HeadPoseEstimationOV.HeadPoseEstimationOV('headpose_estimation',
                                                                              os.path.join(ov_path, config[
                                                                                  'headpose_estimation']['path'][0]),
                                                                              os.path.join(ov_path, config[
                                                                                  'headpose_estimation']['path'][1]),
                                                                              config['headpose_estimation'][
                                                                                  'batch_size'], image_key='face')
        self.open_closed_eye_model = OpenClosedEyeOV.OpenClosedEyeOV('open_closed_eye',
                                                                              os.path.join(ov_path, config[
                                                                                  'open_closed_eye']['path'][0]),
                                                                              os.path.join(ov_path, config[
                                                                                  'open_closed_eye']['path'][1]),
                                                                              config['open_closed_eye'][
                                                                                  'batch_size'], image_key='eyes')
        self.gaze_estimation_model = GazeEstimationOV.GazeEstimationOV('gaze_estimation',
                                                                              os.path.join(ov_path, config[
                                                                                  'gaze_estimation']['path'][0]),
                                                                              os.path.join(ov_path, config[
                                                                                  'gaze_estimation']['path'][1]),
                                                                              config['gaze_estimation'][
                                                                                  'batch_size'], image_key='eyes')

    def initialize(self):
        print('FrameDetectionPipeline: loading')
        self.emotion_recognition_model.initialize()
        self.face_detection_model.initialize()
        self.person_detection_model.initialize()
        self.landmarks_detection_model.initialize()
        self.headpose_estimation_model.initialize()
        self.open_closed_eye_model.initialize()
        self.gaze_estimation_model.initialize()
        print('FrameDetectionPipeline: finished loading')


    def __call__(self, package:dict) -> dict:

        fh, fw, fc = package['image'].shape
        package = self.person_detection_model.preprocess(package)
        package = self.face_detection_model.preprocess(package)
        batch = custom_collate.default_collate([package])
        #batch = self.person_detection_model(batch)
        batch = self.face_detection_model(batch)
        package = custom_collate.inverse_collate(batch, 0)

        package['face_detection_boxes'] = utils.adjust_boxes(package['face_detection_boxes'], 0.02)
        package = utils.filter_boxes('face_detection', package, fw, fh)
        #package = utils.filter_boxes('person_detection', package, fw, fh)

        emotions = []
        landmarks = []
        headpose = []
        leyes = []
        lboxes = []
        reyes = []
        rboxes = []
        faces = []
        closed_eyes = []
        gaze = []
        eye_middle = []

        for idx, b in enumerate(package['face_detection_boxes']):
            package_face = {'face': utils.cut_box(package['image'], b)}

            package_face = self.emotion_recognition_model.preprocess(package_face)
            package_face = self.headpose_estimation_model.preprocess(package_face)
            package_face = self.landmarks_detection_model.preprocess(package_face)

            batch = custom_collate.default_collate([package_face])
            batch = self.emotion_recognition_model(batch)
            batch = self.headpose_estimation_model(batch)
            batch = self.landmarks_detection_model(batch)
            package_face = custom_collate.inverse_collate(batch, 0)

            leye, lbox, lmiddle, reye, rbox, rmiddle, roll = utils.cut_eye(package_face['face'], package_face['headpose_estimation_headpose'],
                                       package_face['landmarks_detection_landmarks'])

            package_face['eyes'] = (leye, reye)
            package_face['eye_middle'] = (lmiddle, rmiddle)
            package_face = self.open_closed_eye_model.preprocess(package_face)
            package_face = self.gaze_estimation_model.preprocess(package_face)
            batch = custom_collate.default_collate([package_face])
            batch = self.open_closed_eye_model(batch)
            batch = self.gaze_estimation_model(batch)
            package_face = custom_collate.inverse_collate(batch, 0)

            package_face['gaze_estimation_gaze'] = utils.rotate_gaze(package_face['gaze_estimation_gaze'],roll)


            emotion = np.argmax(package_face['emotion_recognition_emotions']).item()

            landmarks.append(package_face['landmarks_detection_landmarks'])
            headpose.append(package_face['headpose_estimation_headpose'])
            emotions.append(emotion)
            leyes.append(leye)
            lboxes.append(lbox)
            rboxes.append(rbox)
            reyes.append(reye)
            faces.append(package_face['face'])
            closed_eyes.append(package_face['open_closed_eye_closed'])
            gaze.append(package_face['gaze_estimation_gaze'])
            eye_middle.append(package_face['eye_middle'])

        package['emotions'] = emotions
        package['landmarks'] = landmarks
        package['headpose'] = headpose
        package['leyes'] = leyes
        package['lbox'] = lboxes
        package['reyes'] = reyes
        package['rbox'] = rboxes
        package['face'] = faces
        package['closed_eyes'] = closed_eyes
        package['gaze'] = gaze
        package['eye_middle'] = eye_middle

        return package