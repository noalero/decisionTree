import numpy as np

import dataPath
import feature
# import numericalFeature
# import categoricalFeature
import breed
# import leaf
# import parent


class Node(object):
    def __init__(self, feature_, datapath_) -> None:
        # ToDo
        pass

# getters & setters of class attributes:
    # feature:
    def __set_feature__(self, feature_) -> None:
        self.feature = feature_

    def get_feature(self) -> feature.Feature:
        return self.feature

    # datapath:
    def __set_datapath__(self, datapath_) -> None:
        self.datapath = datapath_

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath

    # num_of_children:
    def __set_num_of_children__(self, num_of_children) -> None:
        self.num_of_children = num_of_children

    def get_num_of_children(self) -> int:
        return self.num_of_children

    # children:
    def __set_children__(self) -> None:
        # ToDo
        pass

    def get_children(self) -> breed.Breed:
        # ToDo
        pass
        # return self.children

#
    def __set_child__(self, child) -> None:
        # ToDo
        # __create_child__ or __add_child__ ?
        pass

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
