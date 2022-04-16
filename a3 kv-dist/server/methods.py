def findUntilNextSpace(t):
    i = 0
    for i in range(0,len(t)):
        if t[i] == " ":
            return (t[0:i], t[i+1:])
    return (t,'')

# find the value associated to the given key in the storage file system.
def find(key): 
    f = open("./storage.txt", "r")
    for line in f:
        line = line.strip() # remove \n
        key1, vb = findUntilNextSpace(line)
        if key == key1:
            f.close()
            return findUntilNextSpace(vb)
    f.close()
    return None
    

# if the key is in the file of storage, update the associated value to the given value
def modify(key, value, byte):
    s = key + " " + value + " " + byte
    find = False
    with open("./storage.txt", "r") as fp:
        lines = fp.readlines()

    with open("./storage.txt", "w") as fp:
        for line in lines:
            if not line.isspace():
                if findUntilNextSpace(line.strip())[0] == key:
                    fp.write(s + "\n")
                    find = True
                else:
                    fp.write(line)
        if not find:
            fp.write("\n" + s)