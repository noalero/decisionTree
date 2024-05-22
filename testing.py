import numpy as np
import pandas as pd
import psycopg2
import sqlite3
import sqlalchemy as sa

import config
from feature import Feature
import tree_data_bases as tdb
import tree_calculations as tclc
from brange import Range
from breed import Breed
from dataPath import DataPath


def main_tree_db_prim() -> None:
    # Sample Data Frame:
    data = {'name': ['Alise', 'Bob', 'Colin', 'Daphne', 'Eduard'], 'id': [12, 34, 56, 78, 90], 'feature1': [10, 15, 25, 12, 30],
            'feature2': ['val2', 'val2', 'val3', 'val2', 'val1'], 'feature3': ['1', '2', '4', '2', '5'], 'gender': ['female', 'male', 'male', 'female', 'male']}
    dataframe = pd.DataFrame(data)
    # Create Primary Table from Data Frame:
    tdb.__create_primary_from_dataframe__(dataframe, 5)
    # Columns to Select:
    columns = ['name', 'id', 'feature2']
    # Where Map:
    where1 = {'feature2': 'val2', 'feature3': '1'}
    where2 = {'feature1': Range(10, 15)}
    wheres = [where1, where2]
    # Select
    result = tdb.select_table(columns, wheres, "TrainingDataPrimaryTable")
    for row in result:
        print(row)


def main_tree_db_ftype() -> None:
    # ============================ Basic ============================ #
    #                Create table:
    tdb.__create_feature_type_table__()
    #                Insert single rows:
    tdb.insert_single_row_feature_type_table('Type3', 'Value1')
    tdb.insert_single_row_feature_type_table('Type2', 'Value3')
    tdb.insert_single_row_feature_type_table('Type2', 'Value2')
    tdb.insert_single_row_feature_type_table('Type1', 'Value2')
    #                Insert multiple rows:
    row1 = {'f_type': 'Type4', 'f_val': 'Value1'}
    row2 = {'f_type': 'Type4', 'f_val': 'Value2'}
    row3 = {'f_type': 'Type4', 'f_val': 'Value3'}
    row4 = {'f_type': 'Type4', 'f_val': 'Value1'}
    rows: list[dict] = [row1, row2, row3, row4]
    inserted_rows = tdb.insert_multiple_rows_feature_type_table(rows)
    print("Number of rows inserted: ", inserted_rows)
    #                Select:
    columns = ['rule_id', 'f_val']
    where1 = {'f_val': 'Value1', 'f_type': 'Type1'}
    where2 = {'f_val': 'Value1', 'f_type': 'Type2'}
    where3 = {'rule_id': Range(2, 17)}
    wheres = [where1, where2, where3]
    result = tdb.select_table(columns, wheres, "FeatureTypeTable")
    for row in result:
        print(row)
    # ============================ With classes ============================ #
    classes = ['Class1', 'Class2', 'Class3']
                   # Create table:
    result = tdb.__create_feature_type_table_classes__(classes)
    print(result)
    #                 Insert single row:
    f_type = 'Type1'
    f_val = 'Value1'
    class_dict = {'Class1': 12, 'Class2': 7, 'Class3': 2}
    result = tdb.insert_single_row_feature_type_table_classes(f_type, f_val, class_dict)
    print(result)
    #                 Insert multiple row:
    dict1 = {'f_type': 'Type3', 'f_val': 'Value1', 'Class1': 1, 'Class2': 1, 'Class3': 1}
    dict2 = {'f_type': 'Type3', 'f_val': 'Value2', 'Class1': 2, 'Class2': 2, 'Class3': 2}
    dict3 = {'f_type': 'Type3', 'f_val': 'Value3', 'Class1': 3, 'Class2': 3, 'Class3': 3}
    dict_list = [dict1, dict2, dict3]
    result = tdb.insert_multiple_rows_feature_type_table_classes(dict_list)
    print(result)


