#!/usr/bin/env python

from scipy.io import wavfile
import numpy as np
from gcc_phat import gcc_phat

fs, data = wavfile.read('song.wav')
print(data.shape)
tau = np.zeros((4,4))
for i in range(4):
    for j in range(4):
        tau[i, j], _ = gcc_phat(data[:,i], data[:,j], fs=fs)
        print(tau[i,j])

print(tau)
