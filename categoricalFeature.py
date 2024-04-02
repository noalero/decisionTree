import feature
class CategoricalFeature(feature.Feature):
    def __init__(self, name, values):
        feature.Feature.__init__(name, values)
        self.__setBreeds__(values)
    def __setBreeds__(self, values): # visitor pattern
        pass
    def isValueOfBreed(self, str, value): # visitor pattern
        return str == value
