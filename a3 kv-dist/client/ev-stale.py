from socket import *
import sys
import time

def findUntilNextSpace(t):
    i = 0
    for i in range(0,len(t)):
        if t[i] == " ":
            return (t[0:i], t[i+1:])
    return (t,'')

def sendmsg(msg):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print(f"You are connected to port {serverPort} of the {serverName}")

    clientSocket.send(str.encode(str(msg)))
    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())
    clientSocket.close()
try:
    serverName = sys.argv[1] # "localhost" or '127.0.0.1'
    serverPort = int(sys.argv[2]) # 9889
except: 
    serverName = "localhost"
    serverPort = 9889

msg1 = ['set', 'x', '42', '1']
msg2 = ['get', 'x']
sendmsg(msg1)
time.sleep(2)
sendmsg(msg2)