#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
import whisper

from mrdamian.component import Component


class Recognize(Component):
    def __init__(self, src, name):
        self.src = src
        self.dst = queue.Queue()
        self.name = name
        self.model = whisper.load_model("medium")
        self.options = whisper.DecodingOptions
        self.options.language = "ja"

    def process(self):
        msg = self.src.get()
        audio = msg[self.name]
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        _, probs = self.model.detect_language(mel)
        lang = max(probs, key=probs.get)

        result = whisper.decode(self.model, mel, self.options)

        val = {"lang": lang, "text": result.text}
        self.dst.put(dict(msg, **val))
