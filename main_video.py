import cv2
import time
import numpy as np

import json


import argparse
import os


import ImageProcessor
import FacesDatabase
from models import utils

parser = argparse.ArgumentParser(description="Video Inference")
parser.add_argument("--ov_path", default="/", type=str, help="path to openvino models")
parser.add_argument("--video_path", default="../video3.mp4", type=str, help="path to the video")

if __name__ == '__main__':
    opt = parser.parse_args()

    with open('model_config.json','r') as f:
        config = json.load(f)

    image_processor = ImageProcessor.FrameDetectionPipeline(opt.ov_path,config)
    image_processor.initialize()

    faces_database = FacesDatabase.LocalFacesDatabase(path='/face/trusted_faces_storage', image_processor=image_processor)
    #image = cv2.imread('../me2.jpg')
    #faces_database.add('Dmitry1',image)
    #image = cv2.imread('../me.png')
    #faces_database.add('Dmitry2', image)

    print('starting video')

    capture = cv2.VideoCapture(opt.video_path)
    has_frame, frame = capture.read()

    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Window', 800, 600)

    #cv2.namedWindow('reid_face', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('reid_face', 800, 600)

    frame_no = 0

    while has_frame:

        if frame_no < 150:
            has_frame, frame = capture.read()
            frame_no += 1
            continue

        if frame_no > 2500:
            break

        start = time.time()

        package = {'image': frame}
        package = image_processor(package)

        end = time.time()
        inf_time = end - start

        ids = []
        distances = []
        for embedding in package['face_id']:
            i, d = faces_database.find(embedding, 5)
            ids.append(i)
            distances.append(d)


        frame = utils.render_gui(package,inf_time, ids, distances)

        cv2.imshow('Window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        has_frame, frame = capture.read()
        frame_no += 1


    #time.sleep(1200)
    print('finished')