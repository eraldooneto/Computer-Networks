import socket
import threading
import time

# Take the IP Address 
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (SERVER_IP, PORT)

# Create a server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []
messages = []

# Send a message just for one person
def sendPersonalMessage(connection):
    
    print(f"Sending a message to {connection['addr']}")
    
    for i in range(connection['last'], len(messages)):
        messageToSend = "msg=" + messages[i]
        
        connection['conn'].send(messageToSend.encode())
        connection['last'] = i + 1
        
        time.sleep(0.2)

# When a new user connects, recieves all the past messages 
def sendMessageforAll():
    global connections
    
    for connection in connections:
        sendPersonalMessage(connection)

# Get the client's message 
def holdClients(conn, addr):
    global connections
    global messages
    
    print(f"A new user has been connected at address {addr}")
    
    name = False

    # Checks if it's really a message and separates the message in name and message 
    while(True):
        msg = conn.recv(2048).decode("utf-8")
        
        if(msg):
            if(msg.startswith("name=")):
                separatedMessage = msg.split("=")
                name = separatedMessage[1]
                
                connectionMap = {
                    "conn": conn,
                    "addr": addr,
                    "name": name,
                    "last": 0
                }
                
                connections.append(connectionMap)
                sendPersonalMessage(connectionMap)
            

            elif(msg.startswith("msg=")):
                separatedMessage = msg.split("=")
                
                message = name + "=" + separatedMessage[1]
                messages.append(message)
                
                sendMessageforAll()

# Socket is listening the client - It means that a socket accepts a message from client 
def begin():
    print("Socket is running")
    
    server.listen()
    
    # A new person get in conversation so a process is created via thread
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=holdClients, args=(conn, addr))
        thread.start()

begin()
