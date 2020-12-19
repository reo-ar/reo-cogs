from .budgetnitro import BudgetNitro


def setup(bot):
    bot.add_cog(BudgetNitro(bot))
