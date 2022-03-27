from xmlrpc.server import SimpleXMLRPCServer
import re
import threading
from socket import *
import json


num_mapper = 10
num_reducer = 10
port_outset = 8001
max_mapper = 20
max_reducer = 20
reducer_outset = port_outset + max_mapper
mapper_ports = [port_outset + n for n in range(max_mapper)]
reducer_ports = [port_outset + max_mapper + n for n in range(max_reducer)]

mapper_sockets = []
reducer_sockets = []


# init_cluster: Takes two numbers m and r, and open m number of mappers and n number of reducers
def init_cluster(m, r):
    global num_mapper
    global num_reducer
    num_mapper = m
    num_reducer = r

    if open_mappers() and open_reducers():
        return True
    return False

def open_mappers():
    serverName = "localhost"
    
    for i in range(num_mapper):
        mapper_sockets.append(socket(AF_INET, SOCK_STREAM))
        
    try:
        for i in range(num_mapper):
            mapper_sockets[i].connect((serverName, mapper_ports[i]))
        print("mapper opened")
        return True
    except Exception as e:
        print(f"mapper failed to open : {e}")
        return False
    print(f"mapper failed to open and escape except")

def open_reducers():
    serverName = "localhost"
    
    for i in range(num_reducer):
        reducer_sockets.append(socket(AF_INET, SOCK_STREAM))
        
    try:
        for i in range(num_reducer):
            reducer_sockets[i].connect((serverName, reducer_ports[i]))
        print("reducer opened")
        return True
    except Exception as e:
        print(f"reducer failed to open : {e}")
        return False
    print(f"reducer failed to open and escape except")

def server_receive_file(arg):
    with open("saved_book.txt", "wb") as handle:
        handle.write(arg.data)
    
    with open("saved_book.txt", "rb") as f:
        lines = []
        for i in range(num_mapper):
            lines.append([])
        
        i = 0
        for line in f:
            i = i % num_mapper
            lines[i].append(line)
            i = i + 1
        # each list in lines now contains the designated job for each mapper process

        # send through socket
        for i in range(num_mapper):
            for line in lines[i]:
                mapper_sockets[i].send(line)
            mapper_sockets[i].send(str.encode('exit'))
        # at this point, data has been successfully sent to mappers!
        
        # initialize map_results
        map_results = []
        for i in range(num_reducer):
            map_results.append([])
        
        # receive from mapper
        for i in range(num_mapper):
            recv = mapper_sockets[i].recv(1024)
            mapper_result = recv
            while recv:
                recv = mapper_sockets[i].recv(1024)
                mapper_result += recv
            temp = json.loads(mapper_result) # [defaultdictOf ID ReducerEntry]
            
            #add to map_results
            for i,re in temp.items():
                c = int(i)
                map_results[c] = map_results[c] + re 
        # at this point, map_results come back from mappers

        # send map_results to reducers
        for i in range(num_reducer):
            temp = map_results[i].append("exit")
            msg = json.dumps(temp)
            reducer_sockets[i].send(str.encode(msg))
        # at this point, data has been successfully sent to reducers!
        
        #--------------------------------
        # # receive from reducers 
        # reduce_results = []
        # for i in range(num_reducer):
        #     reduce_results.append([])
        
        # for i in range(num_reducer):
        #     recv = reducer_sockets[i].recv(1024)
        #     reduce_result = recv
        #     while recv:
        #         recv = reducer_sockets[i].recv(1024)
        #         reduce_result += recv
        #     temp = json.loads(reduce_result) # [defaultdictOf ID ReducerEntry]
        #     print(temp)
        # for i in range(num_reducer):
        #     reducer_sockets[i].close()
        # for i in range(num_mapper):
        #     mapper_sockets[i].close()
    return True

        

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(init_cluster, "init_cluster")
server.register_function(server_receive_file, "server_receive_file")
server.serve_forever()