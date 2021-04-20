import os
import cv2
import numpy as np
import redis

while True:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        break
    raise IOError("Cannot open webcam")

store = redis.Redis()

while True:
    ret, frame = cap.read()
    ret, frame = cv2.imencode('.jpg', frame)
    val = np.array(frame).tobytes()
    store.set('image', val)
    image_id = os.urandom(4)
    store.set('image_id', image_id)
    