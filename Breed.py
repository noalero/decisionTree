class Breed(object):
    def __init__(self, name, dataPath):
        self.__setName__(name)
        self.__setDataPath__(dataPath)
    def __setName__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def __setDataPath__(self, dataPath):
        self.dataPath = dataPath
    def getDataPath(self):
        return self.dataPath
