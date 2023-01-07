#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline


class Append(Component):
    def __init__(self, val):
        super().__init__()
        self.val = val

    async def process(self, slots):
        self.pipeline.put(dict(slots, **self.val))
