import argparse
import socket
import numpy as np
import cv2
import struct
import pickle


def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    data = b''
    payload_size = struct.calcsize("L") 
    while True:
        while len(data) < payload_size:
            data += sock.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += sock.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        ###

        frame=pickle.loads(frame_data)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sock.close()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send and receive over MP-TCP')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,
                        help='TCP port (default 6000)')
    args = parser.parse_args()
    client(args.host, args.p)
