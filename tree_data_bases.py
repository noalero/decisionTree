import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from typing import Union

import feature
import brange
import feature_type


def __create_database__(self) -> None:
    # ToDo return value
    self.__create_trainingdata_primary_table__()
    self.__create_feature_type_table__()
    self.__create_result_table__()


def __create_trainingdata_primary_table__(self) -> None:
    self.dataframe.to_sql(
        "TrainingDataPrimaryTable", con=self.engine, index=True, index_label='index', if_exists='replace')


def select_from_primary_table(self, columns: list[feature.Feature],
                              wheres: list[tuple[feature.Feature, Union[brange.Range, str]]]) -> sa.Sequence:
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
    wheres_names = ' AND '.join(map(lambda where: f'{where}', where_list))
    select_command = sa.text(f'''SELECT {column_names} FROM "TrainingDataPrimaryTable" WHERE {wheres_names}''')
    with self.engine.connect() as connection:
        result = connection.execute(select_command)
        connection.commit()
        connection.close()
    ans = result.fetchall()
    return ans


def __create_feature_type_table__(self) -> None:
    # ToDo
    feature_type.Base.metadata.create_all(self.engine)


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
