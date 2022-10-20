from handle_request_functions import *
from database_handling_functions import *


def main():
    nasa_api_url = 'https://data.nasa.gov/resource/gh4g-9sfh.json'
    database = 'meteorite_db.db'

    # Acquiring response of GET request
    request_response = get_request(nasa_api_url)

    # Decoding response into JSON format
    json_content = request_response.json()

    connect_to_database(database)


if __name__ == '__main__':
    main()
