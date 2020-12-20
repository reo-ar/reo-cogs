from typing import Any

import discord
from redbot.core import commands

Cog: Any = getattr(commands, "Cog", object)


class BanMe(Cog):
    """
    Ridiculous cog for a ridiculous request
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def banme(self, ctx):
        """
        Does what it says on the tin, bans yourself.
        """
        await ctx.guild.ban(ctx.author, reason="You literally banned yourself")