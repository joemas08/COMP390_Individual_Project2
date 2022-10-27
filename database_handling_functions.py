import sqlite3
from util_functions import value_check


def connect_to_database(db_name: str):
    """Returns a database connection and database cursor to interact with database passed in parameter if connection
    was successful. If error occurs, prints corresponding error message and description """
    db_connection = None
    db_cursor = None

    try:
        # connect to a sqlite3 database (creates it if it doesn't exist)
        db_connection = sqlite3.connect(db_name)
        # creating cursor object to interact with connected database
        db_cursor = db_connection.cursor()

    except sqlite3.Error as db_error:
        print(f'A database error has occurred : \n [{db_error}]')
        exit()

    finally:
        return db_connection, db_cursor


def _create_table(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, table_name: str):
    """ Creates a table of name passed to database using connection & cursor passed """
    try:
        db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                            name TEXT,
                            mass TEXT,
                            reclat TEXT,
                            reclong TEXT);''')

        # Clearing all data from table
        db_cursor.execute(f'''DELETE FROM {table_name}''')

    except sqlite3.Error as db_error:
        print(f'A database error has occurred : {db_error}')
        close_db(db_connection, db_cursor)
        exit()


def create_all_region_tables(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor):
    """ Creates seven tables for each region of meteor data into database using db_connection and db_cursor passed """
    _create_table(db_connection, db_cursor, 'Africa_MiddleEast_Meteorites')
    _create_table(db_connection, db_cursor, 'Europe_Meteorites')
    _create_table(db_connection, db_cursor, 'Upper_Asia_Meteorites')
    _create_table(db_connection, db_cursor, 'Lower_Asia_Meteorites')
    _create_table(db_connection, db_cursor, 'Australia_Meteorites')
    _create_table(db_connection, db_cursor, 'North_America_Meteorites')
    _create_table(db_connection, db_cursor, 'South_America_Meteorites')


def insert_into_region_tables(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, json_content):
    """
    Inserts meteorites from JSON content passed into correct tables of database using connection and cursor passed
    """
    try:
        for meteorite in json_content:
            if len(meteorite) > 7:
                regions = _find_region(meteorite)
                for region in regions:
                    db_cursor.execute(f'''INSERT INTO {region} VALUES (?,?,?,?)''',
                                      (meteorite.get('name', None),
                                       meteorite.get('mass', None),
                                       meteorite.get('reclat', None),
                                       meteorite.get('reclong', None)))
                    db_connection.commit()

    except sqlite3.Error as db_error:
        print(f'A database error has occurred : {db_error}')
        close_db(db_connection, db_cursor)
        exit()


def _find_region(meteorite):
    """Finds region of meteorite passed in parameter, Returns list of found regions for meteorite"""
    latitude = meteorite['reclat']
    longitude = meteorite['reclong']
    found_regions = []

    # geolocation bounding box -- (left,bottom,right,top)
    bound_box_dict = {
        'Africa_MiddleEast_Meteorites': (-17.8, -35.2, 62.2, 37.6),
        'Europe_Meteorites': (-24.1, 36, 32, 71.1),
        'Upper_Asia_Meteorites': (32.2, 35.8, 190.4, 72.7),
        'Lower_Asia_Meteorites': (58.2, -9.9, 154, 38.6),
        'Australia_Meteorites': (112.9, -43.8, 154.3, -11.1),
        'North_America_Meteorites': (-168.2, 12.8, -52, 71.5),
        'South_America_Meteorites': (-81.2, -55.8, -34.4, 12.6)
    }

    for region, coordinates in bound_box_dict.items():
        if coordinates[1] <= value_check(latitude) <= coordinates[3] and coordinates[0] <= value_check(longitude) <= \
                coordinates[2]:
            found_regions.append(region)
    return found_regions


def close_db(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor):
    """Closes database connection and database cursor passed in parameter if they are open"""
    if db_cursor:
        db_connection.close()

    if db_connection:
        db_connection.close()
        print('Database has been closed')
