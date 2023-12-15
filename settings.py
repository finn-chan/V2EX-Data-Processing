import json


def Read(path: str) -> dict:
    with open(path, 'r') as config_file:
        data = json.load(config_file)
        return data
