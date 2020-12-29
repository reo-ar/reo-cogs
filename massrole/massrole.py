from redbot.core import commands
from redbot.core import checks
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class MassRole(Cog):
    """
    Adds role to every member!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.admin()
    async def massrole(self, ctx, roleid: int):
        role = ctx.guild.get_role(roleid)
        ara = ctx.guild.members
        count = 0
        for member in ara:
            if not member.bot:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    ctx.send("Error : " + str(e))
                await ctx.send("Added role to : ``" + member.name + "``")
                count += 1
        await ctx.send("Finished Adding roles to " + str(count) + "members!")