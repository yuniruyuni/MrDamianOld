#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
# import codecs # for outputting files.
import asyncio

from recording import Recording
from recognize import Recognize
from translate import Translate
from twitch import Bot, Receive, Send

# from append import Append
from log import Log

async def run():
    print("initializing...")
    # talklog = codecs.open("talk.log", mode="w", encoding="utf-8")
    talklog = sys.stdout
    # TODO: "dst" queue should be hidden by `Pipeline` abstraction.
    bot = Bot()
    receive = Receive(bot)
    # recording = Recording(0.001)
    # recognize = Recognize(recording.dst, "audio")
    translate = Translate(receive.dst, "{text}", "{lang}", "EN-US")
    # translate = Translate(recognize.dst, "{text}", "{lang}", "EN-US")
    # append = Append(recording.dst, {"msg": "audio detected!"})
    # log = Log(translate.dst, "text", talklog)
    send = Send(bot, translate.dst)

    pipes = [receive, recording, recognize, translate, send]

    tasks = [asyncio.create_task(pipe.run()) for pipe in pipes]
    print("started!")
    await asyncio.gather(*tasks)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    asyncio.run(run())

if __name__ == "__main__":
    main()
