"""
This module handles GET requests and extracting the JSON content from that GET request while dealing with any errors
that could occur.
"""

import requests


def get_request(site_passed):
    """ Returns response object from GET request of site passed if no error has occurred, otherwise returns
        corresponding error message """
    try:
        request_response_obj = requests.get(site_passed)
        print(f'~ The URL {site_passed} had: Successful Connection\n')
        return _request_code_handler(request_response_obj)
    except requests.exceptions.InvalidURL:
        print(f'The URL {site_passed} had: Invalid URL Error')
        exit()
    except requests.exceptions.ConnectionError:
        print(f'The URL {site_passed} had: Connection Error')
        exit()
    except requests.exceptions.MissingSchema:
        print(f'The URL {site_passed} had : Missing Schema Error')
        exit()


def _request_code_handler(request_response_obj: requests.Response):
    """ Returns HTTP request response object passed as parameter if the response code
        is successful, otherwise returns error statement with corresponding error code """
    request_response_status_code = request_response_obj.status_code

    # comparing status code in form: lower <= status code <= higher to see where status code belongs
    if _compare_request_code(request_response_status_code, 500, 600):
        print(f'Your request returned the code {request_response_status_code} : [{request_response_obj.reason}]')
        exit()

    elif _compare_request_code(request_response_status_code, 400, 500):
        print(f'Your request returned the code {request_response_status_code}: [{request_response_obj.reason}]')
        exit()

    elif _compare_request_code(request_response_status_code, 300, 400):
        print(f'Your request returned the code {request_response_status_code}: [{request_response_obj.reason}]')
        exit()

    elif _compare_request_code(request_response_status_code, 200, 300):
        print(f'~ Your request returned the code {request_response_status_code}: [{request_response_obj.reason}]\n')
        return request_response_obj

    elif _compare_request_code(request_response_status_code, 100, 200):
        print(f'Your request returned the code {request_response_status_code} : [{request_response_obj.reason}]')
        exit()
    else:
        return 'There was an error with your request that is not recognized'


def _compare_request_code(status_code_passed: int, lower: int, upper: int):
    """ Returns True if status code passed is within lower and upper bounds passed """
    if lower <= status_code_passed < upper:
        return True


def convert_to_json(response_obj: requests.Response):
    """ Returns JSON content of response object passed in parameter. If error occurs, prints corresponding error message
        with description """
    json_content = None

    try:
        json_content = response_obj.json()
        print('~ Request response\'s JSON content has been extracted\n')

    except requests.exceptions.JSONDecodeError as json_error:
        print(f'An error occurred trying to decode the request into json : \n {json_error}')

    finally:
        return json_content
