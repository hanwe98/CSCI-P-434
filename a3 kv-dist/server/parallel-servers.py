from ast import Str
from queue import PriorityQueue
from socket import *
import sys
from methods import *
from multiprocessing import Pool
import argparse

numberOfPorts = 2
serverPorts = [9889 + n for n in range(numberOfPorts)]
mode = None

def incrementTimeStamp(ts, index):
    ts[index] += 1

def broadcast(msg):
    serverName = 'localserver'
    for serverPort in serverPorts:
        socketToOtherReplica = socket(AF_INET, SOCK_STREAM)
        socketToOtherReplica.connect((serverName,serverPort))
        socketToOtherReplica.send(str.encode(msg))
        socketToOtherReplica.close()
        
def open_server(index):
    port = serverPorts[index]
    try:
        serverPort = port
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1)
        print("The server is ready to receive")
    except:
        print("Error on port number")

    # What will happen if multiple clients connect?
    # ----- implement ----- #
    
    location = str(port)  # file location

    # initialize timeStamp and priority queue for total order broadcast
    timeStamp = [0 for n in range(numberOfPorts)]
    pqueue = PriorityQueue()

    # start to receive and process msg from the bound port
    while 1:
        connectionSocket, addr = serverSocket.accept()

        exit = False
        while 1:
            text = connectionSocket.recv(1024).decode()

            if text == 'exit':
                break
            cmd, kbv = findUntilNextSpace(text)
            key, bv = findUntilNextSpace(kbv)
            reply = "The given method is not supported yet!"
            if cmd == "get":
                # perform get
                s = find(location, key)
                if s is None:
                    reply = "the value of " + key + " is not found in the storage system"
                else:
                    reply = "VALUE " + key + " " + s[1] + "\n" + s[0] + "\nEnd"
            if cmd == "set":
                # perform set
                val, byte = findUntilNextSpace(bv)
                s = modify(location, key, val, byte)

                broadcastMsg = "broadcast" + " " + key + " " + val + " " + byte
                if mode == 'eventual':
                    broadcast(broadcastMsg)
                if mode == 'sequential':
                    # blocking broadcast
                    broadcast(broadcastMsg)
                    done = False
                    while not done:
                        ...
                reply = "STORED"

            if cmd == "broadcast":
                # handle broadcast messages from other replica
                val, byte = findUntilNextSpace(bv)
                s = modify(location, key, val, byte)
                break

            connectionSocket.send(str.encode(reply))
        connectionSocket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--consistency', type=str, required=True)
    args = parser.parse_args()
    if args.consistency in ['eventual', 'sequential']:
        mode = args.consistency
    else:
        raise Exception(f'{args.consistency} : Not a valid mode. Please choose from eventual or sequential.')
    with Pool(processes=numberOfPorts) as pool:
        pool.map(open_server, range(numberOfPorts))