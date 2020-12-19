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
        owo = message.guild.emojis
        if message.author.bot is False and "<a:" not in message.content:
            for emoji in owo:
                if emoji.animated:
                    if emoji.name in message.content:
                        OwO = emoji.name
                        uwu = emoji.id
                        msg = re.sub(OwO, ("<a:%s:%d>" % (OwO, uwu)), message.content)
                        await message.channel.send(msg)
                        return ()
