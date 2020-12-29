import random
from typing import Any
import discord
from redbot.core import Config, checks, commands

Cog: Any = getattr(commands, "Cog", object)


class Disco(Cog):
    """
    This cog will randomize the color of your Roles!
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=801)
        default_guild = {"role": 0, "act": False, "ich": 0, "count": 5}
        self.config.register_guild(**default_guild)

    i = 0

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def discocount(self, ctx, count: int):
        """
        Changes the amount of message before the color changes
        """
        await self.config.guild(ctx.guild).count.set(count)
        await ctx.send("Count has been set to: " + str(count))

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def discorole(self, ctx, role: int):
        """
        Changes the role to change color.
        """
        await self.config.guild(ctx.guild).role.set(role)
        await ctx.send("Role has been set to: " + str(role))

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def discotoggle(self, ctx):
        """
        Toggles randomizer on and off.
        """
        ara = self.config.guild(ctx.guild)
        tg = not await ara.act()
        await ara.act.set(tg)
        ta = await ara.act()
        await ctx.send("Randomizer has been set to: " + str(ta))

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def discochannel(self, ctx, ch: int):
        """
        Sets channel to listen to.
        """
        ara = self.config.guild(ctx.guild)
        await ara.ich.set(ch)
        await ctx.send("Disco channel has been set to: " + str(ch))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            ara = self.config.guild(message.guild)
            if message.channel.id == await ara.ich():
                self.i = self.i + 1
                if self.i == await ara.count():
                    self.i = 0
                    tg = await ara.act()
                    if tg:
                        r = random.randint(0, 255)
                        g = random.randint(0, 255)
                        b = random.randint(0, 255)
                        owo = message.guild.get_role(await ara.role())
                        await owo.edit(colour=discord.Colour.from_rgb(r, g, b))
        except Exception as e:
            print(e)
            pass
