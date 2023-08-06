"""Main module."""

# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# https://github.com/audreyfeldroy/cookiecutter-pypackage

# LOAD PACKAGES
import pandas as pd
import sqlite3


def data_check(dfs, df_names):
    # dfs list must have a list of dfs
    list_check = [isinstance(df, pd.DataFrame) for df in dfs]
    if not all(list_check):
        raise Exception('dfs must be set equal to a list of pandas dataframes')

    # df_names names be a list of strings
    list_check = [isinstance(df, str) for df in df_names]
    if not all(list_check):
        raise Exception('df_names must be set equal to a list of strings')

    # df_names names be unique
    if not len(set(df_names)) == len(df_names):
        raise Exception('df_names must contain unique values')

    # check if dfs and df_names are same length
    if not len(dfs) == len(df_names):
        raise Exception('length of df_names and dfs must be equal')


def pandas_query(dfs: list, df_names: list, sql: str):
    data_check(dfs, df_names)

    conn = sqlite3.connect(":memory:")

    for tup in tuple(zip(dfs, df_names)):
        temp_df = tup[0]
        temp_df.to_sql(f'{tup[1]}', conn, index=False)  # load dfs to memory

    df = pd.read_sql_query(sql, conn)
    conn.close()

    return df