import argparse
import socket
import numpy as np
import cv2

def client(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	while True:
		data = sock.recv(100000)
		cv2.imshow('Output', data)
		cv2.waitKey(1)
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and receive over MP-TCP')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,
                        help='TCP port (default 6000)')
    args = parser.parse_args()
    client(args.host, args.p)
