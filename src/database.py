import config
import sqlite3
import sys

from sqlite3 import Error


def create_connection():
    """ Create a database connection to a SQLite database """
    db_file = f'{config.common()}/hotshotpy.db'

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


def create_tables(conn):
    sql = """CREATE TABLE IF NOT EXISTS params(
        current_event_id integer
    );"""

    execute_sql(conn, sql)

    sql = """CREATE TABLE IF NOT EXISTS events(
        id integer PRIMARY KEY,
        name text NOT NULL
    );"""

    execute_sql(conn, sql)

    sql = """CREATE TABLE IF NOT EXISTS drivers(
        id integer PRIMARY KEY,
        name text NOT NULL
    );"""

    execute_sql(conn, sql)
