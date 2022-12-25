#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipeline import Pipeline
import queue

class Append(Pipeline):
    def __init__(self, src, val):
        self.src = src
        self.dst = queue.Queue()
        self.val = val

    def process(self):
        msg = self.src.get()
        self.dst.put(dict(msg, **self.val))
