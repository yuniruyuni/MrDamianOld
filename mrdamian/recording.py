#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import soundcard as sc
import numpy as np

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline

SAMPLE_RATE = 16000  # sampling rate required from whisper model.
INTERVAL = 3  # 3-seconds
RECORD_SIZE = 1024 * 4  # 4KiB
# size of buffer. RECORD_SIZE addition is for padding.
BUFFER_SIZE = SAMPLE_RATE * INTERVAL + RECORD_SIZE


class Recording(Component):
    def __init__(self, threshold):
        self.dst = Pipeline()
        self.buffer = np.empty(BUFFER_SIZE, dtype=np.float32)
        self.e = 0
        self.threshold = threshold

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
        return m.recorder(samplerate=SAMPLE_RATE, channels=1)

    async def __pool_audio(self, mic, audio, e):
        while e < SAMPLE_RATE * INTERVAL:
            data = await asyncio.to_thread(mic.record, RECORD_SIZE)
            audio[e:e+len(data)] = data.reshape(-1)
            e += len(data)
        return e

    def __find_segment(self, audio, e):
        sb = 0  # all segments is started from start of the buffer.
        se = (e * 4) // 5
        # moving average for each 100 samples.
        bins = np.ones(100) / 100
        vol = np.convolve(audio[se:e] ** 2, bins, "same")
        se += vol.argmin()
        return (sb, se)

    async def process(self):
        self.e = await self.__pool_audio(self.mic, self.buffer, self.e)

        sb, se = self.__find_segment(self.buffer, self.e)

        # send recorded audio dst for next pipeline
        audio = self.buffer[sb:se]
        if (audio**2).max() > self.threshold:
            await self.dst.put({"audio": audio})

        prev_buffer = self.buffer
        self.buffer = np.empty(BUFFER_SIZE, dtype=np.float32)
        self.buffer[:self.e-se] = prev_buffer[se:self.e]
        self.e = self.e - se
