import numpy as np
import pandas as pd
import psycopg2

import sqlite3
import sqlalchemy as sa
import testing_c

import config
import feature
import tree_data_bases as tdb
import tree_calculations as tclc
import brange as br

# from sqlalchemy import create_engine
# from sqlalchemy import text
# from sqlalchemy import insert


# entropy:
def __calc_entropy__(total, *args, **kwargs) -> float:
    if len(args) == 1 and isinstance(args[0], list) and not kwargs:
        return __calc_entropy_list__(total, args[0])
    elif 'pos' in kwargs and 'neg' in kwargs and len(kwargs) == 2 and not args:
        return __calc_entropy_bin__(total, kwargs['pos'], kwargs['neg'])
    else:
        raise ValueError("Invalid argument combination")


def __calc_entropy_bin__(total, pos: int, neg: int) -> float:
    pos_p = __calc_p__(total, pos)
    neg_p = __calc_p__(total, neg)
    log_pos_p = np.log(pos_p)
    log_neg_p = np.log(neg_p)
    entropy = (pos_p * log_pos_p + neg_p * log_neg_p) * (-1.)
    return entropy


def __calc_entropy_list__(total, classes: list[int]) -> float:
    mult_sum = 0.
    for cls in classes:
        p = __calc_p__(total, cls)
        log_p = np.log(p)
        p_log_p = p * log_p
        mult_sum += p_log_p
    entropy = mult_sum * (-1.)
    return entropy


def __calc_p__(total, some) -> float:
    return some / total


def e_parent_feature(breeds_) -> float:
    # ToDo
    first_tuple = breeds_[0]
    if isinstance(first_tuple[1], list):
        func_call = __calc_entropy__(first_tuple[0], first_tuple[1])
    elif isinstance(first_tuple[1], int) and len(first_tuple) == 3 and isinstance(first_tuple[2], int):
        func_call = __calc_entropy__(first_tuple[0], pos=first_tuple[1], neg=first_tuple[2])
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


def main_entropy() -> None:
    breeds1 = [(10, 5, 5), (13, 3, 10), (7, 2, 5)]
    breeds2 = [(15, [7, 6, 2]), (20, [1, 14, 5]), (9, [3, 1, 5])]
    e1 = e_parent_feature(breeds1)
    print(f'e1 is: {e1=}')
    e2 = e_parent_feature(breeds2)
    print(f'e2 is: {e2=}')


# database:
def create_table_from_dataframe(engine, df, table_name) -> None:
    df.to_sql(table_name, con=engine, index=True, index_label='index', if_exists='replace')


def insert_into_table(engine, table_name, values, columns) -> None:
    column_names = ', '.join([f'"{col}"' for col in columns])
    value_names = ', '.join([f'{val}' for val in values])
    get_max_command = sa.text(f'''SELECT MAX(\"index\") FROM {table_name}''')
    with engine.connect() as connection:
        max_index_result = connection.execute(get_max_command)
        max_index = max_index_result.scalar()
        next_index = max_index + 1 if max_index is not None else 0
        connection.close()
    insert_command = sa.text(
        f'''INSERT INTO {table_name} (\"index\", {column_names}) VALUES ({next_index}, {value_names})''')
    with engine.connect() as connection:
        result = connection.execute(insert_command)
        connection.commit()
        connection.close()


def select_from_table(engine, table_name, columns, wheres) -> list:
    column_names = ', '.join(map(lambda x: f'"{x}"', columns))
    wheres_names = ' OR '.join(map(lambda where: f'"{where[0]}" = {where[1]}', wheres))
    select_command = sa.text(f'''SELECT {column_names} FROM "{table_name}" WHERE {wheres_names}''')
    with engine.connect() as connection:
        result = connection.execute(select_command)
        connection.commit()
        connection.close()
    ans = result.fetchall()
    return ans


def main_basic_database() -> None:
    database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/TestingDT"
    engine = sa.create_engine(database_url)
    df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Apple', 'Banana', 'Cherry', 'Orange'],
        'amount': [3, 10, 5, 7]
    })
    table_name = 'fruits'
    create_table_from_dataframe(engine, df, table_name)
    df_columns = list(df.columns)
    insert_into_table(engine, "fruits", [5, "'Grape'", 1], df_columns)
    selected = select_from_table(engine, 'fruits', ['name', 'amount'], [('id', 3), ('id', 5)])


def main_specific_database() -> None:
    database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/TestingDT"
    engine = sa.create_engine(database_url)
    test_c = testing_c.TestingC(database_url)
    test_c.create_feature_type_table(engine)
    test_c.insert_feature_type_table([1, 1, 3], [7, 7, 6])
    ans = test_c.select_feature_type_table(['rule_id'], [('feature_type', [1, 2, 3]), ('feature_type_value', [1, 1, 2])])
    print(ans)


