import os
import discord
from discord import app_commands
from discord.ext import commands
from __init__ import ServerId

class Vote_view(discord.ui.View):
    def __init__(self) -> None:
        self.datavotes = dict()
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Registrar", style = discord.ButtonStyle.grey, custom_id = 'stopvote')
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.get_role(1020129264726712371) is not None:
                await interaction.channel.send(content = f'{self.datavotes.values()}')
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

class Message(commands.GroupCog, name = 'message'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    ##Message
    #Send thread
    @app_commands.command(name = 'send', description = 'Send a message')
    @app_commands.describe(text = 'Text to send')
    async def send(self, interaction: discord.Interaction, text:str):
        try:
            await interaction.channel.send(content=text)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Edit message
    @app_commands.command(name = 'edit', description = 'Edit a message')
    @app_commands.describe(text = 'Text to edit')
    async def edit(self, interaction: discord.Interaction, messageid:str, text:str = None):
        try:
            message = await interaction.channel.fetch_message(int(messageid))
            if text is None: text = message.content
            await message.edit(content = text)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    @app_commands.command(name = 'purge', description = 'Purge a messages')
    @app_commands.describe(limit = 'Amount of messages want to purge')
    async def purge(self, interaction: discord.Interaction, limit: int = None):
        try:
            await interaction.channel.purge(limit=limit)
            return await interaction.response.send_message(content = f'🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):       
    await bot.add_cog(Message(bot), guild = discord.Object(id = ServerId))       