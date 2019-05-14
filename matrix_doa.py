#!/usr/bin/python3

from matrix_lite import led
import time
import pyaudio


def show_direction(angle):
    print('The angle is {}'.format(angle))
    direction = int(angle // (360/18))
    image = ['blue']*led.length
    image[direction] = 'red'
    led.set(image)

def find_audio_index():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev['name'].encode('utf-8')
        print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])


if __name__ = '__main__':
    find_audio_index()
