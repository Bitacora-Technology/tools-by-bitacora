from discord import Interaction, TextChannel, app_commands
from discord.ext import commands
from cogs.utils import mongo

from bot import Bot


class Logs(commands.GroupCog, group_name='logs'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def update_guild(
        self, guild_id: int, channel_id: int, action: str
    ) -> None:
        guild = mongo.Guild(guild_id)
        query = {'$set': {action: channel_id}}
        await guild.update(query)

    async def interaction_response(self, interaction: Interaction) -> None:
        content = 'Logs settings have been updated successfully'
        await interaction.response.send_message(content, ephemeral=True)

    @app_commands.command()
    async def joined(
        self, interaction: Interaction, channel: TextChannel
    ) -> None:
        """Get notified every time a user joins the server"""
        await self.update_guild(interaction.guild_id, channel.id, 'joined')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def left(
        self, interaction: Interaction, channel: TextChannel
    ) -> None:
        """Get notified every time a user leaves the server"""
        await self.update_guild(interaction.guild_id, channel.id, 'left')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def edited(
        self, interaction: Interaction, channel: TextChannel
    ) -> None:
        """Get notified every time a user edits a message"""
        await self.update_guild(interaction.guild_id, channel.id, 'edited')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def deleted(
        self, interaction: Interaction, channel: TextChannel
    ) -> None:
        """Get notified every time a user deletes a message"""
        await self.update_guild(interaction.guild_id, channel.id, 'deleted')
        await self.interaction_response(interaction)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Logs(bot))
