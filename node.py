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
        pass

    def __set_feature__(self, feature_) -> None:
        self.feature = feature_

    def get_feature(self) -> feature.Feature:
        return self.feature

    def __set_datapath__(self, datapath_) -> None:
        self.datapath = datapath_

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath

    def __set_num_of_children__(self, num_of_children) -> None:
        self.num_of_children = num_of_children

    def get_num_of_children(self) -> int:
        return self.num_of_children

    def __set_children__(self) -> None:
        pass

    def get_children(self) -> breed.Breed:
        pass
        # return self.children

    def __set_child__(self, child) -> None:
        pass

    def get_child(self, breed_name) -> breed.Breed:
        pass

    def add_child(self, breed_, datapath_, arg) -> None:
        pass
        # create parent / lead, visitor pattern

    def choose_next_for_children(self) -> None:
        pass

    def __calc_entropy__(self, total, pos, neg) -> float:
        pos_p = self.__calc_p__(total, pos)
        neg_p = self.__calc_p__(total, neg)
        log_pos_p = np.log(pos_p)
        log_neg_p = np.log(neg_p)
        entropy = (pos_p * log_pos_p + neg_p * log_neg_p) * (-1.)
        return entropy

    @staticmethod
    def __calc_p__(total, some) -> float:
        return some / total

    def e_parent_feature(self, breeds) -> float:
        expectations = []
        total_sum = 0
        for total, pos, neg in breeds:
            exp = self.__calc_entropy__(total, pos, neg)
            expectations.append(exp * total)
            total_sum += total
        e_parent = 0.
        for exp in expectations:
            e_parent += exp
        e_parent = e_parent / total_sum
        return e_parent

    def __calc_information_gain__(self, breeds, total) -> float:
        # ToDo
        pos = 0.0
        neg = 0.0
        entropy = self.__calc_entropy__(total, pos, neg)
        return 0.0

    def __set_information_gain__(self) -> None:
        pass

    @staticmethod
    def get_information_gain() -> float:
        # ToDo
        return 0.0  # self.information_gain
