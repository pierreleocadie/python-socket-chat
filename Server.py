import socket, pickle, threading

class ServerNetwork:

    def __init__(self, PORT, HEADER=8192):
        #-SERVER SETTINGS
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.HEADER = HEADER
        self.FORMAT = "utf-8"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = self.bind()
        self.allClients = []

        #-SET ACCOUNTS
        self.accounts = []
    
    #-SERVER
    def bind(self):
        try:
            self.server.bind(self.ADDR)
            print("SERVER CONFIGURATED")
        except:
            print("ERROR WHILE TRY TO CONFIGURATE THE SERVER")
    
    def commandDecoder(self, command:str):
        splitCommand = command.split()
        recipientsIDsList = []
        if "[[TO]]" in splitCommand:
            messageReply = " ".join(splitCommand[:splitCommand.index("[[TO]]")])
            recipientsIDsList = []
            splitCommand = splitCommand[splitCommand.index("[[TO]]")+1:]
            for ids in splitCommand:
                recipientsIDsList.append(int(ids))
            return messageReply, recipientsIDsList
        else:
            return command, recipientsIDsList
    
    def createRecipientsSelection(self, selfConn, recipientsIDsList:list):
        recipientsSelection = []
        if len(recipientsIDsList) != 0:
            recipientsSelection = [selfConn]
            for account in self.accounts:
                if account["ID"] in recipientsIDsList:
                    recipientsSelection.append(account["CONN"])
        return recipientsSelection
    
    def sendDataTo(self, reply, toSendReply, toRecipients:list):
        if len(toRecipients) != 0:
            for client in toRecipients:
                client.sendall(str.encode(toSendReply))
                print(f"Sending : {reply} to : {client}")
        else:
            for client in self.allClients:
                client[0].sendall(str.encode(toSendReply))
                print(f"Sending : {reply} to : {client[0]}")
    
    def manageClient(self, conn, addr):
        newJoinerDefaultData = {"ID": len(self.accounts), "CONN": conn, "AMOUNT": 100}
        conn.send(str.encode(f"CONNECTED TO THE SERVER\nYOUR CURRENT ID IS : {len(self.accounts)}"))
        connected = True
        self.allClients.append((conn, addr))
        self.accounts.append(newJoinerDefaultData)
        
        print(f"{ addr } CONNECTED")
        print(f"Number of clients connected : { len(self.allClients) }")
        print(f"New account added { self.accounts[len(self.accounts)-1]}")
        while connected:
            try:
                data = conn.recv(self.HEADER)
                reply = data.decode(self.FORMAT)
                if not data:
                    self.allClients.remove(self.allClients[self.allClients.index((conn, addr))])
                    print(f"Number of clients connected : { len(self.allClients) }")
                    print("DISCONNECTED")
                    break
                else:
                    print(f"Received : {reply} from : {conn}")
                    if len(self.commandDecoder(reply)[1]) != 0:
                        messageToSend = f"{addr} : {self.commandDecoder(reply)[0]}"
                        recipientsList = self.createRecipientsSelection(conn, self.commandDecoder(reply)[1])
                        self.sendDataTo(messageToSend, messageToSend, recipientsList)
                        
                        print(f"Message : { self.commandDecoder(reply)[0] }\nFrom : {addr}\nTo : {recipientsList}\n")
                    else: 
                        toSendReply = f"{addr} : {reply}\n"
                        self.sendDataTo(reply, toSendReply, [])
            except:
                self.allClients.remove(self.allClients[self.allClients.index((conn, addr))])
                
                #-MESSAGES DISPLAY
                print("LOST CONNECTION")
                print("ERROR WHILE TRY TO MANAGED THE CLIENT")
                print(f"Number of clients connected : { len(self.allClients) }")
                break
        conn.close()
    
    def serverManage(self):
        self.server.listen(2)
        while True:
            conn, addr = self.server.accept()
            print(f"{ addr } TRY TO CONNECT")
            thread = threading.Thread(target=self.manageClient, args=(conn, addr))
            thread.start()
            
    def start(self):
        print("RUNNING THE SERVER")
        print("[INFO] HOST : "+self.HOST+" PORT : "+str(self.PORT))
        
        running = True
        while running:
            self.serverManage()


server = ServerNetwork(6000)
server.start()
