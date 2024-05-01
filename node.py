import numpy as np

import dataPath
import feature
import breed
import decisionTree


class Node(object):
    def __init__(self, feature_, datapath_) -> None:
        self.__set_feature__(feature_)
        self.__set_datapath__(datapath_)

    def __set_datapath__(self, datapath_) -> None:
        self.datapath = datapath_

    def __set_feature__(self, feature_) -> None:
        self.feature = feature_

    def __set_num_of_children__(self, num_of_children) -> None:
        self.num_of_children = num_of_children

    def __set_children__(self) -> None:
        # ToDo
        pass

    def __set_child__(self, child) -> None:
        # ToDo
        # __create_child__ ?
        pass

    def get_feature(self) -> feature.Feature:
        return self.feature

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath

    def get_num_of_children(self) -> int:
        return self.num_of_children

    def get_children(self) -> breed.Breed:
        # ToDo
        pass
        # return self.children

    def get_child(self, breed_name) -> breed.Breed:
        # ToDo
        pass

    def add_child(self, breed_, datapath_, arg) -> None:
        # ToDo
        pass
        # create parent / leaf, visitor pattern

    def choose_next_for_children(self) -> None:
        # ToDo
        pass
