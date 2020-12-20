from .banme import BanMe

def setup(bot):
    bot.add_cog(BanMe(bot))