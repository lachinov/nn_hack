import numpy as np

import cv2

import EmotionRecognitionOV

def cut_box(image, box):
    fh, fw, fc = image.shape

    xmin = int(box[0] * fw)  # int(b[0] * fw / W)
    ymin = int(box[1] * fh)
    xmax = int(box[2] * fw)
    ymax = int(box[3] * fh)

    face = image[ymin:ymax, xmin:xmax, :]

    return face

def cut_box_absolute(image, box):
    fh, fw, fc = image.shape

    xmin = np.clip(box[0] ,0, fw)  # int(b[0] * fw / W)
    ymin = np.clip(box[1] ,0, fh)
    xmax = np.clip(box[2] ,0, fw)
    ymax = np.clip(box[3] ,0, fh)

    face = image[ymin:ymax, xmin:xmax, :]

    return face


def adjust_box(box, percent):
    w = (box[2]-box[0])
    h = (box[3]-box[1])

    box[0] -= percent*w
    box[1] -= 4*percent*h

    box[2] += percent*w
    box[3] += percent*h

    return box

def adjust_boxes(boxes, percent):
    for idx in range(boxes.shape[0]):
        boxes[idx] = adjust_box(boxes[idx],percent)

    return boxes

def cut_eye(face, headpose, landmarks):
    scale = 0.8
    face_size = np.array(face.shape)[:2][::-1]
    p1 = landmarks[0:2] * face_size
    p2 = landmarks[2:4] * face_size

    p3 = landmarks[4:6] * face_size
    p4 = landmarks[6:8] * face_size

    roll = headpose[2]

    mat = cv2.getRotationMatrix2D(center=tuple(face_size//2),angle=roll,scale=1)
    face = cv2.warpAffine(face, mat, tuple(face_size),borderMode=cv2.BORDER_REPLICATE)
    p1 = np.dot(mat, np.concatenate([p1,[1]],axis=0))
    p2 = np.dot(mat, np.concatenate([p2,[1]],axis=0))
    p3 = np.dot(mat, np.concatenate([p3,[1]],axis=0))
    p4 = np.dot(mat, np.concatenate([p4,[1]],axis=0))

    p2 = (p2 + (p2-p1)*scale)
    lsize = np.sqrt(np.sum((p1 - p2)**2))
    lmiddle = (p1+p2)/2

    p4 = (p4 + (p4-p3)*scale)
    rsize = np.sqrt(np.sum((p3 - p4) ** 2))
    rmiddle = (p3 + p4) / 2

    lbox = (lmiddle - lsize / 2).astype(np.int32).tolist() + (lmiddle + lsize / 2).astype(np.int32).tolist()
    rbox = (rmiddle - rsize / 2).astype(np.int32).tolist() + (rmiddle + rsize / 2).astype(np.int32).tolist()

    leye = cut_box_absolute(face, lbox)
    reye = cut_box_absolute(face, rbox)

    return leye, reye


def filter_boxes(name, batch: dict, fw, fh) -> dict:
    new_boxes = []
    new_scores = []
    for idx, (b, s) in enumerate(zip(batch[name+'_boxes'], batch[name+'_scores'])):
        b = np.clip(b, 0, 1)
        xmin = int(b[0] * fw)  # int(b[0] * fw / W)
        ymin = int(b[1] * fh)
        xmax = int(b[2] * fw)
        ymax = int(b[3] * fh)

        if (xmax - xmin) * (ymax - ymin) > 25:
            new_boxes.append(b)
            new_scores.append(s)

    batch[name+'_boxes'] = np.stack(new_boxes) if len(new_boxes) > 0 else []
    batch[name+'_scores'] = np.stack(new_scores) if len(new_boxes) > 0 else []

    return batch

def render_gui(package, inf_time):
    fps = 1. / inf_time
    frame = package['image'].copy()
    fh, fw, fc = frame.shape
    text = 'Face Detection - FPS: {}, INF: {}'.format(round(fps, 2), round(inf_time, 4))
    cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 125, 255), 1)

    for idx, (b, e, l, hp) in enumerate(
            zip(package['face_detection_boxes'], package['emotions'], package['landmarks'], package['headpose'])):
        xmin = int(b[0] * fw)  # int(b[0] * fw / W)
        ymin = int(b[1] * fh)
        xmax = int(b[2] * fw)
        ymax = int(b[3] * fh)

        emotion_text = EmotionRecognitionOV.emotions_keys[e]

        for l_idx in range(l.size // 2):
            x, y = l[2 * l_idx], l[2 * l_idx + 1]

            x = int(xmin + x * (xmax - xmin))
            y = int(ymin + y * (ymax - ymin))

            cv2.circle(frame, (x, y), radius=3, color=(0, 255, 0), thickness=-1)

        #cv2.imshow('LEye', package['reyes'][idx])
        #cv2.imshow('LEye', package['face'][idx])
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        # cv2.waitKey(1)

        yaw, pitch, roll = hp

        sin_hp = np.sin(hp * np.pi / 180)
        cos_hp = np.cos(hp * np.pi / 180)

        cosY, cosP, cosR = cos_hp
        sinY, sinP, sinR = sin_hp

        axisLength = 0.4 * (xmax - xmin)
        x_center = (xmax + xmin) // 2
        y_center = (ymax + ymin) // 2

        cv2.line(frame, (x_center, y_center), (
        x_center + int(axisLength * (cosR * cosY + sinY * sinP * sinR)), y_center + int(axisLength * cosP * sinR)),
                 (0, 0, 255), 3)
        cv2.line(frame, (x_center, y_center), (
        x_center + int(axisLength * (cosR * sinY * sinP + cosY * sinR)), y_center - int(axisLength * cosP * cosR)),
                 (0, 255, 0), 3)
        cv2.line(frame, (x_center, y_center),
                 (x_center + int(axisLength * sinY * cosP), y_center + int(axisLength * sinP)), (255, 0, 255), 3)

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 125, 255), 3)
        cv2.putText(frame, emotion_text, (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    for idx, b in enumerate(package['person_detection_boxes']):
        xmin = int(b[0] * fw)  # int(b[0] * fw / W)
        ymin = int(b[1] * fh)
        xmax = int(b[2] * fw)
        ymax = int(b[3] * fh)

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

    return frame