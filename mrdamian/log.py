#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipeline import Pipeline

class Log(Pipeline):
    def __init__(self, src, target, io):
        self.src = src
        self.io = io
        self.target = target

    def process(self):
        msg = self.src.get()
        self.io.write(f"{msg[self.target]}\n")
        self.io.flush()
