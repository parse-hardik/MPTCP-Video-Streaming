import argparse
import socket
import cv2
import struct
import pickle
from threading import Thread

flag = False

def create_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)  # Bind to the port
    sock.listen(64)
    print("Server Listening on {}".format(address))
    return sock

def getFrames(masterSock):
    data = b''
    payload_size = struct.calcsize("L")
    while True:
        while len(data) < payload_size:
            data += masterSock.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += masterSock.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame=pickle.loads(frame_data)
        yield frame

def accept_forever(listener, masterSock, masterAddress):
    count=0
    while True:
        sock, address = listener.accept()
        count+=1
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address, masterSock, masterAddress)

def handle_conversation(sock, address, masterSock, masterAddress):
    try:
        while True:
            handle_request(sock, masterSock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error {}'.format(address,e))
    finally:
        sock.close()

def handle_request(sock, masterSock):
    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     sock.close()
    #     raise IOError("Cannot open webcam")
    # count = 0
    # while True:
    #     ret,frame=cap.read()
    #     count+=1
    #     data = pickle.dumps(frame) ### new code
    #     sock.sendall(struct.pack("L", len(data))+data)
    #     if count > 300:
    #         break
    #     # sock.sendall(frame)
    # cap.release()
    # cv2.destroyAllWindows()
    # sock.close()
    for frame in getFrames(masterSock):     
        data = pickle.dumps(frame) ### new code
        sock.sendall(struct.pack("L", len(data))+data) 

def start(sock, masterAddress, workers=4):
    masterSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    masterSock.connect(masterAddress)
    t = (sock, masterSock, masterAddress)
    for i in range(workers):
        Thread(target=accept_forever, args=t).start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send and receive over MPTCP')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-server', metavar='PORT', type=int, 
                        help='Port number for the master server')
    parser.add_argument('-p', metavar='PORT', type=int, default=6000,
                        help='TCP port (default 6000)')
    args = parser.parse_args()
    sock = create_socket((args.host, args.p))
    start(sock, (args.host, args.server))
