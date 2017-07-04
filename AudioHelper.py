# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import numpy as np
import wave


class InAudio(object):
    def __init__(self):
        self.NUM_SAMPLES = 2000
        self.SAMPLING_RATE = 8000
        p = PyAudio()
        self.stream = p.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE,
                             input=True, frames_per_buffer=self.NUM_SAMPLES)

    def getFrame(self):
        return self.stream.read(self.NUM_SAMPLES)


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

    def playFrame(self,data):
        self.stream.write(data)

    def __del__(self):
        self.stream.close()
        self.p.terminate()


# pi = InAudio()
# po = OutAudio()
# while True:
#     string_audio_data = pi.getFrame()
#     po.playFrame(string_audio_data)
