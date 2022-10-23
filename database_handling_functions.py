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


def create_table(db_connection, db_cursor, table_name):
    try:
        db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                            name TEXT,
                            mass TEXT,
                            reclat TEXT,
                            reclong TEXT);''')

        db_cursor.execute(f'DELETE FROM {table_name}')

    except sqlite3.Error as db_error:
        return f'A database error has occurred : {db_error}'


def create_all_tables(db_connection, db_cursor):
    create_table(db_connection, db_cursor, 'Africa_MiddleEast_Meteorites')
    create_table(db_connection, db_cursor, 'Europe_Meteorites')
    create_table(db_connection, db_cursor, 'Upper_Asia_Meteorites')
    create_table(db_connection, db_cursor, 'Lower_Asia_Meteorites')
    create_table(db_connection, db_cursor, 'Australia_Meteorites')
    create_table(db_connection, db_cursor, 'North_America_Meteorites')
    create_table(db_connection, db_cursor, 'South_America_Meteorites')

    close_db(db_connection, db_cursor)


def close_db(db_connection, db_cursor):
    if db_cursor:
        db_connection.close()

    if db_connection:
        db_connection.close()
        print('Database has been closed')
