import sqlite3


def connect_to_database(db_name):
    """Returns a database connection and database cursor to interact with database passed in parameter"""
    db_connection = None

    try:
        # connect to a sqlite3 database (creates it if it doesn't exist)
        db_connection = sqlite3.connect(db_name)
        # creating cursor object to interact with connected database
        db_cursor = db_connection.cursor()

        return db_connection, db_cursor

    except sqlite3.Error as db_error:
        return f'A database error has occurred : {db_error}'

    finally:
        if db_connection:
            db_connection.close()
            print('Database has been closed')


def create_table(db_connection, db_cursor, table_name):
    try:
        db_cursor.exexute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                            name TEXT,
                            mass TEXT,
                            reclat TEXT
                            reclong TEXT);''')

    except sqlite3.Error as db_error:
        return f'A database error has occurred : {db_error}'
