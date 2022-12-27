#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitchio
import asyncio

from twitchio.ext import commands

from mrdamian.component import Component

from dotenv import dotenv_values

config = dotenv_values(".env")

class Bot(commands.Bot):
    def __init__(self):
        self.name = config['TWITCH_USERNAME']
        self.dst = asyncio.Queue()
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

class Receive(Component, commands.Bot):
    def __init__(self, bot):
        self.bot = bot
        self.dst = bot.dst

    async def process(self):
        await self.bot.start()

class Send(Component, commands.Bot):
    def __init__(self, bot, src):
        self.bot = bot
        self.src = src

    async def process(self):
        msg = await self.src.get()
        for channel in self.bot.connected_channels:
            await channel.send(f"translated: {msg['text']}")
