import json
import os.path

filename = "C:/Users/kevin/PycharmProjects/Raspberry pi/setup.json"  # uncomment for testing
# filename = "/home/pi/RaspberryPi/setup.json"   #uncomment for rpi


def check(file):
    return os.path.exists(file)


def create():
    print('1')
    file = open(filename,"a+")
    print('2')
    file.write('{\"room\":\"test\"}')
    print('3')
    file.close()


def write(room):
    data = {'room': str(room)}
    with open(filename, 'w+') as file:
        json.dump(data, file)
        print('file created')


def read():
    with open(filename,'r+') as file:
        data = json.load(file)
        return data['room']
