import feature
import categoricalFeature
import numericalFeature
import node
import breed
import leaf
import parent
import dataPath
import feature_type

import psycopg2
import numpy as np
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


class DecisionTree(object):
    def __init__(self, dataframe, class_index, n_breeds=7) -> None:
        # ToDo
        # for each feature optional variable: n_breeds
        # Connect to database:
        database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
        self.__set_dataframe__(dataframe)
        self.__set_class_index__(class_index)
        self.__set_engine__(database_url)
        self.__set_features__(n_breeds)
        self.__create_feature_types_list__()
        self.__create_database__()
        self.__set_root__()

# getters & setters of class attributes:
    # features:
    def __set_features__(self, n_breeds) -> None:
        # ToDo: check [dataframe_columns] type
        dataframe_columns = list[self.dataframe.columns]
        self.features = []
        for col in dataframe_columns:
            self.__add_feature__(col, n_breeds)

    @staticmethod
    def get_features(self) -> list:
        return self.features

    def __add_feature__(self, column_name, n_breeds) -> None:
        values = self.dataframe.get(column_name)
        feat = feature.Feature(column_name, values, n_breeds)
        self.features.append(feat)

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
        self.feature_types_list = []

    def get_feature_types_list(self) -> list:
        # Should be private?
        return self.feature_types_list

    def add_feature_types_list(self, feature_type) -> None:
        self.feature_types_list.append(feature_type)

    # engine:
    def __set_engine__(self, database_url):
        self.engine = sa.create_engine(database_url)

    def __get_engine__(self):
        return self.engine

    # session:
    def __set_session__(self) -> None:
        self.session = sa.orm.sessionmaker(bind=self.engine)

    def get_session(self) -> sa.orm.sessionmaker:
        return self.session

    # data_frame:
    def __set_dataframe__(self, df) -> None:
        self.dataframe = df

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe

    # class_index:
    def __set_class_index__(self, class_index) -> None:
        self.class_index = class_index

    def get_class_index(self) -> int:
        return self.class_index

# database related methods:
    def __create_database__(self) -> None:
        # ToDo return value
        self.__create_trainingdata_primary_table__()
        self.__create_feature_type_table__()
        self.__create_result_table__()

    def __create_trainingdata_primary_table__(self) -> None:
        self.dataframe.to_sql(
            "TrainingDataPrimaryTable", con=self.engine, index=True, index_label='index', if_exists='replace')

    def select_from_primary_table(self, columns, wheres) -> sa.Sequence:
        column_names = ', '.join(map(lambda x: f'"{x}"', columns))
        wheres_names = ' AND '.join(map(lambda where: f'"{where[0]}" = {where[1]}', wheres))
        select_command = sa.text(f'''SELECT {column_names} FROM "TrainingDataPrimaryTable" WHERE {wheres_names}''')
        with self.engine.connect() as connection:
            result = connection.execute(select_command)
            connection.commit()
            connection.close()
        ans = result.fetchall()
        return ans

    def __create_feature_type_table__(self) -> None:
        feature_type.Base.metadata.create_all(self.engine)

    def insert_feature_type_table(self, featype, featype_val) -> None:
        session = self.session()
        new_row = feature_type.FeatureTypeObject(feature_type=featype, feature_type_value=featype_val)
        session.add(new_row)
        session.commit()
        session.close()

    def select_feature_type_table(self, columns, wheres) -> sa.Sequence:
        column_names = ', '.join(map(lambda x: f'"{x}"', columns))
        wheres_names = ' AND '.join(map(lambda where: f'"{where[0]}" = ARRAY {where[1]}', wheres))
        select_command = sa.text(f'''SELECT {column_names} FROM "FeatureTypeTable" WHERE {wheres_names}''')
        with self.engine.connect() as connection:
            result = connection.execute(select_command)
            connection.commit()
            connection.close()
        ans = result.fetchall()
        return ans

    def __create_result_table__(self) -> None:
        # ToDo
        self.result_table = []  # database create

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








