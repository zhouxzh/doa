#!/usr/bin/env python

import numpy as np
import pyroomacoustics as pra
from pyroomacoustics.doa import circ_dist
from mic_array import MicArray
import signal
import time
from pixels import Pixels, pixels
import threading
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
MIC_DISTANCE_4 = 0.08127


#R = pra.circular_2D_array([0,0], 4, 0, MIC_RADIUS)
#R = np.array([[-1, 0, 1, 0], [0, 1, 0, -1]]) * MIC_DISTANCE_4/2
R = np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]) * MIC_DISTANCE_4 / 2 / 2**0.5
print(R)


is_quit = threading.Event()

def signal_handler(sig, num):
    is_quit.set()
    print('Quit')

signal.signal(signal.SIGINT, signal_handler)

c = 343
fs = 16000
nfft = 512


#Possible dos algorithms: SRP, MUSIC, TOPS, CSSM, WAVES
doa = pra.doa.algorithms['SRP'](R, fs, nfft, c=c)



plt.figure()
with MicArray(fs, 4, fs/4) as mic:
    start = time.time()
    for chunk in mic.read_chunks():
        #print(chunk.shape)
        #pixels.wakeup(np.random.randint(0, 360, 1))

        X = np.array([pra.stft(chunk[i::4], nfft, nfft//2, transform=np.fft.rfft).T for i in range(4)])
        doa.locate_sources(X, freq_range=[500, 3000])
        direction = doa.azimuth_recon / np.pi * 180
        print('Time: ', time.time()-start, ' Recovered azimuth: ', direction)
        pixels.wakeup(direction)
        #plt.close()
        #doa.polar_plt_dirac()
        #plt.draw()
        #plt.pause(0.0001)

        if is_quit.is_set():
            break

