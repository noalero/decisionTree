import config
import feature
import node
import pandas as pd


class DecisionTree(object):
    def __init__(self, dataframe: pd.DataFrame, class_index: int, n_breeds=7) -> None:
        # ToDo
        # for each feature optional variable: n_breeds
        self.__set_dataframe__(dataframe)
        self.__set_class_index__(class_index)
        self.__set_n_breeds(n_breeds)
        self.__set_features__()
        self.__create_feature_types_list__()
        self.__set_root__()

    def __set_n_breeds(self, n_breeds: int) -> None:
        self.n_breeds = n_breeds

    def get_n_breeds(self) -> int:
        return self.n_breeds

    def __set_features__(self) -> None:
        # ToDo: check [dataframe_columns] type
        dataframe_columns = self.dataframe.columns
        self.features: list[feature.Feature] = []
        serial_number = 1
        for col in dataframe_columns:
            self.__add_feature__(col, serial_number)
            serial_number += 1

    @staticmethod
    def get_features(self) -> list[feature.Feature]:
        return self.features

    def __add_feature__(self, column_name: str, serial_number: int) -> None:
        feat = feature.Feature(column_name, self.n_breeds, serial_number)
        self.features.append(feat)

    def __set_root__(self) -> None:
        # ToDo
        # empty datapath, choose first feature
        pass

    @staticmethod
    def get_root() -> node.Node:
        # ToDo
        fe, de = 0, 0
        n = node.Node(fe, de)
        return n   # self.root

    def __create_feature_types_list__(self) -> None:
        # TODO: type (each feature_type will be [data_path]?
        self.feature_types_list: list[list[int]] = []

    def get_feature_types_list(self) -> list[list[int]]:
        # TODO: return type
        # Should be private?
        return self.feature_types_list

    def add_feature_types_list(self, feature_type_: list[int]) -> None:
        # TODO: [feature_type_] type
        self.feature_types_list.append(feature_type_)

    def __set_dataframe__(self, df: pd.DataFrame) -> None:
        self.dataframe = df

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe

    def __set_class_index__(self, class_index: int) -> None:
        self.class_index = class_index

    def get_class_index(self) -> int:
        return self.class_index










