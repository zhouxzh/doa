#!/usr/bin/python3

from matrix_lite import led
import time
import wave
import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
import queue
import sounddevice as sd

# algorithms parameters
c = 343.    # speed of sound
fs = 16000  # sampling frequency
CHANNELS = 8
RECORD_SECONDS = 3
FRAMES = 16

#Position [x,y] of each mic in the array (mm)
#Mic	X	Y
#M1	00.00	0.00
#M2	-38.13	3.58
#M3	-20.98	32.04
#M4	11.97	36.38
#M5	35.91	13.32
#M6	32.81	-19.77
#M7	5.00	-37.97
#M8	-26.57	-27.58
R = [[0, -38.13, -20.98, 11.97, 35.91, 32.81, 5.00, -26.57],
     [0, 3.58, 32.04, 36.38, 13.32, -19.77, -37.97, -27.58]]
R = np.array(R)
R[0] = -R[0]
R = R/1000
print(R)


q = queue.Queue(FRAMES)

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    if q.full():
        q.get()
    else:
        q.put(indata)

def show_direction(angle):
    #print('The angle is {}'.format(angle))
    direction = int(angle // (360/18))
    image = ['blue']*led.length
    image[direction] = 'red'
    led.set(image)
    
def led_off():
    print('shut down the LED')
    led.set('black')



def update_singal():
    global source_signal
    while not q.empty():
        data = q.get_nowait()
        shift = len(data)
        source_signal = np.roll(source_signal, -shift, axis=0)
        source_signal[-shift:, :] = data

def matrix_doa():
    global source_signal
    #print(source_signal)
    #algo_names = ['SRP', 'MUSIC', 'TOPS', 'CSSM', 'WAVES']
    algo_name = 'SRP'
    #print('The algorithms {} will be used.'.format(algo_name))
    nfft = 256  # FFT size
    ################################
    # Compute the STFT frames needed
    X = np.array([ 
        pra.stft(source_signal[:,i], nfft, nfft // 2, transform=np.fft.rfft).T 
        for i in range(CHANNELS) ])

    ##############################################
    # Construct the new DOA object
    # the max_four parameter is necessary for FRIDA only
    doa = pra.doa.algorithms[algo_name](R, fs, nfft, c=c)

    # this call here perform localization on the frames in X
    doa.locate_sources(X, freq_range=[1000, 3000])

    # doa.azimuth_recon contains the reconstructed location of the source
    angle = doa.azimuth_recon / np.pi * 180
    print('  Recovered azimuth:', angle, 'degrees')
    return(angle)



#######################


try:
    source_signal = np.random.random((256*FRAMES, CHANNELS))
    stream = sd.InputStream(
            device=3,
            channels=8,
            samplerate=fs,
            callback=audio_callback)
    with stream:
        print('DOA starting')
        for i in range(int(100)):
            update_singal()
            angle = matrix_doa()
            print(angle)
            show_direction(angle)
        led_off()
except KeyboardInterrupt:
    led_off()
    print('DOA finished')
    exit(0)

    



