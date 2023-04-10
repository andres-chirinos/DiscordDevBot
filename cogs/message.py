import os
import discord
from discord import app_commands
from discord.ext import commands
from __init__ import guild_id, Cache

class Message(commands.GroupCog, name = 'message'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    ##Message
    #Send thread
    @app_commands.command(name = 'send', description = 'Enviar un mensaje')
    @app_commands.describe(text = 'Contenido')
    async def send(self, interaction: discord.Interaction, text:str):
        try:
            await interaction.channel.send(content=text)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Edit message
    @app_commands.command(name = 'edit', description = 'Editar un mensaje')
    @app_commands.describe(messageid = 'Id del mensaje', content = 'Nuevo contenido')
    async def edit(self, interaction: discord.Interaction, messageid:str, content:str = None):
        try:
            message = await interaction.channel.fetch_message(int(messageid))
            if content is None: content = message.content
            await message.edit(content = content)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    @app_commands.command(name = 'purge', description = 'Eliminar mensajes')
    @app_commands.describe(limit = '¿Cuentos mensajes?')
    async def purge(self, interaction: discord.Interaction, limit: int = None):
        try:
            await interaction.channel.purge(limit=limit)
            return await interaction.response.send_message(content = f'🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):       
    await bot.add_cog(Message(bot), guild = discord.Object(id = guild_id))       