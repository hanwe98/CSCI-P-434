from socket import *
import argparse
from heapq import *
from methods import *
import threading

numberOfPorts = 3
clientPorts = [9889 + n for n in range(numberOfPorts)]
serverPorts = [10000 + n for n in range(numberOfPorts)]
mode = None
timeStamps = [None for n in range(numberOfPorts)]
pqueues = [None for n in range(numberOfPorts)]
ackDicts = [None for n in range(numberOfPorts)]

def broadcast(msg):
    serverName = 'localhost'
    for serverPort in serverPorts:
        socketToOtherReplica = socket(AF_INET, SOCK_STREAM)
        socketToOtherReplica.connect((serverName,serverPort))
        print(f"sending {msg} to {serverPort}")
        socketToOtherReplica.send(str.encode(msg))
        socketToOtherReplica.close()

def portSetup(port):
    try:
        currentSocket = socket(AF_INET,SOCK_STREAM)
        currentSocket.bind(('',port))
        currentSocket.listen()
        print("The server is ready to receive")
        return currentSocket
    except:
        print("Error on port number")

def receive_servermsg(serverSocket, index):
    global timeStamps, pqueues, ackDicts
    # initialize variables
    timeStamp = timeStamps[index]
    pqueue = pqueues[index]
    ackDict = ackDicts[index]
    serverPort = serverPorts[index]
    location = str(index)
    print(f'{serverPort} started')

    while 1:
        connectionSocket, addr = serverSocket.accept()

        text = connectionSocket.recv(1024).decode()
        connectionSocket.close()

        # parse input
        print(f"{serverPort} receives: {text}")
        
        msg = eval(text)
        cmd, key, val, byte, ts, type = msg

        # handle broadcast
        updateTimeStamp(timeStamp, eval(ts)) # updating own timestamp according to timestamp on msg

        # never pop when receive a message because you haven't got your own acknowledgement
        if type == 'message': 
            # add to priority queue
            keyOfHeap = timeStamp[1] * 100 + timeStamp[0]
            heappush(pqueue, (keyOfHeap, key))

            # send acknowledgement
            incrementTimeStamp(timeStamp) # send broadcast
            broadcastMsg = ["broadcast", key, val, byte, str(timeStamp), "acknowledgement"]
            broadcast(str(broadcastMsg))
            
        if type == 'acknowledgement':
            # add to acknowlegement dictionary and check if any can be poped
            count = None
            if key not in ackDict:
                count = 1
            else:
                count = ackDict.get(key) + 1
            ackDict.update({key : count})
            
            print(f'{serverPort} current pqueue: {pqueue}')
            print(f'{serverPort} current ackDict: {ackDict}')
            
            # pop only if the msg in the first in the priority queue and has collected all acknowledgements
            firstKey = pqueue[0][1]
            print(f'{serverPort} current firstKey: {firstKey}')
            print(f'{serverPort} current numberOfPorts: {numberOfPorts}')
            if ackDict.get(firstKey) == numberOfPorts:
                print('should pop now')
                ackDict.pop(firstKey)
                heappop(pqueue)
                modify(location, key, val, byte)
                print(f'{serverPort} modified')
        

def receive_clientmsg(clientSocket, index):
    global timeStamps, pqueues, ackDicts
    # initialize variables
    timeStamp = timeStamps[index]
    clientPort = clientPorts[index]
    location = str(index)
    print(f'{clientPort} started')
    # start receiving msg from clients
    while 1:
        connectionSocket, addr = clientSocket.accept()

        text = connectionSocket.recv(1024).decode()
        print(f"{clientPort}:  receive {text}")
        
        incrementTimeStamp(timeStamp) # receive msg
        msg = eval(text)
        cmd = msg[0]

        # perform exit
        if cmd == 'exit':
            break
        
        key = msg[1]
        reply = "The given method is not supported yet!"

        # perform get
        if cmd == "get":
            s = find(location, key)
            incrementTimeStamp(timeStamp) # call find
            print(f'timestamp after retrieving data from storage : {timeStamps}')
            if s is None:
                reply = "the value of " + key + " is not found in the storage system"
            else:
                reply = "VALUE " + key + " " + s[1] + "\n" + s[0] + "\nEnd"

        # perform set
        if cmd == "set":
            val, byte = msg[2:]

            # A broadcastMsg is a ["broadcast", key, val, byte, timeStamp : String]
            incrementTimeStamp(timeStamp) # call broadcast
            broadcastMsg = ["broadcast", key, val, byte, str(timeStamp), 'message']
            if mode == 'eventual':
                print(f"{clientPort} start broadcasting")
                broadcast(str(broadcastMsg))
                print(f"{clientPort} exit from broadcast")
            if mode == 'sequential':
                # blocking broadcast
                broadcast(broadcastMsg)
                done = False
                while not done:
                    ...
            reply = "STORED"
        connectionSocket.send(str.encode(reply))
        connectionSocket.close()

def open_server(index):
    global timeStamps, pqueues, ackDicts
    clientPort = clientPorts[index]
    serverPort = serverPorts[index]

    clientSocket = portSetup(clientPort)
    serverSocket = portSetup(serverPort)

    # initialize timeStamp and priority queue for total order broadcast
    timeStamps[index] = [index, 0]
    pqueues[index] = []
    ackDicts[index] = {}

    toClient = threading.Thread(target=receive_clientmsg, args=(clientSocket, index))
    toServer = threading.Thread(target=receive_servermsg, args=(serverSocket, index))
    toClient.start()
    toServer.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--consistency', type=str, required=True)
    args = parser.parse_args()
    if args.consistency in ['eventual', 'sequential']:
        mode = args.consistency
    else:
        raise Exception(f'{args.consistency} : Not a valid mode. Please choose from either eventual or sequential.')

    threads = [None] * numberOfPorts
    for i in range(numberOfPorts):
        threads[i] = threading.Thread(target = open_server, args=(i,))
        threads[i].start()
    for i in range(numberOfPorts):
        threads[i].join()