from socket import *
import argparse
from heapq import *
from methods import *
from threading import *
import threading
import time

numberOfPorts = 3
clientPorts = [9889 + n for n in range(numberOfPorts)]   # [ListOf Integer]
serverPorts = [10050 + n for n in range(numberOfPorts)]  # [ListOf Integer]
mode = None                                              # 'eventual' or 'sequential'
                                                         # A TimeStamp is a [serverID, time] : [Integer, Integer]
timeStamps = [None for n in range(numberOfPorts)]        # [ListOf TimeStamp] 
pqueues = [None for n in range(numberOfPorts)]           # [ListOf [PQ encode(TimeStamp)]]  
ackDicts = [None for n in range(numberOfPorts)]          # [ListOf [DictionaryOf String Number]] 
mutexes = [Semaphore(0) for n in range(numberOfPorts)]   # [ListOf Semaphore]
curWrites = [None for n in range(numberOfPorts)]         # [Listof String]

# broadcast : broadcast the given message to all serverports
def broadcast(msg):
    serverName = 'localhost'
    for serverPort in serverPorts:
        socketToOtherReplica = socket(AF_INET, SOCK_STREAM)
        socketToOtherReplica.connect((serverName,serverPort))
        socketToOtherReplica.send(str.encode(msg))
        socketToOtherReplica.close()

# portSetup : return a socket that bind and listen to the given port number
def portSetup(port):
    try:
        currentSocket = socket(AF_INET,SOCK_STREAM)
        currentSocket.bind(('',port))
        currentSocket.listen()
        print(f"{port}The server is ready to receive")
        return currentSocket
    except:
        print("Error on port number")

# receive_servermsg : start to receive and interpret the messages transferred between servers
def receive_servermsg(serverSocket, index):
    global timeStamps, pqueues, ackDicts, curWrites
    # initialize variables
    timeStamp = timeStamps[index]
    pqueue = pqueues[index]
    ackDict = ackDicts[index]

    location = str(index)

    while 1:
        connectionSocket, addr = serverSocket.accept()
        text = connectionSocket.recv(1024).decode()
        connectionSocket.close()
        
         # parse input
        msg = eval(text)
        cmd, key, val, byte, ts, type = msg
        # handle broadcast
        updateTimeStamp(timeStamp, eval(ts)) # updating own timestamp according to timestamp on msg

        # never pop when receive a message because you haven't got your own acknowledgement
        if type == 'message': 
            # add to priority queue
            encodedTS = encodeTimeStamp(eval(ts))
            heappush(pqueue, encodedTS)

            # send acknowledgement
            incrementTimeStamp(timeStamp) # send broadcast
            broadcastMsg = [ts, key, val, byte, str(timeStamp), "acknowledgement"]
            broadcast(str(broadcastMsg))
            
        if type == 'acknowledgement':
            # add to acknowlegement dictionary and check if any can be poped
            ts = cmd
            count = None
            if ts not in ackDict:
                count = 1
            else:
                count = ackDict.get(ts) + 1
            ackDict.update({ts : count})
            
            # pop only if the msg in the first in the priority queue and has collected all acknowledgements
            firstTS = pqueue[0]
            if encodeTimeStamp(eval(ts)) == firstTS and ackDict.get(ts) == numberOfPorts:
                ackDict.pop(ts)
                heappop(pqueue)
                time.sleep(5)
                modify(location, key, val, byte)
                if mode == 'sequential' and curWrites[index] == ts:
                    mutexes[index].release()

# receive_clientmsg : start to receive and interpret the messages sent from clients     
def receive_clientmsg(clientSocket, index):
    global timeStamps, pqueues, ackDicts, curWrites
    # initialize variables
    timeStamp = timeStamps[index]
    clientPort = clientPorts[index]

    location = str(index)
    # start receiving msg from clients
    while 1:
        connectionSocket, addr = clientSocket.accept()
        text = connectionSocket.recv(1024).decode()
        
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
            if s is None:
                reply = "the value of " + key + " is not found in the storage system"
            else:
                reply = "VALUE " + key + " " + s[1] + "\n" + s[0] + "\nEnd"

        # perform set
        if cmd == "set":
            val, byte = msg[2:]

            # A broadcastMsg is a ["broadcast", key, val, byte, timeStamp : String]
            incrementTimeStamp(timeStamp) # call broadcast
            curWrites[index] = str(timeStamp)
            broadcastMsg = ["broadcast", key, val, byte, str(timeStamp), 'message']
            if mode == 'eventual':
                broadcast(str(broadcastMsg))
            if mode == 'sequential':
                # blocking broadcast
                broadcast(str(broadcastMsg))
                mutexes[index].acquire()
            reply = "STORED"
        connectionSocket.send(str.encode(reply))
        connectionSocket.close()

# open_server: setting up the key variables such as timestamp, pqueue, and ackDict;
#              open one thread for handling clients, another thread for handling servers
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