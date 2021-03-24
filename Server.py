import sys
import socket
from ServerWorker import ServerWorker

class Server:
    def run(self):
        try:
            PORT = int(sys.argv[1])
        except:
            print("Usage Server.py <PORT Number>")
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('localhost', PORT))
        rtspSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rtspSocket.listen(64)
        rtpSocket= socket.socket(socket.AF_INET, socket.DGRAM)
        # rtpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rtpSocket.bind(('localhost', 6000))
        rtpSocket.listen(64)
        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()  
            clientInfo['rtpSocket']  = rtpSocket.accept()
            ServerWorker(clientInfo).run()

if __name__ == "__main__":
    Server().run()