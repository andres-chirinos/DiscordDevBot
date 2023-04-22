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
    #Send
    @app_commands.command(name = 'send', description = 'Enviar un mensaje')
    @app_commands.describe(content = 'Contenido')
    async def send(self, interaction: discord.Interaction, content:str):
        try:
            await interaction.channel.send(content=content)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Edit
    @app_commands.command(name = 'edit', description = 'Editar un mensaje')
    @app_commands.describe(messagelink = 'Enlace al mensaje', content = 'Nuevo contenido')
    async def edit(self, interaction: discord.Interaction, messagelink:str, content:str):
        try:
            link = messagelink.split('/')
            channel = self.bot.get_channel(int(link[-2]))
            message = await channel.fetch_message(int(link[-1]))
            await message.edit(content = content)     
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Delete
    @app_commands.command(name = 'delete', description = 'Eliminar un mensaje')
    @app_commands.describe(messagelink = 'Enlace al mensaje', delay = 'Tiempo de espera antes de eliminar el mensaje')
    async def edit(self, interaction: discord.Interaction, messagelink:str, delay:float = None):
        try:
            link = messagelink.split('/')
            channel = self.bot.get_channel(int(link[-2]))
            message = await channel.fetch_message(int(link[-1]))
            await message.delete(delay = delay)
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Purge
    @app_commands.command(name = 'purge', description = 'Eliminar mensajes')
    @app_commands.describe(limit = 'Numero de mensajes')
    async def purge(self, interaction: discord.Interaction, limit: int = None):
        try:
            await interaction.channel.purge(limit=limit)
            return await interaction.response.send_message(content = f'🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):       
    await bot.add_cog(Message(bot), guild = discord.Object(id = guild_id))       