#!/usr/bin/python3

from matrix_lite import led
import time


def show_direction(angle):
    print('The angle is {}'.format(angle))
    direction = int(angle // (360/18))
    image = ['blue']*led.length
    image[direction] = 'red'
    led.set(image)


if __name__ == '__main__':
    led.set('black')
    for angle in range(360):
        show_direction(angle)
        time.sleep(0.05)
    led.set('black')
