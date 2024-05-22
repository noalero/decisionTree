import pandas as pd
import numbers

import config
import visitor
from visitor import ConcreteFeatureVisitor
from feature import Feature
import numericalFeature
import categoricalFeature
from node import Node
from dataPath import DataPath
from breed import Breed


class DecisionTree(object):
    def __init__(self, dataframe: pd.DataFrame, class_index: int, n_breeds=4) -> None:
        # ToDo
        # for each feature optional variable: n_breeds
        self.__set_dataframe__(dataframe)
        self.__set_class_index__(class_index)
        self.__set_n_breeds(n_breeds)
        self.__set_visitor__()
        self.__set_features__()
        self.__set_classes__()
        self.__create_feature_types_list__()
        self.__set_root__()

    # TODO: deal with class column (should be a feature? not in the features list, special attribute?)

    def __set_n_breeds(self, n_breeds: int) -> None:
        self.n_breeds = n_breeds

    def get_n_breeds(self) -> int:
        return self.n_breeds

    def __set_visitor__(self) -> None:
        self.visitor = ConcreteFeatureVisitor()

    def get_visitor(self) -> visitor.ConcreteFeatureVisitor:
        return self.visitor

    def __set_features__(self) -> None:
        # ToDo: check [dataframe_columns] type
        dataframe_columns = self.dataframe.columns
        self.features: list[Feature] = []
        serial_number = 1
        for col in dataframe_columns:
            if col != "class":
                self.__add_feature__(col, serial_number)
                serial_number += 1

    def __add_feature__(self, column_name: str, serial_number: int) -> None:
        feat = self.create_feature(column_name, serial_number)
        self.features.append(feat)

    def create_feature(self, column_name: str, serial_number: int) -> Feature:
        val = self.dataframe[column_name].iloc[0]
        if isinstance(val, numbers.Number):
            feature_ = numericalFeature.NumericalFeature(column_name, self.n_breeds, serial_number)
        elif isinstance(val, str):
            feature_ = categoricalFeature.CategoricalFeature(column_name, self.n_breeds, serial_number)
        else:
            raise ValueError("Invalid feature type")
        feature_.accept(self.visitor)
        return feature_

    def get_features(self) -> list[Feature]:
        return self.features

    def __set_root__(self, feature_: Feature) -> None:
        empty_dp = DataPath(0, [])
        self.root = Node(feature_, empty_dp)

    def get_root(self) -> Node:
        return self.root

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

    def __set_classes__(self) -> None:
        classes_feature = Feature("classes", self.n_breeds, -1)
        self.classes = classes_feature

    def get_classes(self) -> Feature:
        return self.classes
