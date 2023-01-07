#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing

from mrdamian.pipeline import Pipeline
from mrdamian.slot import Slot, ImmediateSlot

class Component:
    def __init__(self):
        self.slot = ImmediateSlot()
        self.pipeline = Pipeline()

    def slots(self) -> typing.List[str]:
        """
        Show input slot names.
        Slots will generated from message by user slot format setting.
        """
        []

    def connect(self, *srcs):
        srcs = [src.pipeline for src in srcs]
        self.slot = Slot(*srcs)
        return self

    async def up(self):
        pass

    async def down(self):
        pass

    async def process(self, slots):
        """
        The process method. It should be implemented from concrete pipelines.
        This method will do something when event comes this pipeline.
        """
        pass

    async def run(self):
        try:
            await self.up()
            try:
                while True:
                    slots = await self.slot.get()
                    await self.process(slots)
            except Exception as e:
                print("pipeline thread is broken because of: ")
                print(e)
                raise
        finally:
            await self.down()
