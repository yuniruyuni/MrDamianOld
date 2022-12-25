#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import codecs

from recording import Recording
from append import Append
from log import Log

talklog = codecs.open("talk.log", mode="w", encoding="utf-8")
# talklog = sys.stdout

# TODO: "dst" queue should be hidden by `Pipeline` abstraction.
recording = Recording()
append = Append(recording.dst, {"msg": "audio detected!"})
log = Log(append.dst, "msg", talklog)

pipes = [recording, append, log]

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    threads = [pipe.start() for pipe in pipes]
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
