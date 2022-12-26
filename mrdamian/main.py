#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
# import codecs # for outputting files.

from recording import Recording
from recognize import Recognize
from translate import Translate

# from append import Append
from log import Log

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # talklog = codecs.open("talk.log", mode="w", encoding="utf-8")
    talklog = sys.stdout

    print("initializing...")

    # TODO: "dst" queue should be hidden by `Pipeline` abstraction.
    recording = Recording(0.001)
    recognize = Recognize(recording.dst, "audio")
    translate = Translate(recognize.dst)
    # append = Append(recording.dst, {"msg": "audio detected!"})
    log = Log(translate.dst, "text", talklog)

    pipes = [recording, recognize, translate, log]

    threads = [pipe.start() for pipe in pipes]
    print("started!")
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
