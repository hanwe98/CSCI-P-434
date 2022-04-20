from socket import *
from multiprocessing import Pool
import argparse
from heapq import *
from methods import *

numberOfPorts = 2
serverPorts = [9889 + n for n in range(numberOfPorts)]
communicationPorts = [10000 + n for n in range(numberOfPorts)]
mode = 'eventual'


def broadcast(msg):
    serverName = 'localhost'
    for serverPort in serverPorts:
        socketToOtherReplica = socket(AF_INET, SOCK_STREAM)
        socketToOtherReplica.connect((serverName,serverPort))
        print(f"sending {msg} to {serverPort}")
        socketToOtherReplica.send(str.encode(msg))
        socketToOtherReplica.close()
        
def open_server(index):
    port = serverPorts[index]
    commPort = communicationPorts[index]

    try:
        serverPort = port
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1)
        print("The server is ready to receive")
    except:
        print("Error on port number")
    
    location = str(port)  # file location

    # initialize timeStamp and priority queue for total order broadcast
    timeStamp = [index, 0]
    pqueue = []
    acknowlegements = {}

    # start to receive and process msg from the bound port
    while 1:
        connectionSocket, addr = serverSocket.accept()

        while 1:
            text = connectionSocket.recv(1024).decode()
            print(f"{port} receives: {text}")
            incrementTimeStamp(timeStamp) # receive msg
            msg = eval(text)
            cmd = msg[0]

            if cmd == 'exit':
                break
            
            key = msg[1]
            reply = "The given method is not supported yet!"

            if cmd == "get":
                # perform get
                s = find(location, key)
                incrementTimeStamp(timeStamp) # call find
                if s is None:
                    reply = "the value of " + key + " is not found in the storage system"
                else:
                    reply = "VALUE " + key + " " + s[1] + "\n" + s[0] + "\nEnd"
            if cmd == "set":
                # perform set
                val, byte = msg[2:]
                s = modify(location, key, val, byte)

                # A broadcastMsg is a ["broadcast", key, val, byte, timeStamp : String]
                broadcastMsg = ["broadcast", key, val, byte, str(timeStamp), 'message']
                if mode == 'eventual':
                    # print(f"{port} 1, entered set, eventual mode")
                    # print(f"sending broadcastMsg : {broadcastMsg}")
                    print(f"{port} start broadcasting")
                    broadcast(str(broadcastMsg))
                    print(f"{port} exit from broadcast")
                if mode == 'sequential':
                    # blocking broadcast
                    broadcast(broadcastMsg)
                    done = False
                    while not done:
                        ...
                reply = "STORED"

            if cmd == "broadcast":
                # handle broadcast messages from other replica
                # print("-----------------------")
                # print(f"{port} receives a broadcast")
                # print(f"received broadcastMsg : {text}")
                # print("-------------")
                # print("entered cmd = broadcast")
                val, byte, ts, type = msg[2:]
                # print(type)
                # print(timeStamp)
                # print(ts)
                updateTimeStamp(timeStamp, eval(ts))
                if type == 'message':
                    # print("entered typed == message")
                    # never pop when receive a message because you haven't got your own acknowledgement
                    s = modify(location, key, val, byte)
                    
                    # add to priority queue
                    keyOfHeap = timeStamp[1] * 100 + timeStamp[0]
                    heappush(pqueue, (keyOfHeap, key))

                    # send acknowledgement
                    broadcastMsg = ["broadcast", key, val, byte, str(timeStamp), "acknowledgement"]
                    broadcast(broadcastMsg)
                    
                if type == 'acknowledgement':
                    # print(f"entered typed == ack")
                    # add to acknowlegement dictionary and check if any can be poped
                    count = None
                    if key not in acknowlegements:
                        count = 1
                    else:
                        count = acknowlegements.get(key) + 1
                    acknowlegements.update({key, count})
                    
                    # pop only if the msg in the first in the priority queue and has collected all acknowledgements
                    firstKey = pqueue[0][1]
                    if acknowlegements.get(firstKey) == numberOfPorts:
                        acknowlegements.pop(firstKey)    
                # There is no need to reply to a broadcast, so skip reply and close the socket        
                # print(f"{port} exit receiving broadcast")
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