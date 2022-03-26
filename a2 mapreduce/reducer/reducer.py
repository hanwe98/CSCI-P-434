from ast import Str
from socket import *
from collections import defaultdict
import sys
import re  
import json

try:
    serverPort = int(sys.argv[1]) # 8021
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print(f"The server {serverPort} is ready to receive")
except:
    print("Error on port number")

mapper_communication_sockets = []
mapper_communication_ports[]
num_mapper = 2


def open_mappers_communication():
    serverName = "localhost"
    
    for i in range(num_mapper):
        mapper_communication_sockets.append(socket(AF_INET, SOCK_STREAM))
        
    try:
        for i in range(num_mapper):
            mapper_communication_sockets[i].connect((serverName, mapper_ports[i]))
        print("communication with mappers established")
        return True
    except Exception as e:
        print(f"mapper failed to open : {e}")
        return False
    print(f"mapper failed to open and escape except")


while 1:
    # receive instructions from 
    master_socket = socket(AF_INET, SOCK_STREAM)
    connectionSocket, addr = serverSocket.accept()
    line = connectionSocket.recv(1024).decode('utf-8', 'ignore')


    # receive ReducerEntry from Mappers
    
    open_mappers_communication()


    
    while line: