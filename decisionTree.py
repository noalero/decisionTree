import feature
import categoricalFeature
import numericalFeature
import node
import breed
import leaf
import parent
import dataPath


class DecisionTree(object):
    def __init__(self) -> None:
        pass

    def __set_features__(self) -> None:
        pass

    @staticmethod
    def get_features() -> list:
        return []  # self.features

    def __set_feature__(self) -> None:
        pass

    def __set_root__(self) -> None:
        pass

    @staticmethod
    def get_root() -> node.Node:
        # ToDo
        fe, de = 0, 0
        n = node.Node(fe, de)
        return n   # self.root

    def __create_database__(self) -> None:
        # ToDo return value
        pass

    def __create_feature_table__(self) -> None:
        # ToDo return value
        pass

    def retrieve_from_database(self, datapath_) -> None:
        # ToDo return value
        pass
