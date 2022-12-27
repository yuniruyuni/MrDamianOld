#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrdamian.component import Component


class Append(Component):
    def __init__(self, src, val):
        self.src = src
        self.dst = asyncio.Queue()
        self.val = val

    async def process(self):
        msg = await self.src.get()
        await self.dst.put(dict(msg, **self.val))
