import breed


class Leaf(breed.Breed):
    def __init__(self, name, datapath_):
        breed.Breed.__init__(self, name, datapath_)

    def __set_answer__(self, answer) -> None:
        self.answer = answer

    def get_answer(self) -> list:
        # ToDo
        return self.answer
