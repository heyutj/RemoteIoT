# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import numpy as np
import wave
import threading
import time


class InAudio(object):
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.NUM_SAMPLES = 2000
        self.SAMPLING_RATE = 8000
        p = PyAudio()
        self.stream = p.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE,
                             input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.buffer=[]
    def start(self):
        self.t = threading.Thread(target=self.record_frame)
        self.t.start()
    def record_frame(self):
        while True:
            self.buffer.append(self.stream.read(self.NUM_SAMPLES))
    def stop(self):
        self.t.stop()
        self.buffer=[]
    def get_frame(self):
        if self.buffer==[]:
            return None
        else:
            return self.buffer.pop(0)


class OutAudio(object):
    def __init__(self):
        self.SAMPLING_RATE = 8000
        self.p = PyAudio()
        self.stream = self.p.open(
            format=paInt16, channels=1, rate=self.SAMPLING_RATE, output=True)
        self.clean_buffer

    def clean_buffer(self):
        self.buffer = []

    def save_buffer(self, data):
        self.buffer.append(data)

    def save_wave_file(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        for tmp in self.buffer:
            wf.writeframes(tmp)
        wf.close()
        self.clean_buffer()

    def play_frame(self, data):
        self.stream.write(bytes(data))

    def __del__(self):
        self.stream.close()
        self.p.terminate()
