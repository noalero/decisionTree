import feature
import categoricalFeature
import numericalFeature
import node
import breed
import leaf
import parent
import dataPath
import psycopg2


class DecisionTree(object):
    def __init__(self, dataset) -> None:
        # ToDo
        # for each feature optional variable: n_breeds
        # Connect to database:
        self.conn = psycopg2.connect(dbname="DecisionTreeTrial",
                                     user="NoaLeron",
                                     password="tsmOn8tln",
                                     host="localhost")
        self.__set_features__(dataset)
        self.__set_root__()

# getters & setters of class attributes:
    # features:
    def __set_features__(self, dataset) -> None:
        # ToDo
        self.features = []

    @staticmethod
    def get_features(self) -> list:
        # ToDo
        return self.features

    def __set_feature__(self) -> None:
        # ToDo
        pass

    # root:
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

    # feature_types_list
    def __create_feature_types_list__(self) -> None:
        # Should be in __init__ instead?
        self.feature_types_list = []

    def get_feature_types_list(self) -> list:
        # Should be private?
        return self.feature_types_list

    def add_feature_types_list(self, feature_type) -> None:
        self.feature_types_list.append(feature_type)


# database related methods:
    def __create_database__(self, dataset) -> None:
        # ToDo return value
        pass

    def __create_trainingdata_primary_table__(self) -> None:
        # ToDo return value
        pass

    def __create_feature_type_table__(self) -> None:
        # ToDo return value
        pass

    def insert_feature_type_table(self, feature_type) -> None:
        # ToDo
        pass

    def __create_result_table__(self) -> None:
        # ToDo
        self.result_table = []  # database create
        for featype in self.feature_types_list:
            self.insert_result_table(featype.rule_id, featype.classes_item_percentage_list)
            pass

    def insert_result_table(self, rule_id, classes_item_percentage_list) -> None:
        # ToDo
        # database insert
        pass







