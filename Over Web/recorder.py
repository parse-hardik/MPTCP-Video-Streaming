import os
import cv2
import numpy as np
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["db"]
col = mydb["image"]

# data = {"name": "Hardik", "age":22}
# x = col.find_one()
# print(x)
val=[]
image_id = os.urandom(4)
col.insert_one({'image': val, 'image_id': image_id})
while True:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        break
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    ret, frame = cv2.imencode('.jpg', frame)
    val = np.array(frame).tobytes()
    # store.set('image', val)
    image_id = os.urandom(4)
    newvalues = { "$set": {'image': val, 'image_id': image_id} }
    # store.set('image_id', image_id)
    col.update_one({}, newvalues)
    x = col.find_one()
    print(x.image, x.image_id)
    print("Done")
    