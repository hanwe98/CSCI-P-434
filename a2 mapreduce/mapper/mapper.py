from ast import Str
from socket import *
from collections import defaultdict
import sys
import re  
import json

try:
    serverPort = int(sys.argv[1]) # 9889
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print(f"The server {serverPort} is ready to receive")
except:
    print("Error on port number")

def emit(word):
    return (word, 1)
    
# line_to_words: String -> [ListOf String]
# takes a line and return a list that contains all the word in the given line without any punctuation. 
def line_to_words(line):
    string_no_punctuation = re.sub("[^\w\s]", "", line)
    return string_no_punctuation.split()

# A ReducerEntry is a [ListOf [PairOf String Count]]
# An ID is an Integer bewteen 0 (inclusive) and num_reducer (exclusive)
# mapper : [ListOf String] -> [PairOf ID ReducerEntry]
# takes a list of lines and return the outcome of a wordcount mapper
def mapper(listOfLines):
    listOfWords = []
    for line in listOfLines:
        listOfWords.extend(line_to_words(line))

    map_result = map(emit,listOfWords)
    combiner_result = combiner(map_result)
    distributor_result = distributor(combiner_result)
    return distributor_result

# combiner : [ListOf [PairOf String One]] -> [ListOf [PairOf String Frequency]]
# takes the result of mapper and reorganize it with a dictionary
def combiner(map_result):
    combiner = defaultdict(list)
    for k,v in (map_result):
        combiner[k].append(v)
    for key in combiner:
        combiner[key] = len(combiner[key])
    # return combiner.items()
    return combiner

num_reducer = 2
# [ListOf [PairOf String Frequency]] -> [ListOf [PairOf String Frequency]]
def distributor(combiner_result):

    # initialize distributor
    distributor = defaultdict(list)
    # fill in sorted_results
    for k,v in combiner_result.items():
        index = (ord(k[0].upper()) - 65) % num_reducer
        distributor[index].append((k,v))
    return distributor

reducer_sockets = []
reducer_ports = [8021, 8022]
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

listOfLines = []
while 1:
    # receive document from master
    connectionSocket, addr = serverSocket.accept()
    line = connectionSocket.recv(1024).decode('utf-8', 'ignore')
    while line:
        if line == 'exit':
            break
        listOfLines.append(line)
        line = connectionSocket.recv(1024).decode('utf-8', 'ignore')
    # document fully received from the master and saved into listOfLines at this point
    
    map_result = mapper(listOfLines) # [PairOf ID ReducerEntry]
    # results are fully computed and saved in map_result at this point

    # send map_results to reducers
    # open_reducers()
    
    # i = 0
    # for k,v in map_results:
    #     serialized_dict = json.dumps(v)
    #     reducer_sockets[i].send(str.encode(serialized_dict))
    #     i += 1
    # at this point, all data has been distributed to all reducers

    # close all sockets
    print("socket closed")
    connectionSocket.close()
    # for socket in reducer_sockets:
    #     socket.close()
    break