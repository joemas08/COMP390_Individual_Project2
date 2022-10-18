import requests
from util_functions import compare_request_code


def get_request(site_passed):
    """
    Returns GET request of site passed if no error has occurred, otherwise returns error message
    """
    try:
        request_response = requests.get(site_passed)
        return _request_code_handler(request_response)
    except requests.exceptions.InvalidURL:
        return 'The URL that was used had : Invalid URL Error'
    except requests.exceptions.ConnectionError:
        return 'The URL that was used had : Connection Error'
    except requests.exceptions.MissingSchema:
        return 'The URL that was used had : Missing Schema Error'


def _request_code_handler(request_response):
    """
    Function takes valid URL GET request response in as parameter and identifies the HTTP response status code of
    response. If status code is successful, returns the response to a function that accesses the
    content of response. Otherwise, prints out error message describing what error occurred with error code
    """
    request_response_status_code = request_response.status_code

    if compare_request_code(request_response_status_code, 500, 600):
        return f'Your request returned the code {request_response_status_code} which is a Server Error Message'

    elif compare_request_code(request_response_status_code, 400, 500):
        return f'Your request returned the code {request_response_status_code} which is a Client Error Response'

    elif compare_request_code(request_response_status_code, 300, 400):
        return f'Your request returned the code {request_response_status_code} which is a Redirection Message'

    elif compare_request_code(request_response_status_code, 200, 300):
        return _response_content(request_response)

    elif compare_request_code(request_response_status_code, 100, 200):
        return f'Your request returned the code {request_response_status_code} which is an Informational Response Code'
    else:
        return 'There was an error with your request that is not recognized'


def _response_content(response_passed):
    """
        Function returns content of successful GET request response passed in parameter
    """
    return response_passed.content
