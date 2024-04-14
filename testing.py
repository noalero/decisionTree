import numpy as np
import psycopg2
import pandas as pd
import sqlite3


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
def create_table_from_dataframe(conn) -> None:
    df = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ["Apple", "Banana", "Cherry", "Orange"],
        'amount': [3, 10, 5, 7]
    })
    table_name = 'fruits'
    print("before to_sql")
    df.to_sql(table_name, con=conn, if_exists='append')
    print("after to_sql")


def insert_into_table(conn, crsr, table_name, values) -> None:
    insert_command = f'''INSERT INTO "{table_name}" VALUES ({values[0]}, "{values[1]}", {values[2]}'''
    crsr.execute(insert_command)
    conn.commit()


def select_from_table(conn, crsr, table_name, columns, wheres) -> list:
    column_names = ', '.join(map(lambda x: f'"{x}"', columns))
    wheres_names = 'AND '.join(map(lambda col, val: f'"{col}" = {val}'))
    select_command = f'''SELECT {column_names} FROM "{table_name}" WHERE {wheres_names}'''
    crsr.execute(select_command)
    conn.commit()
    return crsr.fetchall()


def main_database() -> None:
    conn = psycopg2.connect(dbname="Testing",
                     user="NoaLeron",
                     password="tsmOn8tln",
                     host="localhost")
    print("after connection")
    crsr = conn.cursor()
    print("after cursor")
    create_table_from_dataframe(conn)
    print("after creation")
    insert_into_table(conn, crsr, 'fruits', [5, 'Grape', 1])
    print("after insertion")
    select_from_table(conn, crsr, 'fruits', ['name', 'amount'], [('id', 3), ('id', 5)])
    print("after selection")
    conn.close()
    print("after closing")



def main() -> None:
    # main_entropy()
    main_database()


if __name__ == "__main__":
    main()
