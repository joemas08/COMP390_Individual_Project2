import requests
from util_functions import compare_request_code


def get_request(site_passed):
    """
    Returns response object from GET request of site passed if no error has occurred, otherwise returns corresponding
    error message
    """
    try:
        request_response_obj = requests.get(site_passed)
        print('- The URL that was used had a successful connection')
        return _request_code_handler(request_response_obj)
    except requests.exceptions.InvalidURL:
        print('The URL that was used had : Invalid URL Error')
        exit()
    except requests.exceptions.ConnectionError:
        print('The URL that was used had : Connection Error')
        exit()
    except requests.exceptions.MissingSchema:
        print('The URL that was used had : Missing Schema Error')
        exit()


def _request_code_handler(request_response_obj):
    """
    Returns HTTP request response object passed as parameter if the response code
    is successful, otherwise returns error statement with corresponding error code
    """
    request_response_status_code = request_response_obj.status_code

    if compare_request_code(request_response_status_code, 500, 600):
        print(f'Your request returned the code {request_response_status_code} : [{request_response_obj.reason}]')
        exit()

    elif compare_request_code(request_response_status_code, 400, 500):
        print(f'Your request returned the code {request_response_status_code}: [{request_response_obj.reason}]')
        exit()

    elif compare_request_code(request_response_status_code, 300, 400):
        print(f'Your request returned the code {request_response_status_code}: [{request_response_obj.reason}]')
        exit()

    elif compare_request_code(request_response_status_code, 200, 300):
        return request_response_obj

    elif compare_request_code(request_response_status_code, 100, 200):
        print(f'Your request returned the code {request_response_status_code} : [{request_response_obj.reason}]')
        exit()
    else:
        return 'There was an error with your request that is not recognized'


def convert_to_json(response_obj: requests.Response):
    """
    Returns JSON content of response object passed in parameter. If error occurs, prints corresponding error message
    with description
    """
    json_content = None

    try:
        json_content = response_obj.json()

    except requests.exceptions.JSONDecodeError as json_error:
        print(f'An error occurred trying to decode the request into json : \n {json_error}')

    finally:
        return json_content
