def compare_request_code(status_code_passed, lower, upper):
    """Returns True if status code passed is within lower and upper bounds passed"""
    if lower <= status_code_passed < upper:
        return True


def _check_int(string_passed):
    """Returns True if string passed is an integer, otherwise returns False"""
    try:
        int(string_passed)
        return True

    except ValueError:
        return False


def _check_float(string_passed: str):
    """Returns True if string passed is a float, otherwise returns False"""
    try:
        float(string_passed)
        return True
    except ValueError:
        return False


def value_check(value_passed: str):
    """Returns integer if value passed was an integer, float if value passed was a float, otherwise returns 0"""
    if _check_int(value_passed):
        return int(value_passed)

    elif _check_float(value_passed):
        return float(value_passed)

    else:
        return 0
