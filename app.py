import json
from search import SearchHelper


def read_settings():
    with open('settings.json') as data:
        settings = json.load(data)

    return settings


if __name__ == "__main__":
    settings = read_settings()
    SearchHelper = SearchHelper(settings)
