import argparse
import socket
import cv2
import struct
import pickle

def create_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)  # Bind to the port
    sock.listen(64)
    print("Server Listening on {}".format(address))
    return sock

def start(listener):
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock,address)

def handle_conversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error {}'.format(address,e))
    finally:
        sock.close()

def handle_request(sock):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    count = 0
    while True:
        ret,frame=cap.read()
        count+=1
        data = pickle.dumps(frame) ### new code
        sock.sendall(struct.pack("L", len(data))+data)
        if count > 300:
            break
        # sock.sendall(frame)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Send and receive over MP-TCP')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=5000,
                        help='TCP port (default 5000)')
    args = parser.parse_args()
    sock = create_socket((args.host, args.p))
    start(sock)