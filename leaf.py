import breed
import dataPath
import decisionTree


class Leaf(breed.Breed):
    def __init__(self, name: str, datapath_: dataPath.DataPath, serial_number: int):
        breed.Breed.__init__(self, name, datapath_, serial_number)

    def __set_answer__(self, answer) -> None:
        # ToDo
        # Use [self.datapath] to get the percentage of each class
        self.answer = answer

    def get_answer(self) -> list:
        return self.answer


