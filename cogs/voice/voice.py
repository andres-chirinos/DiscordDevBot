import os
import discord
from discord import app_commands
from discord.ext import commands

from gtts import gTTS

class Voice(commands.GroupCog, name = 'voice'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voiceclient = None

        super().__init__()

    ##Voice Handling
    #Join a voice channel
    @app_commands.command(name = 'join', description = 'Join a voice channel')
    @app_commands.describe(channel = 'Channel to join')
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel = None):
        if self.voiceclient is None and (channel is not None or interaction.user.voice is not None):
            if channel is None: channel = interaction.user.voice.channel
            self.voiceclient = await channel.connect(self_deaf=True)
            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        await interaction.response.send_message(content = '🔴', ephemeral = True)
        
    #Leave a voice channel
    @app_commands.command(name = 'leave', description = 'Leave a voice channel')
    async def leave(self, interaction: discord.Interaction):
        if self.voiceclient is not None:
            self.voiceclient = await self.voiceclient.disconnect()
            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        await interaction.response.send_message(content = '🔴', ephemeral = True)
    
    #Text to speech command
    @app_commands.command(name = 'gtts', description = 'Text to speech in a voice channel')
    @app_commands.describe(text = 'Text to be converted to voice', language = 'Language of text (langcode from google docs)', slow = 'Play more slow the text voice')
    async def gtts(self, interaction: discord.Interaction, text: str, language: str = 'es', slow: bool = False):
        if self.voiceclient is not None:
            gTTS(text = text, lang = language, slow = slow).save('cogs/voice/voice.mp3')
            self.voiceclient.play(source = discord.FFmpegPCMAudio(source = 'cogs/voice/voice.mp3'))
            return await interaction.response.send_message(content = '🟢')
        await interaction.response.send_message(content = '🔴', ephemeral = True)

    #Text to speech listener
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.voiceclient is not None and message.channel.id is self.voiceclient.channel.id and message.author.id is not self.bot.user.id:
            gTTS(text = message.content, lang = 'es', slow = False).save('cogs/voice/voice.mp3')
            self.voiceclient.play(source = discord.FFmpegPCMAudio(source = 'cogs/voice/voice.mp3'))

async def setup(bot: commands.Bot):   
    await bot.add_cog(Voice(bot), guild = discord.Object(id = int(os.getenv('SERVERGUILD', '1018676558652776558'))))        