from .hoistcrabber import HoistCrabber


def setup(bot):
    bot.add_cog(HoistCrabber(bot))
