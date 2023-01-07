#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component


class Log(Component):
    def __init__(self, target, io):
        super().__init__()
        self.target = target
        self.io = io

    async def process(self, slots):
        self.io.write(f"{slots[self.target]}\n")
        self.io.flush()
