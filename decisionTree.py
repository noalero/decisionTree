import feature
import categoricalFeature
import numericalFeature
import node
import breed
import leaf
import parent
import dataPath
import psycopg2
import numpy as np


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

# calculation related methods:
    # entropy:
    def __calc_entropy__(self, total, *args, **kwargs) -> float:
        if len(args) == 1 and isinstance(args[0], list) and not kwargs:
            return self.__calc_entropy_list__(total, args[0])
        elif 'pos' in kwargs and 'neg' in kwargs and len(kwargs) == 2 and not args:
            return self.__calc_entropy_bin__(total, kwargs['pos'], kwargs['neg'])
        else:
            raise ValueError("Invalid argument combination")

    def __calc_entropy_bin__(self, total, pos: int, neg: int) -> float:
        pos_p = self.__calc_p__(total, pos)
        neg_p = self.__calc_p__(total, neg)
        log_pos_p = np.log(pos_p)
        log_neg_p = np.log(neg_p)
        entropy = (pos_p * log_pos_p + neg_p * log_neg_p) * (-1.)
        return entropy

    def __calc_entropy_list__(self, total, classes: list[int]) -> float:
        mult_sum = 0.
        for cls in classes:
            p = self.__calc_p__(total, cls)
            log_p = np.log(p)
            p_log_p = p * log_p
            mult_sum += p_log_p
        entropy = mult_sum * (-1.)
        return entropy

    # calc_p:
    @staticmethod
    def __calc_p__(total, some) -> float:
        return some / total

    # e_parent_feature:
    def e_parent_feature(self, breeds_) -> float:
        # ToDo
        first_tuple = breeds_[0]
        if isinstance(first_tuple[1], list):
            func_call = self.__calc_entropy__(first_tuple[0], first_tuple[1])
        elif isinstance(first_tuple[1], int) and len(first_tuple) == 3 and isinstance(first_tuple[2], int):
            func_call = self.__calc_entropy__(first_tuple[0], pos=first_tuple[1], neg=first_tuple[2])
        else:
            raise TypeError("Unexpected tuple structure in breeds_ list")
        expectations = []
        total_sum = 0  # (0.?)
        for breed_ in breeds_:
            exp = func_call
            total = breed_[0]
            expectations.append(exp * total)
            total_sum += total
        e_parent = 0.
        for exp in expectations:
            e_parent += exp
        e_parent = e_parent / total_sum
        return e_parent

    # calc_information_gain:
    def __calc_information_gain__(self, breeds, total) -> float:
        # ToDo
        # From [feature_] get it's list of breeds [feature_.breeds]
        # From [datapath_] get pos, neg, total for each breed and create [breeds_] list
        pos = 0.0
        neg = 0.0
        entropy = self.__calc_entropy__(total, pos, neg)
        return 0.0








