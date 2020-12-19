from redbot.core import Config, commands, checks
import discord
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class HoistCrabber(Cog):
    """
    Customizable hoist crabber
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=10011)
        default_guild = {
            "hoist_list": [],
            "crab_char": "🦀"
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def edithoistchar(self, ctx, hoist_char: str):
        """
        Adds/removes a character/characters to be renamed if used
        """
        hoist_list = self.config.guild(ctx.guild).hoist_list

        hoistlist = await hoist_list()
        embed = discord.Embed(title="Hoist Crabber", color=0xff0080)

        if hoist_char in hoistlist:
            async with hoist_list() as hoist_list:
                hoist_list.remove(hoist_char)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="Removed hoist char", value=hoist_char)

        else:
            async with hoist_list() as hoist_list:
                hoist_list.append(hoist_char)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name="Added new hoist char:", value=hoist_char)

        await ctx.send(embed=embed)

    @commands.command()
    async def hoistcharlist(self, ctx):
        """
        Displays the current hoist chars to be renamed
        """
        hoist_list = await self.config.guild(ctx.guild).hoist_list()
        hoist_chars = "\n".join(hoist_list)
        embed = discord.Embed(title="Hoist Crabber List", color=0xff0080)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="List:", value=hoist_chars)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, previous_member_state, member):
        hoist_list = await self.config.guild(member.guild).hoist_list()
        crab_char = await self.config.guild(member.guild).crab_char()
        member_nick = member.nick
        for hoist_char in hoist_list:
            if member_nick.startswith(hoist_char):
                await member.edit(nick=crab_char)
