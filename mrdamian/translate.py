#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
import deepl

from mrdamian.component import Component

from dotenv import dotenv_values

config = dotenv_values(".env")

class Translate(Component):
    def __init__(self, src):
        self.src = src
        self.dst = queue.Queue()

        self.api = deepl.Translator(config['DEEPL_API_KEY'])

    def process(self):
        msg = self.src.get()

        srclang = "JA"
        dstlang = "EN-US"

        # srclang = msg[self.srclang]
        # dstlang = self.dstlang

        try:
            res = self.api.translate_text(
                msg["text"],
                source_lang=srclang,
                target_lang=dstlang,
            )
            msg["text"] = res.text
            msg["lang"] = dstlang
            self.dst.put(msg)
        except Exception as e:
            print(e)
