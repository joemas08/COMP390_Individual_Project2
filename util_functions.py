def compare_request_code(status_code_passed, lower, upper):
    if lower <= status_code_passed < upper:
        return True
