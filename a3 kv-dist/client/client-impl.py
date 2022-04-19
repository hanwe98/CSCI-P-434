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
    msg = []
    if sentence == 'exit':
        msg.append('exit')
        clientSocket.send(str.encode(str(msg)))
        break
    # parse the input from user
    cmd, keyByte = findUntilNextSpace(sentence)
    key, byte = findUntilNextSpace(keyByte)

    msg.append(cmd)
    if cmd == "set":
        value = input()
        msg.append(key)
        msg.append(value)
        msg.append(byte)
    elif cmd == "get":
        msg.append(key)
    else:
        print(f"{cmd} : This method is not supported yet!")
        continue
    print(str(msg))
    clientSocket.send(str.encode(str(msg)))

    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())

clientSocket.close()