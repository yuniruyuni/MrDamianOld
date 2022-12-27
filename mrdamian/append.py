#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline


class Append(Component):
    def __init__(self, src, val):
        self.src = src.connect()
        self.dst = Pipeline()
        self.val = val

    async def process(self):
        msg = await self.src.get()
        await self.dst.put(dict(msg, **self.val))
