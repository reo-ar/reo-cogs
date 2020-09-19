from .guardian import guardian


def setup(bot):
    bot.add_cog(guardian(bot))
