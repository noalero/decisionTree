import breed
import node


class Parent(breed.Breed):
    def __init__(self, name, datapath_, feature_):
        self.__create_next__(feature_, datapath_)
        breed.Breed.__init__(self, name, datapath_)

    def __set_next__(self, next_: node.Node) -> None:
        self.next = next_

    def get_next(self) -> node.Node:
        return self.next

    def __create_next__(self, feature_, datapath_) -> None:
        # ToDo
        # Use [self.tree] to choose the next feature
        new_feature = 0  # The chosen feature
        new_datapath = 0  # Add the [new_feature] to the [datapath]
        next_ = node.Node(new_feature, new_datapath)
        self.__set_next__(next_)

