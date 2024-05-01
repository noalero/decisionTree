import feature
import node
import pandas as pd



class DecisionTree(object):
    def __init__(self, dataframe: pd.DataFrame, class_index: int, n_breeds=7) -> None:
        # ToDo
        # for each feature optional variable: n_breeds
        # Connect to database:
        database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
        self.__set_dataframe__(dataframe)
        self.__set_class_index__(class_index)
        # self.__set_engine__(database_url)
        self.__set_features__(n_breeds)
        self.__create_feature_types_list__()
        # self.__create_database__()
        self.__set_root__()

    def __set_features__(self, n_breeds: int) -> None:
        # ToDo: check [dataframe_columns] type
        dataframe_columns = self.dataframe.columns
        self.features: list[feature.Feature] = []
        for col in dataframe_columns:
            self.__add_feature__(col, n_breeds)

    @staticmethod
    def get_features(self) -> list[feature.Feature]:
        return self.features

    def __add_feature__(self, column_name: str, n_breeds: int) -> None:
        values = self.dataframe.get(column_name)
        feat = feature.Feature(column_name, values, n_breeds)
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
        self.feature_types_list: list[list[int]] = []

    def get_feature_types_list(self) -> list[list[int]]:
        # Should be private?
        return self.feature_types_list

    def add_feature_types_list(self, feature_type_: list[int]) -> None:
        self.feature_types_list.append(feature_type_)

    def __set_dataframe__(self, df: pd.DataFrame) -> None:
        self.dataframe = df

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe

    def __set_class_index__(self, class_index: int) -> None:
        self.class_index = class_index

    def get_class_index(self) -> int:
        return self.class_index










