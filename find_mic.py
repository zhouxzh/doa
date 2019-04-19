#!/usr/bin/env python

from scipy.io import wavfile
import numpy as np
from gcc_phat import gcc_phat
from mic_array import MicArray

import signal
import threading

is_quit = threading.Event()
def signal_handler(sig, num):
    is_quit.set()
    print('Quit')

signal.signal(signal.SIGINT, signal_handler)

fs = 16000

from pixels import Pixels, pixels

with MicArray(fs, 4, fs) as mic:
    for chunk in mic.read_chunks():
        direction = mic.get_direction(chunk)
        print(int(direction))
        pixels.wakeup(direction)
        tau = np.zeros((4,4))
        for i in range(4):
            for j in range(4):
                tau[i, j], _ = gcc_phat(chunk[i::4], chunk[j::4], fs=fs)
        if is_quit.is_set():
            break

        print(tau*343*100)
