import feature
class CategoricalFeature(feature.Feature):
    def __init__(self, name, index, values):
        feature.Feature.__init__(name, index, values)
        self.__setBreeds__(values)
    def __setBreeds__(self, values): # visitor pattern
        breeds = []
        pass
    def isValueOfBreed(self, str, value): # visitor pattern
        return str == value
