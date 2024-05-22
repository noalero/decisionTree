from __future__ import annotations

from brange import Range
from dataPath import DataPath
from feature import Feature
from breed import Breed
import tree_calculations as tc


class Node(object):
    def __init__(self, feature_: Feature, datapath_: DataPath) -> None:
        self.__set_feature__(feature_)
        self.__set_datapath__(datapath_)
        self.__init_num_of_children__()  # for initialization
        self.__set_children__()

    def __set_datapath__(self, datapath_: DataPath) -> None:
        self.datapath = datapath_

    def __set_feature__(self, feature_: Feature) -> None:
        self.feature = feature_

    def __init_num_of_children__(self) -> None:
        self.num_of_children = 0

    def __increase_num_of_children__(self) -> None:
        self.num_of_children += 1

    def __choose_feature_for_child__(self, breed_: Breed, feat_list: list[Feature],
                                     classes: list[str]) -> tuple[Feature, float]:
        # TODO: test
        inf_gain = 0
        ret_feature = feat_list[0]
        for feature_ in feat_list:
            feature_dir = (self.feature, breed_)
            feature_dp = DataPath(self.datapath.get_size(), self.datapath.get_path(), feature_dir)
            cur_ig = tc.calc_feature_information_gain(feature_, feature_dp, classes)
            if cur_ig > inf_gain:
                inf_gain = cur_ig
                ret_feature = feature_
        return ret_feature, inf_gain

    def __set_children__(self) -> None:
        self.children: list[Node] = []

    def __add_child__(self, breed_: Breed, child_feature: Feature) -> None:
        # ToDo: test
        new_dir = (self.feature, breed_)
        child_data_path = DataPath(self.datapath.get_size(), self.datapath.get_path(), new_dir)
        new_child = Node(child_feature, child_data_path)
        self.children.append(new_child)
        self.__increase_num_of_children__()

    def get_feature(self) -> Feature:
        return self.feature

    def get_datapath(self) -> DataPath:
        return self.datapath

    def get_num_of_children(self) -> int:
        return self.num_of_children

    def get_children(self) -> list[Node]:
        return self.children

    def get_child(self, breed_: Breed) -> Node:
        for child in self.children:
            dp = child.get_datapath()
            dp_size = dp.get_size()
            last_dir = dp.get_path()[dp_size - 1]
            if last_dir[1] == breed_:
                return child
        raise ValueError(f"Child of breed {breed_} not found")

    def choose_next_for_children(self, feat_list: list[Feature], classes: list[str]) -> None:
        # ToDo: test
        feat_dict: dict[Feature, tuple[Breed, float]] = {}  # key: feature, value: breed, IG
        unchosen_breeds: set[Breed] = self.feature.get_breeds()
        curr_feature_list: list[Feature] = feat_list
        i: int = 0
        org_size = len(unchosen_breeds)
        for brd in unchosen_breeds:
            if i == org_size:
                for feat, tup in feat_dict:
                    # add children from [feat_dict]:
                    self.__add_child__(tup[0], feat)
                    # empty [feat_dict]:
                    del feat_dict[feat]
                    # remove features from [curr_feature_list]:
                    curr_feature_list.remove(feat)
                # new value to org_size:
                org_size = len(unchosen_breeds)
                # restart i:
                i = 0
            i += 1
            temp_feat, temp_ig = self.__choose_feature_for_child__(brd, curr_feature_list, classes)
            unchosen_breeds.remove(brd)
            if temp_feat in feat_dict:
                old_breed, old_ig = feat_dict[temp_feat]
                if temp_ig > old_ig:
                    feat_dict[temp_feat] = (brd, temp_ig)
                    unchosen_breeds.add(old_breed)
                else:
                    unchosen_breeds.add(brd)
            else:
                feat_dict[temp_feat] = (brd, temp_ig)

    def is_leaf(self) -> bool:
        last_dir = self.datapath.get_path()[self.datapath.get_size() - 1]
        last_feature_name = last_dir[0].get_name()
        return last_feature_name == self.feature.get_name()

