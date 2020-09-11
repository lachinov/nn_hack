import numpy as np
from scipy.spatial.distance import cosine

import os
import cv2
import pickle

class LocalFacesDatabase():
    def __init__(self,path, image_processor):
        self.path = path
        self.image_processor = image_processor

        self.database = {}

        try:
            with open(os.path.join(self.path,'database.pkl'), 'rb') as f:
                self.database = pickle.load(f)
        except:
            pass


    def add(self,id, record:np.ndarray):
        if len(record.shape) == 1:
            self.database[id] = record
        elif len(record.shape) == 3:
            package = {'image': record}
            package = self.image_processor(package)

            if package['face_detection_boxes'].shape[0] > 1:
                raise Exception('Detected more that one face')

            self.database[id] = package['face_id'][0]

            os.makedirs(os.path.join(self.path,str(id)),exist_ok=True)

            number_images = len(os.listdir(os.path.join(self.path,str(id))))

            image_to_write = package['face_reid_face'][0].transpose((1,2,0))
            path_to_write = os.path.join(self.path,str(id),str(number_images)+'.png')
            cv2.imwrite(path_to_write,image_to_write)

            with open(os.path.join(self.path,'database.pkl'), 'wb') as f:
                pickle.dump(self.database,f)

            return package

        raise Exception('incorrect record')

    def remove(self,id):
        del self.database[id]

    def exists(self,id):
        return id in self.database


    def find(self, embedding, topk):
        values = list(self.database.values())
        keys = list(self.database.keys())

        distance = []
        for v in values:
            c = cosine(embedding,v)
            dot = np.dot(embedding.T, v)/(np.linalg.norm(embedding)*np.linalg.norm(v))

            distance.append(dot)
        distance = np.array(distance)
        sorted = np.argsort(distance)[::-1]

        s = sorted[:topk]
        k = [keys[idx] for idx in s]
        d = distance[s]

        return k, d
