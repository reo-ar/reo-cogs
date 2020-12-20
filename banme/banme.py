from typing import Any

import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate

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
        try:
            pred = MessagePredicate.yes_or_no()
            await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
            await ctx.send("Are you sure about banning yourself? Answer with a `Yes` or a `No`")
            if pred.result is True:
                await ctx.guild.ban(ctx.author, reason="You literally banned yourself")
        except Exception as e:
            await ctx.send("Yeah I don't have perms to do that.")