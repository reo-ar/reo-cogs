import re
from typing import Any

import discord
from redbot.core import commands

Cog: Any = getattr(commands, "Cog", object)


class BudgetNitro(Cog):
    """
    Replies with emoji if string has a guild emoji in it!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            owo = message.guild.emojis
        except AttributeError:
            return
        msg = message.content
        ouo = False

        if message.author.bot is False and "<a:" not in message.content:
            for emoji in owo:
                if emoji.animated:
                    if emoji.name in msg:
                        OwO = emoji.name
                        uwu = emoji.id
                        msg = re.sub(OwO, ("<a:%s:%d>" % (OwO, uwu)), msg)
                        ouo = True

        if ouo is True:
            await message.channel.send(msg)
