import sys, threading, socket

class ServerWorker:
    client_info={}

    def __init__(self, clientInfo):
        self.client_info = clientInfo

    def run(self):
        threading.Thread(target=self.recvRTSPreq).start()

    def recvRTSPreq(self):
        sock = self.client_info['rtsp'][0]
        while True:
            data = sock.recv(4096)
            data.decode()
            if data is "start":
                reply = "starting"
                sock.sendall(reply.encode())
                processRTSPreq(sock)

    def processRTSPreq(self, sock):
        # Create a new thread and start sending RTP packets
        self.clientInfo['event'] = threading.Event()
        self.clientInfo['worker']= threading.Thread(target=self.sendRtp)
        self.clientInfo['worker'].start()