def main_tree_db_result() -> None:
    #                Create:                #
    class_names = ['A', 'B', 'C', 'D']
    ans = tdb.__create_result_table__(class_names)
    print(ans)
    #                Insert:                #
    row1 = {'rule_id': 1,
            'A': 5,
            'B': 10,
            'C': 0,
            'D': 20}
    row2 = {'rule_id': 2,
            'A': 0,
            'B': 10,
            'C': 9,
            'D': 21}
    row3 = {'rule_id': 7,
            'A': 0,
            'B': 0,
            'C': 13,
            'D': 21}
    rows = [row3, row2, row1]
    ans = tdb.insert_result_table(rows)
    print(ans)
    #                Select:                #
    cond1 = {'f_type': "Type1", 'f_val': "Value1"}
    cond2 = {'f_type': "Type3", 'f_val': "Value1"}
    conditions = [cond1, cond2]
    ans = tdb.select_result_table(class_names, conditions)
    print(ans)


def main_calc_basic() -> None:
    # <total, list: classes> || <total, pos, neg>
    # classes: A, B, C, D
    parent_classesA = [14, 16]
    breed1_classesA = [1, 12]
    breed2_classesA = [13, 4]
    breedsA = [breed1_classesA, breed2_classesA]
    parent_classesB = [14, 16]
    breed1_classesB = [1, 7]
    breed2_classesB = [6, 4]
    breed3_classesB = [7, 5]
    breedsB = [breed1_classesB, breed2_classesB, breed3_classesB]
    ig = tclc.calc_information_gain(breedsB, parent_classesB)
    print("information gain: ", ig)


def main_db_calc() -> None:
    # Sample Data Frame:
    data = {'name': ['Alise', 'Bob', 'Colin', 'Daphne', 'Eduard'], 'id': [12, 34, 56, 78, 90],
            'feature1': [10, 15, 25, 12, 30],
            'feature2': ['val2', 'val2', 'val3', 'val2', 'val1'], 'feature3': ['1', '2', '4', '2', '5'],
            'gender': ['female', 'male', 'male', 'female', 'male']}
    dataframe = pd.DataFrame(data)
    # Create Primary Table from Data Frame:
    tdb.__create_primary_from_dataframe__(dataframe, 5)
    # ToDo: use visitor
    feature1 = Feature("feature1", 3, 1)
    feature2 = Feature("feature2", 3, 2)
    feature3 = Feature("feature3", 3, 3)
    breed1 = Breed(Range(10, 16.33), 1)
    breed2 = Breed("val2", 1)
    breed3 = Breed('2', 2)
    data_path = DataPath(0, [(feature1, breed1), (feature2, breed2)], (feature3, breed3))
    classes = ['female', 'male']
    cls_amnt = tdb.get_path_classes_amounts(data_path, classes)
    print(cls_amnt)

    # _____________________________ CALC: _____________________________
    # calc_feature_breeds_amount(feat: Feature, dp: DataPath, classes: list[str]) -> list[list[int]]
    # calc_feature_entropy(feat: Feature, dp: DataPath, classes: list[str]) -> float
    # calc_feature_information_gain(feat: Feature, dp: DataPath, classes: list[str]) -> float
    #
    # _____________________________ DB: _____________________________
            # __create_primary_from_dataframe__(dataframe: pd.DataFrame, class_index: int) -> None
            # add_class_column(dataframe: pd.DataFrame, class_index: int) -> pd.DataFrame
            # __create_feature_type_table__() -> str
                    # __create_feature_type_table_classes__(class_names: list[str]) -> str
            # insert_single_row_feature_type_table(f_type, f_val) -> str
                    # insert_single_row_feature_type_table_classes(f_type: str, f_val: str, classes: dict[str, int]) -> str
            # insert_multiple_rows_feature_type_table(rows: list[dict]) -> int
                    # insert_multiple_rows_feature_type_table_classes(rows: list[dict[str, int | str]]) -> int
            # __create_result_table__(class_names: list[str]) -> str
            # insert_result_table(rows: list[dict[str, int]]) -> int
    ##### select_result_table(class_names: list[str], conditions: list[dict[str, str]])
    # get_path_classes_amounts(dt_path: DataPath, classes: list[str]) -> list[int]
    a = 5


def main() -> None:
    # main_entropy()
    # main_basic_database()
    # main_specific_database()
    # main_tree_db_prim()
    # main_tree_db_ftype()
    # main_tree_db_result()
    # main_calc_basic()
    main_db_calc()

if __name__ == "__main__":
    main()
