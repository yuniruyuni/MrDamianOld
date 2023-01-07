#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import twitchio

from twitchio.ext import commands

from mrdamian.component import Component
from mrdamian.pipeline import Pipeline

from dotenv import dotenv_values

config = dotenv_values(".env")


class Bot(commands.Bot):
    def __init__(self):
        self.name = config['TWITCH_USERNAME']
        self.dst = Pipeline()
        super().__init__(
            token=config['TWITCH_OAUTH'],
            prefix='?',
            initial_channels=[config['TWITCH_CHANNEL']],
        )

    async def event_channel_joined(self, channel: twitchio.Channel):
        await channel.send(f"{self.name} is joined channel.")

    async def event_message(self, msg: twitchio.Message) -> None:
        # skip if the message is sent from bot itself.
        if msg.echo:
            return

        # process message as a command.
        if not msg.echo:
            await self.handle_commands(msg)

        await self.dst.put({"lang": "ja", "author": msg.author.name, "text": msg.content})


class Receive(Component):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.pipeline = bot.dst

    async def up(self):
        await self.bot.start()

    async def down(self):
        await self.bot.close()

    async def process(self, args):
        await asyncio.sleep(1)


class Send(Component):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def process(self, args):
        for channel in self.bot.connected_channels:
            await channel.send(args['text'])
