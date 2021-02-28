import hotshotpy
import sqlite3
import sys

from sqlite3 import Error


def create_connection():
    """ Create a database connection to a SQLite database """
    db_file = hotshotpy.config.db_file()

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    if conn is None:
        print(f"Error, cannot connect to dabase {db_file}")
        sys.exit(1)

    return conn


def execute_sql(conn, sql):
    """
    Execute the given SQL query
    :param conn: Connection object
    :param sql: a SQL statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)
