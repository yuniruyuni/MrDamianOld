#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class Pipeline:
    def start(self) -> threading.Thread:
        self.closed = False
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def close(self) -> None:
        self.closed = True

    def up(self) -> None:
        pass

    def down(self) -> None:
        pass

    def process(self):
        """
        The process method. It should be implemented from concrete pipelines.
        This method will do something when event comes this pipeline.
        """
        pass

    def run(self):
        try:
            self.up()
            while not self.closed:
                try:
                    self.process()
                except Exception as e:
                    print("pipeline thread is broken because of: ")
                    print(e)
                    raise
        except Exception as e:
            self.down()
            raise
