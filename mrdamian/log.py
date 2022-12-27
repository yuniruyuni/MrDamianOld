#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component


class Log(Component):
    def __init__(self, src, target, io):
        self.src = src.connect()
        self.io = io
        self.target = target

    async def process(self):
        msg = self.src.get()
        self.io.write(f"{msg[self.target]}\n")
        self.io.flush()
