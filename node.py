import brange
import dataPath
import feature
import node


class Node(object):
    def __init__(self, feature_: feature.Feature, datapath_: dataPath.DataPath) -> None:
        self.__set_feature__(feature_)
        self.__set_datapath__(datapath_)
        self.__init_num_of_children__()  # for initialization
        self.__set_children__()

    def __set_datapath__(self, datapath_: dataPath.DataPath) -> None:
        self.datapath = datapath_

    def __set_feature__(self, feature_: feature.Feature) -> None:
        self.feature = feature_

    def __init_num_of_children__(self) -> None:
        self.num_of_children = 0

    def __increase_num_of_children__(self) -> None:
        self.num_of_children += 1

    def __choose_feature_for_child__(self, breed_: str | brange.Range, feat_list: list[feature.Feature])\
            -> tuple[feature.Feature, float]:
        # TODO
        pass

    def __set_children__(self) -> None:
        self.children: list[node.Node] = []

    def __add_child__(self, breed_: str | brange.Range, child_feature: feature.Feature) -> None:
        # ToDo: test
        # child_feature = self.__choose_feature_for_child__(breed_, feat_list)
        new_dir = (self.feature, breed_)
        child_data_path = dataPath.DataPath(self.datapath.get_size(), self.datapath.get_path(), new_dir)
        new_child = node.Node(child_feature, child_data_path)
        self.children.append(new_child)
        self.__increase_num_of_children__()

    def get_feature(self) -> feature.Feature:
        return self.feature

    def get_datapath(self) -> dataPath.DataPath:
        return self.datapath

    def get_num_of_children(self) -> int:
        return self.num_of_children

    def get_children(self) -> list[node.Node]:
        return self.children

    def get_child(self, breed_: str | brange.Range) -> node.Node:
        for child in self.children:
            dp = child.get_datapath()
            dp_size = dp.get_size()
            last_dir = dp.get_path()[dp_size - 1]
            if last_dir[1] == breed_:
                return child
        raise ValueError(f"Child of breed {breed_} not found")

    def choose_next_for_children(self, feat_list: list[feature.Feature]) -> None:
        # ToDo: test
        feat_dict: dict[feature.Feature, tuple[str | brange.Range, float]] = {}  # key: feature, value: breed, IG
        unchosen_breeds: list[str | brange.Range] = self.feature.get_breeds()
        curr_feature_list: list[feature.Feature] = feat_list
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
            temp_feat, temp_ig = self.__choose_feature_for_child__(brd, curr_feature_list)
            unchosen_breeds.remove(brd)
            if temp_feat in feat_dict:
                old_breed, old_ig = feat_dict[temp_feat]
                if temp_ig > old_ig:
                    feat_dict[temp_feat] = (brd, temp_ig)
                    unchosen_breeds.append(old_breed)
                else:
                    unchosen_breeds.append(brd)
            else:
                feat_dict[temp_feat] = (brd, temp_ig)
