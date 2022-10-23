def compare_request_code(status_code_passed, lower, upper):
    """Returns True if status code passed is within lower and upper bounds passed"""
    if lower <= status_code_passed < upper:
        return True
