import numpy as np
class Feature(object):
    def __init__(self, name, values):
        self.__setName__(name)
    def __setName__(self, name):
        self.name = name
    def getName(self):
        return self.name
    def __setBreeds__(self, values): # visitor pattern
        pass
    def getBreeds(self):
        return self.breeds
    def __setInformationGane__(self):
        pass
    def getInformationGaine(self):
        return self.informationGaine
    def isValueOfBreed(self, breed, value): # visitor pattern
        pass
    def __calcInformationGaine__(self, breeds, total):
        entropy = self.__calcEntropy__()
        pass
    def __calcEntropy__(self, total, pos, neg):
        posP = self.__calcP__(total, pos)
        negP = self.__calcP__(total, neg)
        logPosP = np.log(posP)
        logNegP = np.log(negP)
        entropy = (posP * logPosP + negP * logNegP) * (-1.)
        return entropy
    def __calcP__(self, total, some):
        return some / total
    def EParentFeature(self, breeds):
        expectations = []
        totalSum = 0
        for total, pos, neg in breeds:
            exp = self.__calcEntropy__(total, pos, neg)
            expectations.append(exp * total)
            totalSum += total
        eParent = 0.
        for exp in expectations:
            eParent += exp
        eParent = eParent / totalSum
        return eParent
