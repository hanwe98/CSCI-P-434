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

def reducer(ls):
    reducer = {}
    for k,v in ls:
        prev = reducer.get(k)
        if prev is None:
            reducer.update({k: v})
        else:
            reducer.update({k: v + prev})
    return reducer


connectionSocket, addr = serverSocket.accept()
recv = connectionSocket.recv(1024)
mapper_result = recv
print(0)
while recv:
    if recv.decode()[-6:-2] == "exit":
        break
    recv = connectionSocket.recv(1024)
    mapper_result += recv
print(1)
ls = json.loads(mapper_result)
reduce_result = reducer(ls)
serialized_dict = json.dumps(reduce_result)

print("socket closed")
connectionSocket.send(str.encode(serialized_dict))
connectionSocket.close()