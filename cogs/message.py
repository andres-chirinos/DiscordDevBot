import os
import discord
from discord import app_commands
from discord.ext import commands
from __init__ import guild_id, Cache

class Message(commands.GroupCog, name = 'message'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        super().__init__()
    
    def getmessagefromlink(self, messagelink:str):
        link = messagelink.split('/')
        channel = self.bot.get_channel(int(link[-2]))
        return channel.fetch_message(int(link[-1]))

    ##Message
    #Send
    @app_commands.command(name = 'send', description = 'Enviar un mensaje')
    @app_commands.describe(content = 'Contenido')
    async def send(self, interaction: discord.Interaction, content:str):
        await interaction.channel.send(content=content)
        return await interaction.response.send_message(content = '🟢',ephemeral = True)

    #Edit
    @app_commands.command(name = 'edit', description = 'Editar un mensaje')
    @app_commands.describe(messagelink = 'Enlace al mensaje', content = 'Nuevo contenido')
    async def edit(self, interaction: discord.Interaction, messagelink:str, content:str):
        message = await self.getmessagefromlink(messagelink)
        await message.edit(content = content)   
        return await interaction.response.send_message(content = '🟢',ephemeral = True)

    #Delete
    @app_commands.command(name = 'delete', description = 'Eliminar un mensaje')
    @app_commands.describe(messagelink = 'Enlace al mensaje', delay = 'Tiempo de espera antes de eliminar el mensaje')
    async def delete(self, interaction: discord.Interaction, messagelink:str, delay:float = None):
        message = await self.getmessagefromlink(messagelink)
        await message.delete(delay = delay)
        return await interaction.response.send_message(content = '🟢',ephemeral = True)

    #Purge
    @app_commands.command(name = 'purge', description = 'Eliminar mensajes')
    @app_commands.describe(limit = 'Numero de mensajes')
    async def purge(self, interaction: discord.Interaction, limit: int = None):
        await interaction.channel.purge(limit=limit)
        return await interaction.response.send_message(content = f'🟢',ephemeral = True)

async def setup(bot: commands.Bot):       
    await bot.add_cog(Message(bot), guild = discord.Object(id = guild_id))       