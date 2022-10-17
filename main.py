from handle_request_functions import get_request


def main():
    request = get_request("https://data.nasa.gov/resource/gh4g-9sfh.json")
    print(request)


if __name__ == '__main__':
    main()
