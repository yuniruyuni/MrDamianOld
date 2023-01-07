#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import asyncio
# import codecs # for outputting files.

from recording import Recording
from recognize import Recognize
from translate import Translate
from twitch import Bot, Receive, Send

# from append import Append
from log import Log

async def run():
    print("initializing...")
    # talklog = codecs.open("talk.log", mode="w", encoding="utf-8")
    # talklog = sys.stdout
    # TODO: "dst" queue should be hidden by `Pipeline` abstraction.
    bot = Bot()
    receive = Receive(bot)
    # recording = Recording(0.001)
    # recognize = Recognize("audio").connect(recording)
    translate = Translate("{text}", "{lang}", "EN-US").connect(receive)
    # append = Append({"msg": "audio detected!"}).connect(recording)
    # log = Log("text", talklog).connect(translate)
    send = Send(bot).connect(translate)

    pipes = [receive, translate, send]

    tasks = [asyncio.create_task(pipe.run()) for pipe in pipes]
    print("started!")
    await asyncio.gather(*tasks)


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    asyncio.run(run())

if __name__ == "__main__":
    main()
