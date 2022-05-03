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
    serverName = sys.argv[1] # "localhost" or '127.0.0.1'
    serverPort = int(sys.argv[2]) # 9889

except: 
    serverName = "localhost"
    serverPort = 9889


sendmsg(msg1)
sendmsg(msg2)



clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print(f"You are connected to port {serverPort} of the {serverName}")

    # sentence = input("Please enter a memcached-like command (type exit to quit): \n")
    # msg = []
    # if sentence == 'exit':
    #     msg.append('exit')
    #     clientSocket.send(str.encode(str(msg)))
    #     break
    # # parse the input from user
    # cmd, keyByte = findUntilNextSpace(sentence)
    # key, byte = findUntilNextSpace(keyByte)

    # msg.append(cmd)
    # if cmd == "set":
    #     value = input()
    #     msg.append(key)
    #     msg.append(value)
    #     msg.append(byte)
    # elif cmd == "get":
    #     msg.append(key)
    # else:
    #     print(f"{cmd} : This method is not supported yet!")
    #     continue
    # print(str(msg))

    # testing case: seting x to be 3
msg = ['set', 'x', '42', '1']
# msg = ['get', 'wa']
clientSocket.send(str.encode(str(msg)))

modifiedSentence = clientSocket.recv(1024)
print(modifiedSentence.decode())

clientSocket.close()

