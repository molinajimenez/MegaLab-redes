class Node:
    def __init__(self, name, neighbors, message):
        self.name = name
        self.neighbors = neighbors
        self.message = message

    def getNeighbors(self):
        return self.neighbors

    def getMessage(self):
        return self.message

    def getName(self):
        return self.name

    def setMessage(self, message):
        self.message = message

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors

    #no he probado esto lol.
    def objectNode(self):
        dic = {}
        dic[self.name] = {self.neighbors[i] for i in range(0, len(self.neighbors))}
        return dic
