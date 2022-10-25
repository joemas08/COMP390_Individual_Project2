from handle_request_functions import *
from database_handling_functions import *
from util_functions import *


def main():
    nasa_url = 'https://data.nasa.gov/resource/gh4g-9sfh.json'
    database = 'meteorite_db.db'

    # Acquiring response of GET request
    request_response_obj = get_request(nasa_url)

    # Decoding response into JSON format
    json_content = convert_to_json(request_response_obj)

    # total = 0
    #
    # for meteorite in json_content:
    #     if len(meteorite) > 7:
    #         name = meteorite['name']
    #         lat = meteorite['reclat']
    #         long = meteorite['reclong']
    #         if -35.2 <= value_check(lat) <= 37.6 and -17.8 <= value_check(long) <= 62.2:
    #             print(f'Name: {name}\nReclat: {lat}\nReclong: {long}\n')
    #             total += 1
    #         print('-'*40)
    # print(total)

    db_connection, db_cursor = connect_to_database(database)

    create_all_tables(db_connection, db_cursor)


if __name__ == '__main__':
    main()

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
