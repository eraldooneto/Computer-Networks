import socket
import threading
import time 

# Take the IP Address 
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADRESS = (SERVER_IP, PORT)

# Create a server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADRESS)

connections = []
messages = []

# Send a message just for one person 
def sendPersonalMessage(connection):
    print(f"Sending messages to {connection['address']}")

    for i in range(connection['last'], len(messages)):
        messageToSend = "msg=" + messages[i]
        connection['connection'].send(messageToSend.encode())
        connection['last'] = i + 1
        time.sleep(0.2)

# Send a message for everyone
def sendGroupMessage():
    global connections

    for connection in connections:
        sendPersonalMessage(connection)

def holdClients(connection, address):
    global connections
    global messages
    name = False

    print(f"A new user has been connected via address {address}.")

    # Get the client's message 
    while(True):
        msg = connection.recv(2048).decode("utf-8")

        # Check if it's really a message and separates the message in name and message 
        if(msg): 
            if(msg.startwith("name=")):
                separatedMessage = msg.split("=")
                name = separatedMessage[1]
                
                connectionMap = {
                                "connection": connection, 
                                "address": address,
                                "name": name,
                                "last": 0
                }

                connections.append(connectionMap)
                sendPersonalMessage(connectionMap)
        
        elif(msg.startwith("msg=")):
            separatedMessage = msg.split("=")
    
            # Check this variable later
            message = name + "=" + separatedMessage[1]
            messages.append(message)
            sendGroupMessage()


# Socket is listening the client - It means that a socket accepts a message from client 
def begin():
    print("[Beginning] Initializing Socket")
    server.listen()

    while(True): 

        # A new person get in conversation so a process is created via thread
        connection, address = server.accept()
        thread = threading.Thread(target=holdClients, args=(connection, address))
        thread.start()

begin()
