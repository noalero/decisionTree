import numpy as np
import psycopg2
import pandas as pd
import sqlite3
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
import feature_type
from feature_type import Base


class TestingC(object):

    def __init__(self, url) -> None:
        self.engine = sa.create_engine(url)
        self.session = sa.orm.sessionmaker(bind=self.engine)

    def create_feature_type_table(self) -> None:
        Base.metadata.create_all(self.engine)

    def insert_feature_type_table(self, featype, featype_val) -> None:
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
