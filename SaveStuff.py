import json
import os.path


def check(file):
    return os.path.exists(file)


def create(filename):
    file = open(filename, "a+")
    file.write('{\"room\":\"test\"}')
    file.close()


def write(data, filename):
    with open(filename, 'w+') as file:
        json.dump(data, file)


def read(filename):
    with open(filename, 'r+') as file:
        data = json.load(file)
        return data

