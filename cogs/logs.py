from importlib import reload

import discord
from discord import ButtonStyle, Interaction, app_commands
from discord.ext import commands
from discord.ui import Button, View

from bot import Bot
from cogs.utils import mongo

logs_options = [
    'Joined',
    'Left',
    'Edited',
    'Deleted',
    'Created'
]


def logs_embed(options: list[str], settings: dict[str, str]) -> discord.Embed:
    title = 'Logs Settings'
    footer =\
        'Click any of the buttons below to reset the selected channel'
    embed = discord.Embed(title=title)
    embed.set_footer(text=footer)

    for option in options:
        value = settings.get(option.lower(), None)
        if value:
            value = f'<#{value}>'
        else:
            value = 'Not specified'
        embed.add_field(name=option, value=value)

    return embed


class ResetLogsButton(Button):
    def __init__(self, option: str, has_value: bool) -> None:
        style = ButtonStyle.danger
        disabled = not has_value
        super().__init__(style=style, label=option, disabled=disabled)

    async def callback(self, interaction: Interaction) -> None:
        guild = mongo.Guild(interaction.guild_id)
        query = {'$set': {self.label.lower(): None}}
        await guild.update(query)
        guild_settings = await guild.check()

        embed = logs_embed(logs_options, guild_settings)
        view = ResetLogsView(logs_options, guild_settings)
        await interaction.response.edit_message(embed=embed, view=view)


class ResetLogsView(View):
    def __init__(self, options: list[str], settings: dict[str, str]) -> None:
        super().__init__(timeout=None)
        for option in options:
            has_value = bool(settings.get(option.lower(), None))
            self.add_item(ResetLogsButton(option, has_value))


class Logs(commands.GroupCog, group_name='logs'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        reload(mongo)

    async def update_guild(
        self, guild_id: int, channel_id: int, option: str
    ) -> None:
        guild = mongo.Guild(guild_id)
        query = {'$set': {option: channel_id}}
        await guild.update(query)

    async def interaction_response(self, interaction: Interaction) -> None:
        content = 'Logs settings have been updated successfully'
        await interaction.response.send_message(content, ephemeral=True)

    @app_commands.command()
    async def joined(
        self, interaction: Interaction, channel: discord.TextChannel
    ) -> None:
        """Get notified every time a user joins the server"""
        await self.update_guild(interaction.guild_id, channel.id, 'joined')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def left(
        self, interaction: Interaction, channel: discord.TextChannel
    ) -> None:
        """Get notified every time a user leaves the server"""
        await self.update_guild(interaction.guild_id, channel.id, 'left')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def edited(
        self, interaction: Interaction, channel: discord.TextChannel
    ) -> None:
        """Get notified every time a user edits a message"""
        await self.update_guild(interaction.guild_id, channel.id, 'edited')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def deleted(
        self, interaction: Interaction, channel: discord.TextChannel
    ) -> None:
        """Get notified every time a user deletes a message"""
        await self.update_guild(interaction.guild_id, channel.id, 'deleted')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def created(
        self, interaction: Interaction, channel: discord.TextChannel
    ) -> None:
        """Get notified every time a user creates a thread"""
        await self.update_guild(interaction.guild_id, channel.id, 'created')
        await self.interaction_response(interaction)

    @app_commands.command()
    async def settings(self, interaction: Interaction) -> None:
        """Check and update logs settings"""
        guild = mongo.Guild(interaction.guild_id)
        guild_settings = await guild.check()

        embed = logs_embed(logs_options, guild_settings)
        view = ResetLogsView(logs_options, guild_settings)
        await interaction.response.send_message(
            embed=embed, view=view, ephemeral=True
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        pass

    @commands.Cog.listener()
    async def on_raw_member_remove(
        self, payload: discord.RawMemberRemoveEvent
    ) -> None:
        pass

    @commands.Cog.listener()
    async def on_raw_message_edit(
        self, payload: discord.RawMessageUpdateEvent
    ) -> None:
        pass

    @commands.Cog.listener()
    async def on_raw_message_deleted(
        self, payload: discord.RawMessageDeleteEvent
    ) -> None:
        pass

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread) -> None:
        pass


async def setup(bot: Bot) -> None:
    await bot.add_cog(Logs(bot))
