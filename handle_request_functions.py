import requests
from util_functions import compare_request_code


def get_request(site_passed):
    try:
        request_response = requests.get(site_passed)
        return request_code_handler(request_response)
    except requests.exceptions.InvalidURL:
        return 'The URL that was used is not valid'


def request_code_handler(request_response):
    request_response_status_code = request_response.status_code

    if compare_request_code(request_response_status_code, 500, 600):
        return print(f'Your request returned the code {request_response_status_code} which is a Server Error Message')

    elif compare_request_code(request_response_status_code, 400, 500):
        return print(f'Your request returned the code {request_response_status_code} which is a Client Error Response')

    elif compare_request_code(request_response_status_code, 300, 400):
        return print(f'Your request returned the code {request_response_status_code} which is a Redirection Message')

    elif compare_request_code(request_response_status_code, 200, 300):
        return handle_request(request_response)

    elif compare_request_code(request_response_status_code, 100, 200):
        return print(f'Your request returned the code {request_response_status_code} which is an Informational '
                     f'Response Code')
    else:
        return 'There was an error with your request that is not recognized'


def handle_request(request_response):
    return request_response.content
