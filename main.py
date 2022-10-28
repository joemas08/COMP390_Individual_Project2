"""This main module uses the URL and Database with it's imported functions to create a sqlite3 database and populate
that database with content from the URL. Notifies user of each step as it happens.
"""

from handle_request_functions import *
from database_handling_functions import *


def main():
    """This main function uses the hard coded url to send a GET request and then populate hard coded database with
        JSON data from GET request """

    # The target URL for GET request
    nasa_url = 'https://data.nasa.gov/resource/gh4g-9sfh.json'

    # Database to be populated
    database = 'meteorite_db.db'

    # Acquiring response of GET request
    request_response_obj = get_request(nasa_url)

    # Decoding response into JSON format
    json_content = convert_to_json(request_response_obj)

    # Getting a connection and cursor object to interact with database
    db_connection, db_cursor = connect_to_database(database)

    # Creating tables for all seven regions
    create_all_region_tables(db_connection, db_cursor)

    # Sorting meteorites into correct region table
    insert_into_region_tables(db_connection, db_cursor, json_content)

    # Closing the database
    close_db(db_connection, db_cursor)


if __name__ == '__main__':
    main()
