from ast import Str
from socket import *
import sys
from methods import *
from multiprocessing import Pool


numberOfPorts = 2
serverPorts = [9889 + n for n in range(numberOfPorts)]

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
                    # (test use) reply = "the value of " + key + " is " + s
                    reply = "VALUE " + key + " " + s[1] + "\n" + s[0] + "\nEnd"
            if cmd == "set":
                # perform set
                val, byte = findUntilNextSpace(bv)
                s = modify(location, key, val, byte)

                # (test use) reply = "the value of " + key + " has been set to " + val 
                reply = "STORED"
                # broadcast in the background multiprocessing?

            connectionSocket.send(str.encode(reply))
        connectionSocket.close()

if __name__ == '__main__':
    with Pool(processes=numberOfPorts) as pool:
        pool.map(open_server, serverPorts)
    