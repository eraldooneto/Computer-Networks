import socket
import threading
import time

# Connects a client
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Treats the message to send on the format 'user: message'
def holdMessages():
    while(True):
        msg = client.recv(2048).decode()
        separatedMessage = msg.split("=")
        print(separatedMessage[1] + ": " + separatedMessage[2])

# Client send method 
def send(message):
    client.send(message.encode('utf-8'))

# Takes the message from user and calls for the client method to send 
def sendMessage():
    while(True):
        message = input("> ")
        send("msg=" + message)

# Takes the name from user and sends via 
def sendName():
    name = input("Please, type your name: ")
    send("name=" + name)

def beginSending():
    sendName()
    sendMessage()

def begin():
    
    # Call two process: while a message comes in first process the other process is sending 
    firstThread = threading.Thread(target=holdMessages)
    secondThread = threading.Thread(target=beginSending)
    
    firstThread.start()
    secondThread.start()

begin()
