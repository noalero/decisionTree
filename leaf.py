import breed
class Leaf(breed.Breed):
    def __init__(self, name, dataPath, answer):
        breed.Breed.__init__(name, dataPath)
    def __setAnswer__(self, answer):
        self.answer = answer
    def getAnswer(self):
        return self.answer