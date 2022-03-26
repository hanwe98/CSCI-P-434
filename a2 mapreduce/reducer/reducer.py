from ast import Str
from socket import *
from collections import defaultdict
import sys
import re  
import json
from threading import Thread

try:
    serverPort = int(sys.argv[1]) # 8021
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print(f"The server {serverPort} is ready to receive")
except:
    print("Error on port number")

# to_be_reduced ： [ArrayOf ReducerEntry]
to_be_reduced = [] 
def save_to_list(connectionSocket, addr):
    recv = connectionSocket.recv(1024)
    result = recv
    while recv:
        recv = connectionSocket.recv(1024)
        results += recv
    print(json.loads(results).items())
    to_be_reduced.append(json.loads(results))
    connectionSocket.close()

# receive # of mappers
for i in range(2):
    connectionSocket, addr = serverSocket.accept()     # Establish connection with mapper.
    Thread.start_new_thread(save_to_list, (connectionSocket,addr))
# at this point, list contains all works that needs to be done 
t.join()
serverSocket.close()


# receive files from mappers

# operate on files

# send back to master


for i in range(num_mapper):
    connectionSocket[i], addr[i] = mapper_communication_sockets[i].accept()
# connection established with mapper
    
    line = connectionSocket.recv(1024).decode('utf-8', 'ignore')
# when to stop?



# receive ReducerEntry from Mappers

open_mappers_communication()

