class Node:
    def __init__(self, name, neighbors, ip, conn):
        self.name = name
        # neighbor structure: dict object ->
        # {
        #   neighbor1_name: weight, 
        #   neighbor2_name: weight, 
        #   ...
        # }
        self.neighbors = neighbors
        self.message = ""
        self.ip = ip
        self.socket = conn

    def getNeighbors(self):
        return self.neighbors
    
    def getNeighborsCost(self, key):
        if key not in self.neighbors.keys():
            return -1
        return self.neighbors[key]

    def getMessage(self):
        return self.message

    def getName(self):
        return self.name

    def setMessage(self, message):
        self.message = message

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    # #no he probado esto lol.
    # def objectNode(self):
    #     dic = {}
    #     dic[self.name] = {self.neighbors[i] for i in range(0, len(self.neighbors))}
    #     return dic
    
    def getState(self):
        state = {
            self.name: self.neighbors
        }
        return state