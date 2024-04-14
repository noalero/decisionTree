import breed
import decisionTree


class Leaf(breed.Breed):
    def __init__(self, tree, name, datapath_):
        self.__set_tree__(tree)
        breed.Breed.__init__(self, name, datapath_)

# getters & setters of class attributes:
    # answer:
    def __set_answer__(self, answer) -> None:
        # ToDo
        # Use [self.tree] and [self.datapath] to get the percentage of each class
        self.answer = answer

    def get_answer(self) -> list:
        return self.answer

    # tree:
    def __set_tree__(self, tree) -> None:
        self.tree = tree

    def get_tree(self) -> decisionTree.DecisionTree:
        return self.tree
