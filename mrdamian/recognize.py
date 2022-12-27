#!/usr/bin/env python
# -*- coding: utf-8 -*-

import whisper

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline


class Recognize(Component):
    def __init__(self, src, name):
        self.src = src.connect()
        self.dst = Pipeline()
        self.name = name
        self.model = whisper.load_model("medium")
        self.options = whisper.DecodingOptions

    async def process(self):
        msg = await self.src.get()
        audio = msg[self.name]
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        _, probs = self.model.detect_language(mel)
        lang = max(probs, key=probs.get)

        result = whisper.decode(self.model, mel, self.options)

        await self.dst.put(dict(msg, lang=lang, text=result.text))
