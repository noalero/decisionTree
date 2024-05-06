import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
import typing as tp
import psycopg2
from psycopg2 import sql

import feature
import brange as br
import feature_type


def connect_db(database_url: str) -> sa.engine:
    engine = sa.create_engine(database_url)
    return engine


def __create_databases__(dataframe: pd.DataFrame, database_url: str) -> None:
    # database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
    # engine = sa.create_engine(database_url)
    # session = sa.orm.sessionmaker(bind=engine)
    __create_primary_from_dataframe__(dataframe, database_url)
    # __create_feature_type_table__()
    # __create_result_table__()


def __create_primary_from_dataframe__(dataframe: pd.DataFrame, database_url: str) -> None:
    engine = connect_db(database_url)
    dataframe.to_sql(
        "TrainingDataPrimaryTable", con=engine, index=True, index_label='index', if_exists='replace')
    engine.dispose()


def simple_select_from_primary_table(columns: list[str],
                              conditions: tp.Dict[str, str], engine: sa.engine):
    select_clause = f'''SELECT {', '.join(columns)} FROM "TrainingDataPrimaryTable"'''
    if conditions:
        condition_clause = [f"{col} = :{col}" for col in conditions]
        where_clause = " WHERE " + " AND ".join(condition_clause)
    else:
        where_clause = ""
    full_sql = select_clause + where_clause
    sql_text = sa.text(full_sql)
    for param, value in conditions.items():
        sql_text = sql_text.bindparams(sa.sql.bindparam(param, value=value))
    with engine.connect() as connection:
        result = connection.execute(sql_text)
        return result.fetchall()


# ToDo: check, where or + where and


def types_select_from_primary_table(columns: list[str],
                                    conditions: dict[str, str | br.Range], engine: sa.engine):
    select_clause = f'''SELECT {', '.join(columns)} FROM "TrainingDataPrimaryTable"'''
    if conditions:
        condition_clauses: list[str] = []  # [f"{col} = :{col}" for col in conditions]
        for col in conditions.items():
            if isinstance(col[1], br.Range):
                con1 = f"{col[0]} >= {col[1].get_from_index()}"
                condition_clauses.append(con1)
                con2 = f"{col[0]} < {col[1].get_to_index()}"
                condition_clauses.append(con2)
            elif isinstance(col[1], str):
                con = f"{col[0]} = '{col[1]}'"
                condition_clauses.append(con)
        where_clause = " WHERE " + " AND ".join(condition_clauses)
    else:
        where_clause = ""
    full_sql = select_clause + where_clause
    sql_text = sa.text(full_sql)
    with engine.connect() as connection:
        result = connection.execute(sql_text)
        return result.fetchall()


def select_is_instance(conditions: dict[str, str | br.Range]) -> list[str]:
    condition_clauses: list[str] = []
    for col in conditions.items():
        if isinstance(col[1], br.Range):
            con1 = f"{col[0]} >= {col[1].get_from_index()}"
            con2 = f"{col[0]} < {col[1].get_to_index()}"
            condition_clauses.append(f"({con1} AND {con2})")
        elif isinstance(col[1], str):
            con = f"{col[0]} = '{col[1]}'"
            condition_clauses.append(con)
    return condition_clauses


def or_select_from_primary_table(columns: list[str],
                                 conditions: list[dict[str, str | br.Range]], engine: sa.engine):
    select_clause = f'''SELECT {', '.join(columns)} FROM "TrainingDataPrimaryTable"'''
    condition_clauses: list[str] = []
    # TODO: Add and option for range
    if conditions:
        for or_dict in conditions:
            if len(or_dict) > 1:
                str_lst: list[str] = select_is_instance(or_dict)
                or_clause = ' OR '.join(str_lst)
                condition_clauses.append(f"({or_clause})")
            elif len(or_dict) == 1:
                str1 = select_is_instance(or_dict)
                condition_clauses.append(f"{str1[0]}")
            else:
                o = 0
        where_clause = " WHERE " + " AND ".join(condition_clauses)
    else:
        where_clause = ""
    full_sql = select_clause + where_clause
    sql_text = sa.text(full_sql)
    with engine.connect() as connection:
        result = connection.execute(sql_text)
        return result.fetchall()


def __create_feature_type_table__(engine: sa.engine) -> None:
    # ToDo
    feature_type.Base.metadata.create_all(engine)


def insert_feature_type_table(self, featype: list[int], featype_val: list[int]) -> None:
    session = self.session()
    try:
        new_row = feature_type.FeatureTypeObject(feature_type=featype, feature_type_value=featype_val)
        session.add(new_row)
        session.commit()
    except sa.exc.IntegrityError as e:
        if 'already exists' in str(e):
            print(
                f"An entry with the same combination of feature_type and feature_type_value already exists: {featype}, {featype_val}")
        else:
            print(f"A database integrity error occurred: {str(e)}")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        session.rollback()
    finally:
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
