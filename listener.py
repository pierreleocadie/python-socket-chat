import threading, Client

CLIENT = Client.ClientNetwork("192.168.1.18", 6000)

while True:
    serverData = CLIENT.receive()
    print(serverData)
