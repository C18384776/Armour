import sqlite3
from sqlite3 import Error


def make_connection(database_save_path):
    """
    Attempts to create a SQLite3 database file.

    :param database_save_path:
    Directory path where SQLite3 database file will be saved.

    :return:
    SQLite3 connection from the given path.
    """
    con = None
    try:
        con = sqlite3.connect(database_save_path)
    except Error as e:
        print(e)

    return con


def database_query(connection, query):
    """
    Attempts to perform an SQLite3 query.

    :param connection:
    SQLite3 connection to a database.

    :param query:
    User given query to be performed to a given SQLite3 database.
    """
    try:
        cur = connection.cursor()
        cur.execute(query)
    except Error as e:
        print(e)
