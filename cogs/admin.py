from discord.ext import commands

from bot import Bot


class Admin(commands.GroupCog, group_name='admin'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Admin(bot))
