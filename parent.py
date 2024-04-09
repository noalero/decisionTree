import breed
import node


class Parent(breed.Breed):
    def __init__(self, name, datapath_, feature_):
        breed.Breed.__init__(self, name, datapath_)
        self.__create_next__(feature_, datapath_)
        pass

    def __set_next__(self, next_) -> None:
        self.next = next_

    def get_next(self) -> node.Node:
        return self.next

    def __create_next__(self, feature, datapath_) -> None:
        pass
