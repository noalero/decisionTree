import feature
class NumericalFeature(feature.Feature):
    def __init__(self, name, values):
        feature.Feature.__init__(name, values)
        self.__setBreeds__(values)
    def __setBreeds__(self, values): # visitor pattern
        pass
    def isValueOfBreed(self, range, value): # visitor pattern
        ans = True
        if(value < range.getFromIndex() | value > range.getToIndex()):
            ans = False
        if(not(range.getEdges()[0]) & value == range.getFromIndex()):
            ans = False
        if(not(range.getEdges()[1]) & value == range.getToIndex()):
            ans = False
        return ans
