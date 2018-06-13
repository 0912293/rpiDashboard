import json
import os.path


def check(file):
    return os.path.exists(file)

def create(filename):
    print('1')
    file = open(filename, "a+")
    print('2')
    file.write('{\"room\":\"test\"}')
    print('3')
    file.close()


def write(data, filename):
    with open(filename, 'w+') as file:
        json.dump(data, file)
        print('file created')


def read(filename):
    with open(filename, 'r+') as file:
        data = json.load(file)
        return data

