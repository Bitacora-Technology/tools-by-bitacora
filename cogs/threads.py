from discord.ext import commands

from bot import Bot


class Threads(commands.GroupCog, group_name='threads'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Threads(bot))
