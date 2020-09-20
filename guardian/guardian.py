from redbot.core import Config, commands, checks
from .utils.configutils import add_to_config
import discord
import re
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class guardian(Cog):
    """
    This cog kicks usernames using either regex or string matching.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=10010)
        default_guild = {
            "guardian_list": [],
            "guardian_log": 0
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def regexkick(self, ctx, string_to_add: str):
        """
        Adds/removes a regex kick filter
        """
        regex_kick_list = self.config.guild(ctx.guild).regex_kick_list
        command = "Regex Kick"
        await add_to_config(ctx, string_to_add, regex_kick_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def stringkick(self, ctx, string_to_add: str):
        """
        Adds/removes a string match kick filter
        """
        string_kick_list = self.config.guild(ctx.guild).string_kick_list
        command = "String Kick"
        await add_to_config(ctx, string_to_add, string_kick_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def regexban(self, ctx, string_to_add: str):
        """
        Adds/removes a regex ban filter
        """
        regex_ban_list = self.config.guild(ctx.guild).regex_ban_list
        command = "Regex Ban"
        await add_to_config(ctx, string_to_add, regex_ban_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def stringban(self, ctx, string_to_add: str):
        """
        Adds/removes a string match ban filter
        """
        string_ban_list = self.config.guild(ctx.guild).string_ban_list
        command = "String Ban"
        await add_to_config(ctx, string_to_add, string_ban_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def guardianlist(self, ctx):
        """
        Displays current list of Guardian's filters
        """
        guild_group = self.config.guild(ctx.guild)
        string_bans = "\n".join(await guild_group.string_ban_list())
        string_kicks = "\n".join(await guild_group.string_kick_list())
        regex_bans = "\n".join(await guild_group.regex_ban_list())
        regex_kicks = "\n".join(await guild_group.regex_kick_list())
        embed = discord.Embed(title="Guardian Filter List", color=0xff0080)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed = embed.add_field(name="String Ban List:", value=f"```{string_bans}```")
        embed = embed.add_field(name="Regex Ban List:", value=f"```{regex_bans}```")
        embed = embed.add_field(name="String Kick List:", value=f"```{string_kicks}```")
        embed = embed.add_field(name="Regex Kick List:", value=f"```{regex_kicks}```")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        member_name = member.name
        guild_group = self.config.guild(member.guild)
        string_bans = await guild_group.string_ban_list()
        string_kicks = await guild_group.string_kick_list()
        regex_bans = await guild_group.regex_ban_list()
        regex_kicks = await guild_group.regex_kick_list()

        # Do bans first then kicks in case of duplicates

        for ban in string_bans:
            if ban in member_name:
                await member.ban(reason=f"Guardian has detected this user's "
                                        f"name contains the following string ban: {ban}")
                return

        for ban in regex_bans:
            if re.search(ban, member_name):
                await member.ban(reason=f"Guardian has detected this user matched the following regex ban: {ban}")
                return

        for kick in string_kicks:
            if kick in member_name:
                await member.kick(reason=f"Guardian has detected this user's"
                                         f"name contains the following string kick {kick}")
                return

        for kick in regex_kicks:
            if re.search(kick, member_name):
                await member.kick(reason=f"Guardian has detected this user matched the following regex kick: {kick}")
                return
