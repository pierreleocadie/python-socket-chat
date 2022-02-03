#!usr/bin/python3
import socket, pickle

class ClientNetwork:
    
    def __init__(self, HOST, PORT, HEADER=8192):
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER = HEADER
        self.FORMAT = "utf-8"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.connect()
        print(self.status)
    
    def connect(self):
        try:
            self.client.connect(self.ADDR)
            return self.client.recv(self.HEADER).decode()
        except socket.error as e:
            return "ERROR WHILE TRY TO CONNECT TO THE SERVER", e
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #pickle.dumps()
            #return self.client.recv(self.HEADER).decode()
        except socket.error as e:
            return "ERROR WHILE TRYING TO SEND DATA", e
    
    def receive(self):
        try:
            return self.client.recv(self.HEADER).decode()
            #return pickle.loads(self.client.recv(self.HEADER))
        except socket.error as e:
            return "ERROR WHILE TRYING TO RECEIVE DATA", e