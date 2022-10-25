import sqlite3
from util_functions import value_check


def connect_to_database(db_name: str):
    """Returns a database connection and database cursor to interact with database passed in parameter if connection
    was successful """
    db_connection = None
    db_cursor = None

    try:
        # connect to a sqlite3 database (creates it if it doesn't exist)
        db_connection = sqlite3.connect(db_name)
        # creating cursor object to interact with connected database
        db_cursor = db_connection.cursor()

    except sqlite3.Error as db_error:
        return f'A database error has occurred : \n [{db_error}]'

    finally:
        return db_connection, db_cursor


def create_table(db_connection, db_cursor, table_name):
    try:
        db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                            name TEXT,
                            mass TEXT,
                            reclat TEXT,
                            reclong TEXT);''')

        db_cursor.execute(f'''DELETE FROM {table_name}''')

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


def insert_into_region(db_connection, db_cursor, json_content):
    try:
        for meteorite in json_content:
            if len(meteorite) > 7:
                regions = find_region(meteorite)
                for region in regions:
                    db_cursor.execute(f'''INSERT INTO {region} VALUES (?,?,?,?)''',
                                      (meteorite.get('name', None),
                                       meteorite.get('mass', None),
                                       meteorite.get('reclat', None),
                                       meteorite.get('reclong', None)))
                    db_connection.commit()

    except sqlite3.Error as db_error:
        return f'A database error has occurred : {db_error}'


def find_region(meteorite):
    latitude = meteorite['reclat']
    longitude = meteorite['reclong']
    regions = []
    if -35.2 <= value_check(latitude) <= 37.6 and -17.8 <= value_check(longitude) <= 62.2:
        regions.append('Africa_MiddleEast_Meteorites')
    if 36 <= value_check(latitude) <= 71.1 and -24.1 <= value_check(longitude) <= 32:
        regions.append('Europe_Meteorites')
    if 35.8 <= value_check(latitude) <= 72.7 and 32.2 <= value_check(longitude) <= 190.4:
        regions.append('Upper_Asia_Meteorites')
    if -9.9 <= value_check(latitude) <= 38.6 and 58.2 <= value_check(longitude) <= 154:
        regions.append('Lower_Asia_Meteorites')
    if -43.8 <= value_check(latitude) <= -11.1 and 112.9 <= value_check(longitude) <= 154.3:
        regions.append('Australia_Meteorites')
    if 12.8 <= value_check(latitude) <= 71.5 and -168.2 <= value_check(longitude) <= -52:
        regions.append('North_America_Meteorites')
    if -55.8 <= value_check(latitude) <= 12.6 and -81.2 <= value_check(longitude) <= -34.4:
        regions.append('South_America_Meteorites')
    return regions


def close_db(db_connection, db_cursor):
    if db_cursor:
        db_connection.close()

    if db_connection:
        db_connection.close()
        print('Database has been closed')
