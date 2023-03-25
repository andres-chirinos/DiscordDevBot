import os
import discord
from discord import app_commands
from discord.ext import commands
from __init__ import ServerId

class Thread(commands.GroupCog, name = 'thread'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    ##Thread
    #Create thread
    @app_commands.command(name = 'create', description = 'Crear un hilo')
    @app_commands.describe(name = 'Nombre', private = '¿Es privado?')
    async def create(self, interaction: discord.Interaction, name: str, private: bool = False):
        try:
            if private is True: private = discord.ChannelType.private_thread
            else: private = discord.ChannelType.public_thread
            thread = await interaction.channel.create_thread(name = name, type = private, invitable = False)
            return await interaction.response.send_message(content = f'🟢 <#{thread.id}>',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Delete thread
    @app_commands.command(name = 'delete', description = 'Eliminar un hilo')
    async def delete(self, interaction: discord.Interaction):
        try:
            await interaction.channel.delete()
            return await interaction.response.send_message(content = '🟢',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #add user thread
    @app_commands.command(name = 'add', description = 'Añadir un usuario')
    @app_commands.describe(user = 'Elija al usuario')
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await interaction.channel.add_user(user)
            return await interaction.response.send_message(content = f'🟢 {user.mention}',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #remove user thread
    @app_commands.command(name = 'remove', description = 'Quitar un usuario')
    @app_commands.describe(user = 'Elija al usuario')
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await interaction.channel.remove_user(user)
            return await interaction.response.send_message(content = f'🟢 {user.mention}',ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    """#List forums
    async def forum_autocomplete(self, interaction: discord.Interaction, current: str):
        forums = interaction.guild.forums
        return [app_commands.Choice(name = forum.name, value = str(forum.id)) for forum in forums]

    #Create Post
    @app_commands.command(name = 'createpost', description = 'Create a post')
    @app_commands.describe(name = 'Name of post', forumid = 'Forum to create post', archive_in_minutes = 'Time for archive')
    @app_commands.choices(archive_in_minutes=[
        app_commands.Choice(name="1 hora", value=60),
        app_commands.Choice(name="1 dia", value=1440),
        app_commands.Choice(name="3 dias", value=4320),
        app_commands.Choice(name="1 semana", value=10080),
        ])
    @app_commands.autocomplete(forumid = forum_autocomplete)
    async def createpost(self, interaction: discord.Interaction, name: str, forumid: str, content: str, archive_in_minutes: int = None):
        try:
            forum = interaction.guild.get_channel(int(forumid))
            if archive_in_minutes == None: archive_in_minutes = forum.default_auto_archive_duration
            post = await forum.create_thread(name = name, auto_archive_duration = archive_in_minutes, content = content, applied_tags=None)
            return await interaction.response.send_message(content = f'🟢 <#{post.thread.id}>', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)"""

async def setup(bot: commands.Bot):   
    await bot.add_cog(Thread(bot), guild = discord.Object(id = ServerId))        