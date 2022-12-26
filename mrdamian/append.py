#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component
import queue


class Append(Component):
    def __init__(self, src, val):
        self.src = src
        self.dst = queue.Queue()
        self.val = val

    def process(self):
        msg = self.src.get()
        self.dst.put(dict(msg, **self.val))
