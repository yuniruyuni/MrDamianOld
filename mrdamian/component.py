#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import asyncio


class Component:
    def up(self) -> None:
        pass

    def down(self) -> None:
        pass

    async def process(self):
        """
        The process method. It should be implemented from concrete pipelines.
        This method will do something when event comes this pipeline.
        """
        pass

    async def run(self):
        try:
            self.up()
            try:
                while True:
                    await self.process()
            except Exception as e:
                print("pipeline thread is broken because of: ")
                print(e)
                raise
        finally:
            self.down()
