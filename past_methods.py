import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from typing import Union
import numpy as np

import feature
import brange


# ------------------------------ decision tree ------------------------------
# database related methods:
def __create_database__(self) -> None:
    # ToDo return value
    self.__create_trainingdata_primary_table__()
    self.__create_feature_type_table__()
    self.__create_result_table__()


def __create_trainingdata_primary_table__(self) -> None:
    self.dataframe.to_sql(
        "TrainingDataPrimaryTable", con=self.engine, index=True, index_label='index', if_exists='replace')


def select_from_primary_table(self, columns: list[feature.Feature], wheres: list[tuple[feature.Feature, Union[brange.Range, str]]]) -> sa.Sequence:
    # ToDo: check
    column_names = ', '.join(map(lambda x: f'"{x.get_name}"', columns))
    where_list: list[str] = []
    for tup in wheres:
        if isinstance(tup[1], brange.Range):
            where_str = f'''"{tup[0].get_name()}" >= {tup[1].get_from_index()} AND "{tup[0].get_name()}" < {tup[1].get_to_index()}'''
            where_list.append(where_str)
        elif isinstance(tup[1], str):
            where_str = f'''"{tup[0].get_name()}" == "{tup[1]}"'''
            where_list.append(where_str)
    wheres_names = ' AND '.join(map(lambda where_str: f'{where_str}', where_list))
    select_command = sa.text(f'''SELECT {column_names} FROM "TrainingDataPrimaryTable" WHERE {wheres_names}''')
    with self.engine.connect() as connection:
        result = connection.execute(select_command)
        connection.commit()
        connection.close()
    ans = result.fetchall()
    return ans


# def __create_feature_type_table__(self) -> None:
#     # ToDo
#     feature_type.Base.metadata.create_all(self.engine)


# def insert_feature_type_table(self, featype: list[int], featype_val: list[int]) -> None:
#     session = self.session()
#     try:
#         new_row = feature_type.FeatureTypeObject(feature_type=featype, feature_type_value=featype_val)
#         session.add(new_row)
#         session.commit()
#     except sa.exc.IntegrityError as e:
#         if 'already exists' in str(e):
#             print(
#                 f"An entry with the same combination of feature_type and feature_type_value already exists: {featype}, {featype_val}")
#         else:
#             print(f"A database integrity error occurred: {str(e)}")
#         session.rollback()
#     except Exception as e:
#         print(f"An unexpected error occurred: {str(e)}")
#         session.rollback()
#     finally:
#         session.close()


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
def __calc_p__(total, some) -> float:
    return some / total


# e_parent_feature:
def e_parent_feature(self, breeds_: list[tuple]) -> float:
    # ToDo
    first_tuple = breeds_[0]
    if isinstance(first_tuple[1], list):
        func_call = self.__calc_entropy__(first_tuple[0], first_tuple[1])
    elif isinstance(first_tuple[1], int) and len(first_tuple) == 3 and isinstance(first_tuple[2], int):
        func_call = self.__calc_entropy__(first_tuple[0], pos=first_tuple[1], neg=first_tuple[2])
    else:
        raise TypeError("Unexpected tuple structure in breeds_ list")
    expectations: list[float] = []
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
    return entropy


# engine:
def __set_engine__(self, database_url) -> None:
    self.engine = sa.create_engine(database_url)


def __get_engine__(self) -> sa.engine:
    return self.engine


# session:
def __set_session__(self) -> None:
    self.session = sa.orm.sessionmaker(bind=self.engine)


def get_session(self) -> sa.orm.sessionmaker:
    return self.session
