#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

class ImmediateSlot:
    async def get(self):
        return {}

class Slot:
    def __init__(self, *srcs):
        self.srcs = [src.connect() for src in srcs]

    async def get(self):
        for src in self.srcs:
            if src.empty():
                continue
            return await src.get()
        await asyncio.sleep(1)
