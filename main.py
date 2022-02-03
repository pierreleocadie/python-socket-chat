import threading, Client

CLIENT = Client.ClientNetwork("192.168.1.14", 6000)

def receiveDataNetwork():
    while True:
        serverData = CLIENT.receive()
        print(serverData)

def askUser():
    while True:
        userDataToSend = input("What would you send to people ? \n")
        if userDataToSend != "STOP" and len(userDataToSend) != 0:
            CLIENT.send(userDataToSend)
        elif userDataToSend == "STOP":
            break

th_askUser = threading.Thread(target=askUser)
th_receiveDataNetwork = threading.Thread(target=receiveDataNetwork)
    
th_askUser.start()
th_receiveDataNetwork.start()