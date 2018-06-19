import json
import os.path


def check(file):
    return os.path.exists(file)


def create(filename):
    file = open(filename, "a+")
    file.write('{\"room\":\"test\"}')
    file.close()


def create_(filename, data):
    file = open(filename, "a+")
    file.write(data)
    file.close()


def write(data, filename):
    with open(filename, 'w+') as file:
        json.dump(data, file)
    file.close()


def read(filename):
    with open(filename, 'r+') as file:
        data = json.load(file)
        file.close()
        return data
