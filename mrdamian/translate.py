#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
import deepl

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline

from dotenv import dotenv_values

config = dotenv_values(".env")


class Translate(Component):
    def __init__(self, src, text, srclang, dstlang):
        self.src = src.connect()
        self.dst = Pipeline()
        self.api = deepl.Translator(config['DEEPL_API_KEY'])
        self.text = text
        self.srclang = srclang
        self.dstlang = dstlang

    async def process(self):
        msg = await self.src.get()

        text = self.text.format(**msg)
        srclang = self.srclang.format(**msg).upper()
        dstlang = self.dstlang.format(**msg).upper()

        try:
            res = self.api.translate_text(
                text,
                source_lang=srclang,
                target_lang=dstlang,
            )
            await self.dst.put(dict(msg, text=res.text, lang=dstlang))
        except Exception as e:
            print(e)
