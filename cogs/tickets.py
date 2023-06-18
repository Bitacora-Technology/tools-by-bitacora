from discord.ext import commands

from bot import Bot


class Tickets(commands.GroupCog, group_name='tickets'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Tickets(bot))
