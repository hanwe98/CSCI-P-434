import os

def findUntilNextSpace(t):
    i = 0
    for i in range(0,len(t)):
        if t[i] == " ":
            return (t[0:i], t[i+1:])
    return (t,'')

# find the value associated to the given key in the storage file system.
def find(location, key): 
    filename = "./server/" + location + "/storage.txt"

    # -----------------------
    # If the directory doesn't exist, should we make a brand new one or copy from existed?
    
    # path = "./" + location
    # # create repo if not exist
    # if not os.path.exists(path):
    #     os.makedirs(path)
    
    # # create file if not exist
    # create = open(filename, "a+")
    # create.close()

    f = open(filename, "r")
    for line in f:
        line = line.strip() # remove \n
        key1, vb = findUntilNextSpace(line)
        if key == key1:
            f.close()
            return findUntilNextSpace(vb)
    f.close()
    return None

# if the key is in the file of storage, update the associated value to the given value
def modify(location, key, value, byte):
    filename = "./server/" + location + "/storage.txt"

    # create file if not exist
    create = open(filename, "a+")
    create.close()

    s = key + " " + value + " " + byte
    find = False
    with open(filename, "r") as fp:
        lines = fp.readlines()

    with open(filename, "w") as fp:
        for line in lines:
            if not line.isspace():
                if findUntilNextSpace(line.strip())[0] == key:
                    fp.write(s + "\n")
                    find = True
                else:
                    fp.write(line)
        if not find:
            fp.write("\n" + s)

# increment own timestamp by 1, denoting an event has taken place
def incrementTimeStamp(ts):
    ts[1] += 1

# update own timestamp according to the sender's timestamp when receiving a msg
def updateTimeStamp(selfTs, senderTs):
    if senderTs[1] > selfTs[1]:
        selfTs[1] = senderTs[1]
    incrementTimeStamp(selfTs)

def encodeTimeStamp(timeStamp):
    return timeStamp[1] * 100 + timeStamp[0]