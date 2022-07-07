import socket
import threading
import time 

PORT = 5050
SERVER = "192.168.0.109"
ADRESS = (SERVER, PORT)

# Client connection to server address
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADRESS)

def holdMessages():
    while(True):
        msg = client.recv(2048).decode()
        separatedMessage = msg.split("=")
        print(separatedMessage[1] + ": " + separatedMessage[2])

def send(message):
    client.send(message.encode("utf-8"))

def sendMessage():
    message = input()
    send("msg=" + message)

def sendAuthor():
    name = input("Please, type your name: ")
    send("name=" + name)

def beginSending():
    sendAuthor()
    sendMessage()

def begin():
    firstThread = threading.Thread(target=holdMessages)
    secondThread = threading.Thread(target=beginSending)
    
    firstThread.start()
    secondThread.start()

begin()
