import breed
class Leaf(breed.Breed):
    # answer
    def __init__(self, name, dataPath):
        breed.Breed.__init__(name, dataPath)
    def __setAnswer__(self, answer):
        self.answer = answer
    def getAnswer(self):
        return self.answer