import numpy as np

import cv2

from . import EmotionRecognitionOV

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

    box[0] -= 2*percent*w
    box[1] -= 4*percent*h#*4

    box[2] += 2*percent*w
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

    return leye, lbox, lmiddle, reye, rbox, rmiddle, roll

def rotate_gaze(gaze, roll):
    sin = np.sin(roll*np.pi/180)
    cos = np.cos(roll*np.pi/180)

    x = gaze[0]*cos + gaze[1]*sin
    y = -gaze[0]*sin + gaze[1]*cos

    gaze[0] = x
    gaze[1] = y

    return gaze

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

# copied from re-id demo
def normalize(array, axis):
    mean = array.mean(axis=axis)
    array -= mean
    std = array.std()
    array /= std
    return mean, std

def get_transform(src, dst):
    assert np.array_equal(src.shape, dst.shape) and len(src.shape) == 2, \
            "2d input arrays are expected, got %s" % (src.shape)
    src_col_mean, src_col_std = normalize(src, axis=(0))
    dst_col_mean, dst_col_std = normalize(dst, axis=(0))

    u, _, vt = np.linalg.svd(np.matmul(src.T, dst))
    r = np.matmul(u, vt).T

    transform = np.empty((2, 3))
    transform[:, 0:2] = r * (dst_col_std / src_col_std)
    transform[:, 2] = dst_col_mean.T - \
        np.matmul(transform[:, 0:2], src_col_mean.T)
    return transform

def transform_face(face, landmarks, destination_landmarks):
    h, w, c = face.shape

    size = np.array([[w,h]])
    landmarks = landmarks.copy()*size
    destination_landmarks = destination_landmarks.copy()*size
    transform = get_transform(destination_landmarks, landmarks)

    face = cv2.warpAffine(face, transform, (w,h), flags=cv2.WARP_INVERSE_MAP)
    return face


def render_gui(package, inf_time, ids, distances):
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

        c_open = (0,255,0)
        c_closed = (0,0,255)

        l_state = package['closed_eyes'][idx][0,0] > package['closed_eyes'][idx][0,1]
        r_state = package['closed_eyes'][idx][1,0] > package['closed_eyes'][idx][1,1]

        lc = c_open
        rc = c_open
        if l_state:
            lc = c_closed

        if r_state:
            rc = c_closed

        lbox = package['lbox'][idx]
        rbox = package['rbox'][idx]
        cv2.rectangle(frame, (xmin+lbox[0], ymin+lbox[1]), (xmin+lbox[2], ymin+lbox[3]), lc, 1)
        cv2.rectangle(frame, (xmin + rbox[0], ymin + rbox[1]), (xmin + rbox[2], ymin + rbox[3]), rc, 1)



        gaze = package['gaze'][idx]
        eye_middle = package['eye_middle'][idx]
        gaze[1] = -gaze[1]

        gaze = 0.4*gaze*(xmax-xmin)

        cv2.arrowedLine(frame, (int(xmin+eye_middle[0][0]), int(ymin+eye_middle[0][1])),
                        (int(xmin+eye_middle[0][0]+gaze[0]), int(ymin+eye_middle[0][1]+gaze[1])),(255,0,0),2)
        cv2.arrowedLine(frame, (int(xmin+eye_middle[1][0]), int(ymin+eye_middle[1][1])),
                        (int(xmin+eye_middle[1][0]+gaze[0]), int(ymin+eye_middle[1][1]+gaze[1])),(255,0,0),2)


        #eye = package['leyes'][idx].copy()
        #print('eye state:',package['closed_eyes'][idx][0] < package['closed_eyes'][idx][1])
        #cv2.putText(eye, str(package['closed_eyes'][idx]), (5, 10), cv2.FONT_HERSHEY_COMPLEX, 0.1, (0, 0, 255), 1)

        #reid_face = package['reid_face'][idx]
        #cv2.imshow('reid_face', reid_face.transpose((1,2,0)))

        #cv2.imshow('LEye', eye)
        #cv2.imshow('LEye', package['face'][idx])
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        #cv2.waitKey(1)

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

        #emotion_text[:4]+
        text = '{} {:.2f}'.format(ids[idx][0],distances[idx][0])
        cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1)

    #for idx, b in enumerate(package['person_detection_boxes']):
    #    xmin = int(b[0] * fw)  # int(b[0] * fw / W)
    #    ymin = int(b[1] * fh)
    #    xmax = int(b[2] * fw)
    #    ymax = int(b[3] * fh)

    #    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

    return frame