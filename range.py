class Range:
    def __init__(self, fromIndex, toIndex, edges):
        self.__setFromIndex__(fromIndex)
        self.__setToIndex__(toIndex)
        self.__setEdges__(edges[0], edges[1])
    def __setFromIndex__(self, index):
        self.fromIndex = index
    def getFromIndex(self):
        return self.fromIndex
    def __setToIndex__(self, index):
        self.toIndex = index
    def getToIndex(self):
        return self.toIndex
    def __setEdges__(self, left, right):
        self.leftEdge = left
        self.rightEdge = right
    def getEdges(self):
        return (self.leftEdge, self.rightEdge)