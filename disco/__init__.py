from .disco import Disco


def setup(bot):
    bot.add_cog(Disco(bot))
