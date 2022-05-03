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
msg1 = ['set', 'x', '0', '1']
endTime = time.time()

print(f'time elapsed: {endTime - startTime}')
sendmsg(msg1)