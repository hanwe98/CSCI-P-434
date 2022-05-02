from socket import *
import sys

def sendmsg(msg):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print(f"You are connected to port {serverPort} of the {serverName}")

    clientSocket.send(str.encode(str(msg)))
    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())
    clientSocket.close()
try:
    key = sys.argv[1]
    val = sys.argv[2]
except: 
    key = 'x'
    val = '42'
serverName = "localhost"
serverPort = 9889

msg1 = ['set', key, val, '1']
msg2 = ['get', key]
sendmsg(msg1)
sendmsg(msg2)