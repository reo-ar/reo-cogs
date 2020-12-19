from .guardian import Guardian


def setup(bot):
    bot.add_cog(Guardian(bot))
