import os
import discord
from discord import app_commands
from discord.ext import commands

class Thread(commands.GroupCog, name = 'thread'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    ##Thread
    #Create thread
    @app_commands.command(name = 'createthread', description = 'Create a thread')
    @app_commands.describe(name = 'Name of thread', archive_in_minutes = 'Time for archive', channel_id = 'Channel id to create thread')
    @app_commands.choices(archive_in_minutes = [
        app_commands.Choice(name="1 hora", value=60),
        app_commands.Choice(name="1 dia", value=1440),
        app_commands.Choice(name="3 dias", value=4320),
        app_commands.Choice(name="1 semana", value=10080),
        ])
    async def createthread(self, interaction: discord.Interaction, name: str, archive_in_minutes: int = None, channel_id: str = None):
        try:
            if archive_in_minutes == None: archive_in_minutes = interaction.channel.default_auto_archive_duration
            if channel_id == None: channel_id = interaction.channel.id
            Channel = interaction.guild.get_channel(int(channel_id))
            thread = await Channel.create_thread(name = name, message = None, type = discord.ChannelType.public_thread, auto_archive_duration = archive_in_minutes)
            return await interaction.response.send_message(content = f'🟢 <#{thread.id}>',ephemeral = True)
        except:
            await interaction.response.send_message(content = '🔴', ephemeral = True)
    
    #List forums
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
            post = await forum.create_thread(name = name, auto_archive_duration = archive_in_minutes, content = content)
            return await interaction.response.send_message(content = f'🟢 <#{post.thread.id}>', ephemeral = True)
        except:
            await interaction.response.send_message(content = '🔴', ephemeral = True)

async def setup(bot: commands.Bot):   
    await bot.add_cog(Thread(bot), guild = discord.Object(id = int(os.getenv('SERVERGUILD', '1018676558652776558'))))        