import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
import typing as tp
import psycopg2
from psycopg2 import sql

import config
import brange
import dataPath
import feature
import brange as br


def connect_db(database_url: str) -> sa.engine:
    # TODO: delete?
    engine = sa.create_engine(database_url)
    return engine


def __create_databases__(dataframe: pd.DataFrame, database_url: str) -> None:
    # database_url = "postgresql://NoaLeron:tsmOn8tln@localhost:5432/DecisionTree"
    # engine = sa.create_engine(database_url)
    # session = sa.orm.sessionmaker(bind=engine)
    __create_primary_from_dataframe__(dataframe, database_url)
    # __create_feature_type_table__()
    # __create_result_table__()


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


def select_table(columns: list[str], conditions: list[dict[str, str | br.Range]], engine: sa.engine, name: str):
    select_clause = f'''SELECT {', '.join(columns)} FROM "{name}"'''
    condition_clauses: list[str] = []
    if conditions:
        for or_dict in conditions:
            if len(or_dict) > 1:
                str_lst: list[str] = select_is_instance(or_dict)
                or_clause = ' OR '.join(str_lst)
                condition_clauses.append(f"({or_clause})")
            elif len(or_dict) == 1:
                str1 = select_is_instance(or_dict)
                condition_clauses.append(f"{str1[0]}")
        where_clause = " WHERE " + " AND ".join(condition_clauses)
    else:
        where_clause = ""
    full_sql = select_clause + where_clause
    sql_text = sa.text(full_sql)
    with engine.connect() as connection:
        result = connection.execute(sql_text)
        return result.fetchall()


def __create_primary_from_dataframe__(dataframe: pd.DataFrame, database_url: str) -> None:
    # TODO: ["class"] column
    engine = connect_db(database_url)
    dataframe.to_sql(
        "TrainingDataPrimaryTable", con=engine, index=True, index_label='index', if_exists='replace')
    engine.dispose()


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


def __create_feature_type_table__(engine: sa.engine) -> str:
    create_table_query = sa.text("""
                                    CREATE TABLE IF NOT EXISTS "FeatureTypeTable"  (
                                        rule_id SERIAL PRIMARY KEY,
                                        f_type VARCHAR(225) NOT NULL,
                                        f_val VARCHAR(255) NOT NULL,
                                        UNIQUE (f_type, f_val)
                                    )
                                """)
    with engine.connect() as connection:
        try:
            connection.execute(create_table_query)
            connection.commit()
            ret_str = "FeatureTypeTable created successfully."
        except Exception as e:
            ret_str = f"Failed to create table: {e}"
        finally:
            connection.close()
            return ret_str


def __create_feature_type_table_classes__(engine: sa.engine, class_names: list[str]) -> str:
    classes_query = f'''{' BIGINT NOT NULL, '.join(class_names)} BIGINT NOT NULL, '''
    create_table_query = sa.text(f"""
                                    CREATE TABLE IF NOT EXISTS "FeatureTypeTable"  (
                                        rule_id SERIAL PRIMARY KEY,
                                        f_type VARCHAR(225) NOT NULL,
                                        f_val VARCHAR(255) NOT NULL,
                                        {classes_query}
                                        UNIQUE (f_type, f_val)
                                    )
                                """)
    with engine.connect() as connection:
        try:
            connection.execute(create_table_query)
            connection.commit()
            ret_str = "FeatureTypeTable created successfully."
        except Exception as e:
            ret_str = f"Failed to create table: {e}"
        finally:
            connection.close()
            return ret_str


def insert_single_row_feature_type_table(engine: sa.engine, f_type, f_val) -> str:
    insert_query = sa.text("""
                                INSERT INTO "FeatureTypeTable" (f_type, f_val) 
                                VALUES (:f_type, :f_val)
                                ON CONFLICT (f_type, f_val) DO NOTHING
                            """)
    with engine.connect() as connection:
        result = connection.execute(insert_query, {'f_type': f_type, 'f_val': f_val})
        connection.commit()
        if result.rowcount:
            ret_str = "Data inserted successfully."
        else:
            ret_str = "Insertion failed due to duplicate f_type and f_val."
        connection.close()
    return ret_str


def insert_single_row_feature_type_table_classes(engine: sa.engine, f_type: str, f_val: str,
                                                 classes: dict[str, int]) -> str:
    class_names = ', '.join(classes.keys())
    class_vals = ', '.join([f":{key}" for key in classes.keys()])
    insert_query = sa.text(f"""
                                INSERT INTO "FeatureTypeTable" (f_type, f_val, {class_names}) 
                                VALUES (:f_type, :f_val, {class_vals})
                                ON CONFLICT (f_type, f_val) DO NOTHING
                            """)
    param_dict: dict[str, int | str] = {'f_type': f_type, 'f_val': f_val} | classes
    with engine.connect() as connection:
        result = connection.execute(insert_query, param_dict)
        connection.commit()
        if result.rowcount:
            ret_str = "Data inserted successfully."
        else:
            ret_str = "Insertion failed due to duplicate f_type and f_val."
        connection.close()
    return ret_str


def insert_multiple_rows_feature_type_table(engine: sa.engine, rows: list[dict]) -> int:
    if not rows:
        ans = 0
    else:
        insert_query = sa.text("""
                                    INSERT INTO "FeatureTypeTable" (f_type, f_val) 
                                    VALUES (:f_type, :f_val) 
                                    ON CONFLICT (f_type, f_val) DO NOTHING
                                """)
        with engine.connect() as connection:
            with connection.begin():
                try:
                    # Execute all inserts in one go:
                    result = connection.execute(insert_query, rows)
                    connection.commit()
                    ans = result.rowcount
                except Exception as e:
                    print("Something went wrong: ", e)
                    ans = -1
                finally:
                    connection.close()
    return ans


