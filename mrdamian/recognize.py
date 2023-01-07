#!/usr/bin/env python
# -*- coding: utf-8 -*-

import whisper

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline


class Recognize(Component):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.model = whisper.load_model("medium")
        self.options = whisper.DecodingOptions

    async def process(self, slots):
        audio = slots[self.name]
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        _, probs = self.model.detect_language(mel)
        lang = max(probs, key=probs.get)

        result = whisper.decode(self.model, mel, self.options)

        self.pipeline.put(dict(slots, lang=lang, text=result.text))
