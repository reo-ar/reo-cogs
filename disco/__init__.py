from .disco import DiscoMode


def setup(bot):
    bot.add_cog(DiscoMode(bot))
