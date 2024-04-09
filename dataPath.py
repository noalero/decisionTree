import feature
import numericalFeature
import categoricalFeature
import breed
import leaf
import parent
class DataPath(object):
    def __init__(self):
        pass
    def __setSize__(self, size):
        self.size = size
    def getSize(self):
        return self.size
    def __setPath__(self, path):
        self.path = path
        pass
    def getPath(self):
        return self.path
    def addFeature(self, feature):
        pass
        # resize
    def addBreed(self, breed):
        pass
        # resize