def main_tree_db_prim() -> None:
    # URL:
    database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"

    # Sample Data Frame:
    data = {'name': ['Alise', 'Bob', 'Colin', 'Daphne', 'Eduard'], 'id': [12, 34, 56, 78, 90], 'feature1': [10, 15, 25, 12, 30],
            'feature2': ['val2', 'val2', 'val3', 'val2', 'val1'], 'feature3': ['1', '2', '4', '2', '5']}
    dataframe = pd.DataFrame(data)
    # Create Primary Table from Data Frame:
    tdb.__create_primary_from_dataframe__(dataframe, database_url)
    # Columns to Select:
    columns = ['name', 'id', 'feature2']
    # Where Map:
    where1 = {'feature2': 'val2', 'feature3': '1'}
    where2 = {'feature1': br.Range(10, 15)}
    wheres = [where1, where2]
    # Select
    engine = tdb.connect_db(database_url)
    result = tdb.select_table(columns, wheres, engine, "TrainingDataPrimaryTable")
    for row in result:
        print(row)


def main_tree_db_ftype() -> None:
    # URL:
    database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
    engine: sa.engine = tdb.connect_db(database_url)
    # ============================ Basic ============================ #
    #                Create table:
    tdb.__create_feature_type_table__(engine)
    #                Insert single rows:
    tdb.insert_single_row_feature_type_table(engine, 'Type3', 'Value1')
    tdb.insert_single_row_feature_type_table(engine, 'Type2', 'Value3')
    tdb.insert_single_row_feature_type_table(engine, 'Type2', 'Value2')
    tdb.insert_single_row_feature_type_table(engine, 'Type1', 'Value2')
    #                Insert multiple rows:
    row1 = {'f_type': 'Type4', 'f_val': 'Value1'}
    row2 = {'f_type': 'Type4', 'f_val': 'Value2'}
    row3 = {'f_type': 'Type4', 'f_val': 'Value3'}
    row4 = {'f_type': 'Type4', 'f_val': 'Value1'}
    rows: list[dict] = [row1, row2, row3, row4]
    inserted_rows = tdb.insert_multiple_rows_feature_type_table(engine, rows)
    print("Number of rows inserted: ", inserted_rows)
    #                Select:
    columns = ['rule_id', 'f_val']
    where1 = {'f_val': 'Value1', 'f_type': 'Type1'}
    where2 = {'f_val': 'Value1', 'f_type': 'Type2'}
    where3 = {'rule_id': br.Range(2, 17)}
    wheres = [where1, where2, where3]
    result = tdb.select_table(columns, wheres, engine, "FeatureTypeTable")
    for row in result:
        print(row)
    # ============================ With classes ============================ #
    classes = ['Class1', 'Class2', 'Class3']
                   # Create table:
    result = tdb.__create_feature_type_table_classes__(engine, classes)
    print(result)
    #                 Insert single row:
    f_type = 'Type1'
    f_val = 'Value1'
    class_dict = {'Class1': 12, 'Class2': 7, 'Class3': 2}
    result = tdb.insert_single_row_feature_type_table_classes(engine, f_type, f_val, class_dict)
    print(result)
    #                 Insert multiple row:
    dict1 = {'f_type': 'Type3', 'f_val': 'Value1', 'Class1': 1, 'Class2': 1, 'Class3': 1}
    dict2 = {'f_type': 'Type3', 'f_val': 'Value2', 'Class1': 2, 'Class2': 2, 'Class3': 2}
    dict3 = {'f_type': 'Type3', 'f_val': 'Value3', 'Class1': 3, 'Class2': 3, 'Class3': 3}
    dict_list = [dict1, dict2, dict3]
    result = tdb.insert_multiple_rows_feature_type_table_classes(engine, dict_list)
    print(result)


def main_tree_db_result() -> None:
    # URL:
    database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
    engine: sa.engine = tdb.connect_db(database_url)
    #                Create:                #
    class_names = ['A', 'B', 'C', 'D']
    # ans = tdb.__create_result_table__(engine,class_names)
    # print(ans)
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
    # ans = tdb.insert_result_table(engine, rows)
    # print(ans)
    #                Select:                #
    cond1 = {'f_type': "Type1", 'f_val': "Value1"}
    cond2 = {'f_type': "Type3", 'f_val': "Value1"}
    conditions = [cond1, cond2]
    ans = tdb.select_result_table(class_names, conditions, engine)
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


def main() -> None:
    # main_entropy()
    # main_basic_database()
    # main_specific_database()
    # main_tree_db_prim()
    # main_tree_db_ftype()
    # main_tree_db_result()
    main_calc_basic()


if __name__ == "__main__":
    main()
