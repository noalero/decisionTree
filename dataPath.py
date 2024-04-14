import feature
import numericalFeature
import categoricalFeature
import breed
import leaf
import parent
import decisionTree


class DataPath(object):
    def __init__(self, tree, size, orgnl_path, new_dir) -> None:
        self.__set_size__(size)
        self.__set_path__(orgnl_path, new_dir)
        self.__set_tree__(tree)

# getters & setters of class attributes:
    # size:
    def __set_size__(self, size) -> None:
        self.size = size

    def get_size(self) -> int:
        return self.size

    # path
    def __set_path__(self, orgnl_path, new_dir) -> None:
        # ToDo
        self.path = orgnl_path.append(new_dir)


    def get_path(self) -> list:
        return self.path

    # tree:
    def __set_tree__(self, tree) -> None:
        self.tree = tree

    def get_tree(self) -> decisionTree.DecisionTree:
        return self.tree

# addition methods (should delete):
    def add_feature(self, feature_) -> None:
        # ToDo
        pass
        # resize

    def add_breed(self, breed_) -> None:
        # ToDo
        pass  # resize
