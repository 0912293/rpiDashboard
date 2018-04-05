import json
import os.path

filename = "C:/Users/kevin/PycharmProjects/Raspberry pi/setup.json"  # uncomment for testing
# filename = "/home/pi/RaspberryPi/setup.json"   #uncomment for rpi


def check():
    return os.path.exists(filename)


def create():
    print('1')
    file = open(filename,"a+")
    print('2')
    file.write('test')
    print('3')
    file.close()


def write(room):
    data = {'room': str(room)}
    with open(filename, 'w+') as file:
        json.dump(data, file)
        print('file created')


def read():
    with open(filename,'r+') as file:
        data = json.loads(file.decode('utf-8'))
        return data['room']