def insert_multiple_rows_feature_type_table_classes(engine: sa.engine, rows: list[dict[str, int | str]]) -> int:
    # make sure that every row has [f_type] and [f_var]
    if rows:
        for index, dct in list(enumerate(rows)):
            if not ('f_type' in dct and 'f_val' in dct):
                rows.pop(index)
    if not rows:
        ans = 0
    else:
        class_names = ', '.join(rows[0].keys())
        class_vals = ', '.join([f":{key}" for key in rows[0].keys()])
        insert_query = sa.text(f"""
                                    INSERT INTO "FeatureTypeTable" ({class_names}) 
                                    VALUES ({class_vals}) 
                                    ON CONFLICT (f_type, f_val) DO NOTHING
                                """)
        with engine.connect() as connection:
            with connection.begin():
                try:
                    # Execute all inserts in one go:
                    result = connection.execute(insert_query, rows)
                    connection.commit()
                    ans = result.rowcount
                except Exception as e:
                    print("Something went wrong: ", e)
                    ans = -1
                finally:
                    connection.close()
    return ans


def __create_result_table__(engine: sa.engine, class_names: list[str]) -> str:
    classes_query = f'''{' BIGINT NOT NULL, '.join(class_names)} BIGINT NOT NULL, '''
    create_table_query = sa.text(f"""
                                    CREATE TABLE IF NOT EXISTS "ResultTable"  (
                                        rule_id INT PRIMARY KEY,
                                        {classes_query}
                                        total BIGINT NOT NULL,
                                        FOREIGN KEY (rule_id) REFERENCES "FeatureTypeTable"(rule_id)
                                    )
                                """)
    with engine.connect() as connection:
        try:
            connection.execute(create_table_query)
            connection.commit()
            ret_str = "ResultTable created successfully."
        except Exception as e:
            ret_str = f"Failed to create table: {e}"
        finally:
            connection.close()
            return ret_str


def calculate_total(classes_amount: list[int]) -> int:
    if classes_amount:
        total_sum = 0
        for cls_amnt in classes_amount:
            total_sum += cls_amnt
    else:
        total_sum = -1
    return total_sum


def calculate_total_lst(rows: list[dict[str, int]]) -> list[int]:
    totals: list[int] = []
    for dct in rows:
        sums: list[int] = []
        for key, val in dct.items():
            if key != 'rule_id':
                sums.append(val)
        total = calculate_total(sums)
        totals.append(total)
    return totals


def insert_result_table(engine: sa.engine, rows: list[dict[str, int]]) -> int:
    # [rows]: [rule_id], [class_a], [calss_b], ...
    if not rows:
        ans = 0
    else:
        # Calculate total amount:
        totals: list[int] = calculate_total_lst(rows)
        # Add [totals] to dictionaries:
        i = 0
        for dct in rows:
            dct['total'] = totals[i]
            i += 1
        column_names = ', '.join(rows[0].keys())
        column_vals = ', '.join([f":{key}" for key in rows[0].keys()])
        insert_query = sa.text(f"""
                                    INSERT INTO "ResultTable" ({column_names}) 
                                    VALUES ({column_vals})
                                """)
        with engine.connect() as connection:
            with connection.begin():
                try:
                    # Execute all inserts in one go:
                    result = connection.execute(insert_query, rows)
                    connection.commit()
                    ans = result.rowcount
                except Exception as e:
                    print("Something went wrong: ", e)
                    ans = -1
                finally:
                    connection.close()
    return ans


def select_result_table(class_names: list[str], conditions: list[dict[str, str]], engine: sa.engine):
    select_clause = f'''SELECT r.{', r.'.join(class_names)} FROM "FeatureTypeTable" ft
                        JOIN "ResultTable" r ON ft.rule_id = r.rule_id'''
    condition_clauses: list[str] = []
    where_clause = ""
    if conditions:
        for index, dct in list(enumerate(conditions)):
            if not ('f_type' in dct and 'f_val' in dct):
                # remove invalid dictionaries:
                conditions.pop(index)
            else:
                and_clause = f"""ft.f_type = '{dct['f_type']}' AND ft.f_val = '{dct['f_val']}'"""
                condition_clauses.append(and_clause)
        if condition_clauses:
            where_clause = " WHERE " + " OR ".join(condition_clauses)
    full_sql = select_clause + where_clause
    sql_text = sa.text(full_sql)
    with engine.connect() as connection:
        result = connection.execute(sql_text)
        return result.fetchall()


def get_path_classes_amounts(dt_path: dataPath.DataPath, classes: list[str], engine: sa.engine) -> list[int]:
    # TODO: test + class column name
    # Create conditions list:
    path_conditions = []
    for fb in dt_path.get_path():
        cond = {fb[0].get_name(): fb[1]}
        path_conditions.append(cond)
    result: list[int] = []
    for cls in classes:
        class_condition: dict[str, str | brange.Range] = {"class": cls}
        class_column = select_table(["class"], path_conditions+[class_condition], engine, "TrainingDataPrimaryTable")
        if class_column:
            cls_sum = len(class_column)
            result.append(cls_sum)
    return result


