import cv2
import numpy as np
# import socket
import sys
#import pickle
#import struct

cap=cv2.VideoCapture(0)
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect(('localhost',8089))
# data = b'' ### CHANGED
# payload_size = struct.calcsize("L") ### CHANGED
while True:
    ret,frame=cap.read()
    # Serialize frame
    # data = pickle.dumps(frame)

    # Send message length first
    # message_size = struct.pack("L", len(data)) ### CHANGED

    # Then data
    # clientsocket.sendall(message_size + data)
    # frame = pickle.loads(frame)
    cv2.imshow('frame', frame)
    print(sys.getsizeof(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
