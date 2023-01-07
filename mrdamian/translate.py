#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
import deepl

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline

from dotenv import dotenv_values

config = dotenv_values(".env")


class Translate(Component):
    def __init__(self, text, srclang, dstlang):
        super().__init__()
        self.api = deepl.Translator(config['DEEPL_API_KEY'])
        self.text = text
        self.srclang = srclang
        self.dstlang = dstlang

    async def process(self, slots):
        text = self.text.format(**slots)
        srclang = self.srclang.format(**slots).upper()
        dstlang = self.dstlang.format(**slots).upper()

        try:
            res = self.api.translate_text(
                text,
                source_lang=srclang,
                target_lang=dstlang,
            )
            await self.pipeline.put(dict(slots, text=res.text, lang=dstlang))
        except Exception as e:
            print(e)
