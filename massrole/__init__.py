from .massrole import MassRole


def setup(bot):
    bot.add_cog(MassRole(bot))
