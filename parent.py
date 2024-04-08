import breed
class Parent(breed.Breed):
    def __init__(self, name, dataPath, feature):
        breed.Breed.__init__(name, dataPath)
        self.__createNext__(feature, dataPath)
    def __setNext__(self, next):
        self.next = next
    def getNext(self):
        return self.next
    def __createNext__(self, feature, dataPath):
        pass