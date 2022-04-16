from ast import Str
from socket import *
import sys
from methods import *
from multiprocessing import Pool
import argparse

numberOfPorts = 2
serverPorts = [9889 + n for n in range(numberOfPorts)]
mode = None

def broadcast(msg):
    return None

def open_server(port):
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

                reply = "STORED"
                broadcastMsg = "broadcast" + " " + key + " " + val + " " + byte
                if mode == 'eventual':
                    # broadcast text in the background by multiprocessing?
                    # non blocking broadcast
                    ...
                if mode == 'sequential':
                    # blocking broadcast
                    ...

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
        pool.map(open_server, serverPorts)
    