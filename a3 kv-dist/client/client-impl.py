from socket import *
import sys

def findUntilNextSpace(t):
    i = 0
    for i in range(0,len(t)):
        if t[i] == " ":
            return (t[0:i], t[i+1:])
    return (t,'')

try:
    serverName = sys.argv[1] # "localhost" or '127.0.0.1'
    serverPort = int(sys.argv[2]) # 9889

except: 
    serverName = "localhost"
    serverPort = 9889

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print(f"You are connected to port {serverPort} of the {serverName}")

while 1:
    sentence = input("Please enter a memcached-like command (type exit to quit): \n")
    
    if sentence == 'exit':
        clientSocket.send(str.encode(sentence))
        break
    cmd, keyByte = findUntilNextSpace(sentence)
    key, byte = findUntilNextSpace(keyByte)
    s = cmd
    if cmd == "set":
        value = input()
        s = s + " " + key + " " + value + " " + byte
    elif cmd == "get":
        s = s + " " + key
    
    # print(s)
    clientSocket.send(str.encode(s))

    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())

clientSocket.close()