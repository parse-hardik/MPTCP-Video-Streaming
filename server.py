import argparse
import socket
import cv2
import struct
import pickle

def server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))  # Bind to the port
    sock.listen(64)
    print("Server Listening on {}".format((ip, port)))
    while True:
        conn, addr = sock.accept()     # Establish connection with client.
        print('Got connection from', addr)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            conn.close()
            raise IOError("Cannot open webcam")
        count = 0
        while True:
            ret,frame=cap.read()
            count+=1
            data = pickle.dumps(frame) ### new code
            conn.sendall(struct.pack("L", len(data))+data)
            if count > 300:
                break
            # conn.sendall(frame)
        cap.release()
        cv2.destroyAllWindows()
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send and receive over MP-TCP')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,
                        help='TCP port (default 6000)')
    args = parser.parse_args()
    server(args.host, args.p)
