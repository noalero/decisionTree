import feature
import numericalFeature
import categoricalFeature
import breed
import leaf
import parent
class Node(object):
    # children
    # numOfChildren
    def __init__(self, feature, dataPath):
        pass
    def __setFeature__(self, feature):
        self.feature = feature
    def getFeature(self):
        return self.feature
    def __setDataPath__(self, dataPath):
        self.dataPath = dataPath
    def getDataPath(self):
        return self.dataPath
    def __setNumOfChildren__(self, numOfChildren):
        self.numOfChildren = numOfChildren
    def getNumOfChildren(self):
        return self.numOfChildren
    def __setChildren__(self):
        pass
    def getChildren(self):
        pass
        # return self.children
    def __setChild__(self, child):
        pass
    def getChild(self, breed):
        pass
    def addChild(self, breed, dataPath, arg):
        pass
        # create parent / lead, visitor pattern
