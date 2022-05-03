from socket import *
import time

def sendmsg(msg):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    print(f"You are connected to port {serverPort} of the {serverName}")

    clientSocket.send(str.encode(str(msg)))
    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())
    clientSocket.close()

serverName = "localhost"
serverPort = 9889

startTime = time.time()
for i in range(100):
    msg1 = ['set', 'x', str(i), '1']
    msg2 = ['get', 'x']
    sendmsg(msg1)
    sendmsg(msg2)
endTime = time.time()

print(f'time elapsed: {endTime - startTime}')