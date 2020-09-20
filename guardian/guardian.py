from redbot.core import Config, commands, checks
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

    async def add_to_config(self, ctx, string_to_add: str, command_list, command: str):
        """
        :param self:
        :param ctx: command context
        :param string_to_add: string to be added to the command's list
        :param command_list: list that the string will be added to
        :param command: command that that executed this function
        """

        try:

            cl = await command_list()
            commandlist = cl

            if string_to_add in commandlist:
                print(f"trying to remove {string_to_add}")

                async with command_list() as command_list:
                    print(f"Filter removed {string_to_add}")
                    command_list.remove(string_to_add)

                removeembed = discord.Embed(title="Guardian", color=0xff0080)
                removeembed.set_thumbnail(url=ctx.guild.icon_url)
                removeembed.add_field(name=f"Removed {command} filter", value=string_to_add)
                await ctx.send(embed=removeembed)

            else:
                print(f"trying to add {string_to_add}")

                async with command_list() as command_list:
                    print(f"New filter added {string_to_add}")
                    command_list.append(string_to_add)

                addembed = discord.Embed(title="Guardian", color=0xff0080)
                addembed.set_thumbnail(url=ctx.guild.icon_url)
                addembed.add_field(name=f"Added new {command} filter", value=string_to_add)
                await ctx.send(embed=addembed)

        except Exception as exception:
            error_string = f"There was an exception executing the {command}, error returned: {exception}"
            print(error_string)
            await ctx.send(error_string)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def regexkick(self, ctx, string_to_add: str):
        """
        Adds/removes a regex kick filter
        """
        regex_kick_list = self.config.guild(ctx.guild).regex_kick_list
        command = "Regex Kick"
        await self.add_to_config(ctx, string_to_add, regex_kick_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def stringkick(self, ctx, string_to_add: str):
        """
        Adds/removes a string match kick filter
        """
        string_kick_list = self.config.guild(ctx.guild).string_kick_list
        command = "String Kick"
        await self.add_to_config(ctx, string_to_add, string_kick_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def regexban(self, ctx, string_to_add: str):
        """
        Adds/removes a regex ban filter
        """
        regex_ban_list = self.config.guild(ctx.guild).regex_ban_list
        command = "Regex Ban"
        await self.add_to_config(ctx, string_to_add, regex_ban_list, command)

    @commands.command()
    @checks.admin_or_permissions(ban_members=True)
    async def stringban(self, ctx, string_to_add: str):
        """
        Adds/removes a string match ban filter
        """
        string_ban_list = self.config.guild(ctx.guild).string_ban_list
        command = "String Ban"
        await self.add_to_config(ctx, string_to_add, string_ban_list, command)

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
        member_name = member.name()
        guild_group = self.config.guild(member.guild)
        string_bans = await guild_group.string_ban_list()
        string_kicks = await guild_group.string_kick_list()
        regex_bans = await guild_group.regex_ban_list()
        regex_kicks = await guild_group.regex_kick_list()

        for ban in string_bans:
            if ban in member_name:
                await ban(member, reason=f"Guardian has detected this user's "
                                         f"name contains the following string ban: {ban}")

        for ban in regex_bans:
            if re.search(ban, member_name):
                await ban(member, reason=f"Guardian has detected this user matched the following regex ban: {ban}")

        for kick in string_kicks:
            if kick in member_name:
                await kick(member, reason=f"Guardian has detected this user's"
                                          f"name contains the following string kick {kick}")

        for kick in regex_kicks:
            if re.search(kick, member_name):
                await kick(member,
                           reason=f"Guardian has detected this user matched the following regex kick: {kick}")
