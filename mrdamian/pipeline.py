#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from mrdamian.component import Component

class Pipeline(Component):
    def __init__(self):
        self.dsts = []

    def connect(self) -> asyncio.Queue:
        """
        Acquire a new queue and return it back.
        """
        # TODO: protect with mutex
        dst = asyncio.Queue()
        self.dsts.append(dst)
        return dst

    async def put(self, msg):
        for dst in self.dsts:
            await dst.put(msg.copy())
