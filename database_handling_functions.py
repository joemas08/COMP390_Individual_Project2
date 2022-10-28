"""
This module creates a sqlite3 database with tables for the 7 regions of all fallen meteorites from
NASA data and correctly populates the region tables with meteorites that fell within their bounds.
"""

import sqlite3
from util_functions import value_check


def connect_to_database(db_name: str):
    """ Returns a database connection and database cursor to interact with database passed in parameter if connection
        was successful. If error occurs, prints corresponding error message and description """
    db_connection = None
    db_cursor = None

    try:
        # connect to a sqlite3 database (creates it if it doesn't exist)
        db_connection = sqlite3.connect(db_name)
        # creating cursor object to interact with connected database
        db_cursor = db_connection.cursor()

        print(f'- Database: {db_name} connected\n')

    except sqlite3.Error as db_error:
        print(f'A database error has occurred : \n [{db_error}]')
        exit()

    finally:
        return db_connection, db_cursor


def _create_table(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor, table_name: str):
    """ Creates a table of name passed in parameter to database using connection and cursor passed in parameter """
    try:
        db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
                            name TEXT,
                            mass TEXT,
                            reclat TEXT,
                            reclong TEXT);''')

        # Clearing all data from table from previous runs of program
        db_cursor.execute(f'''DELETE FROM {table_name}''')

        print(f'~ {table_name} table has been created\n')

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
    """ Inserts meteorites from JSON content passed into correct tables of database using the connection and cursor
    passed. If error occurs, returns corresponding error message and closes any database connections before exiting
    program """
    try:
        for meteorite in json_content:
            # Checking number of attributes of current meteorite, if greater than 7 it must have latitude and longitude
            if len(meteorite) > 7:
                # List returned has the region(s) that the current meteorite fell within and will be used to insert
                regions = _find_region(meteorite)
                for region in regions:
                    db_cursor.execute(f'''INSERT INTO {region} VALUES (?,?,?,?)''',
                                      (meteorite.get('name', None),
                                       meteorite.get('mass', None),
                                       meteorite.get('reclat', None),
                                       meteorite.get('reclong', None)))
                    db_connection.commit()
        print('~ Database: meteorite_db.db has been populated with meteorite data\n')
    except sqlite3.Error as db_error:
        print(f'A database error has occurred : {db_error}')
        close_db(db_connection, db_cursor)
        exit()


def _find_region(meteorite):
    """ Finds region(s) for meteorite passed in parameter. Returns list of found region(s) for meteorite """

    # Getting latitude and longitude of meteorite
    meteor_latitude = meteorite['reclat']
    meteor_longitude = meteorite['reclong']

    # List that will be returned with regions that meteorite fell in
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

    # Iterating through regions dict and checking meteorite to see if it fell within the region's bounds.
    # If so, adds region to found_region list
    for region, coordinates in bound_box_dict.items():
        # left, bottom, right, and top bounds of region
        left_bound, bottom_bound, right_bound, top_bound = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
        if bottom_bound <= value_check(meteor_latitude) <= top_bound and left_bound <= value_check(meteor_longitude) <= right_bound:
            found_regions.append(region)
    return found_regions


def close_db(db_connection: sqlite3.Connection, db_cursor: sqlite3.Cursor):
    """ Closes database connection and database cursor passed in parameter if they are open """
    if db_cursor:
        db_connection.close()

    if db_connection:
        db_connection.close()
        print('~ Database: meteorite_db.db has been closed')
