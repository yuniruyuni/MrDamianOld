#!/usr/bin/env python
# -*- coding: utf-8 -*-

import soundcard as sc
import numpy as np
import queue

from pipeline import Pipeline

SAMPLE_RATE = 48000
INTERVAL = 3
BUFFER_SIZE = 1024 * 4

ACTUAL_BUFFER_SIZE = SAMPLE_RATE * INTERVAL + BUFFER_SIZE

class Recording(Pipeline):
    def __init__(self):
        self.dst = queue.Queue()
        self.buffer = np.empty(ACTUAL_BUFFER_SIZE, dtype=np.float32)
        self.bins = np.ones(100) / 100
        self.e = 0

    def up(self):
        from pythoncom import CoInitialize
        CoInitialize()
        self.mic = self.__mic()
        self.mic.__enter__()

    def down(self):
        self.mic.__exit__()
        from pythoncom import CoUninitialize
        CoUninitialize()

    def __mic(self):
        m = sc.get_microphone(
            id=sc.default_microphone().name,
            include_loopback=False,
        )
        return m.recorder(samplerate=48000, channels=1)

    def __pool_audio(self, mic, audio, e):
        while e < SAMPLE_RATE * INTERVAL:
            data = mic.record(BUFFER_SIZE)
            audio[e:e+len(data)] = data.reshape(-1)
            e += len(data)
        return e

    def __find_segment(self, audio, e):
        sb = 0 # all segments is started from start of the buffer.
        se = e * 4 // 5
        vol = np.convolve(audio[se:e] ** 2, self.bins, 'same')
        se += vol.argmin()
        return (sb, se)

    def process(self):
        mic = self.mic

        self.e = self.__pool_audio(mic, self.buffer, self.e)

        sb, se = self.__find_segment(self.buffer, self.e)

        # send recorded audio dst for next pipeline
        self.dst.put({"audio": self.buffer[sb:se]})

        prev_buffer = self.buffer
        self.buffer = np.empty(ACTUAL_BUFFER_SIZE, dtype=np.float32)
        self.buffer[:self.e-se] = prev_buffer[se:self.e]
        self.e = self.e - se
