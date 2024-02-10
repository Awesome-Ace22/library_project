import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_db():
    database = r"/Users/ameliaellis/PycharmProjects/library_project/users.db"

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS user (
                                        user_id integer PRIMARY KEY,
                                        username text,
                                        password text,
                                    ); """
    sql_create_libraries_table = """CREATE TABLE IF NOT EXISTS library (
                                        library_id integer PRIMARY KEY,
                                        user_id integer NOT NULL,
                                        library_name text,
                                        FOREIGN KEY (user_id) REFERENCES user (user_id)
                                    ); """

    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS book (
                                        book_id integer PRIMARY KEY,
                                        library_id integer,
                                        isbn text,
                                        title text,
                                        authors text
                                        publisher text NOT NULL,
                                        publishedDate text NOT NULL,
                                        description text NOT NULL,
                                        pageCount integer,
                                        thumbnail text NOT NULL,
                                        FOREIGN KEY (library_id) REFERENCES library (library_id)
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_libraries_table)
        create_table(conn, sql_create_books_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    create_db()