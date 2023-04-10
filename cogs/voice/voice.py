import os
import discord
from discord import app_commands
from discord.ext import commands
from __init__ import guild_id, Cache

from gtts import gTTS

class Voice(commands.GroupCog, name = 'voice'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voiceclient = None

        super().__init__()

    ##Create Voice
    #Create a voice channel on join in
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            print(f'{member} has joined the vc')

    ##Voice Handling
    #Join a voice channel
    @app_commands.command(name = 'join', description = 'Unirse a un canal')
    @app_commands.describe(channel = '¿Cual canal?')
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel = None):
        try:
            if self.voiceclient is None and (channel is not None or interaction.user.voice is not None):
                if channel is None: channel = interaction.user.voice.channel
                self.voiceclient = await channel.connect(self_deaf=True)
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Leave a voice channel
    @app_commands.command(name = 'leave', description = 'Salir del canal')
    async def leave(self, interaction: discord.Interaction):
        try:
            if self.voiceclient is not None:
                self.voiceclient = await self.voiceclient.disconnect()
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Text to speech command
    @app_commands.command(name = 'gtts', description = 'Escritura a voz')
    @app_commands.describe(text = '¿Contenido a leer?', language = '¿Idioma (langcode desde google docs)?', slow = '¿Velocidad de lectura?')
    async def gtts(self, interaction: discord.Interaction, text: str, language: str = 'es', slow: bool = False):
        try:
            if self.voiceclient is not None:
                gTTS(text = text, lang = language, slow = slow).save('cogs/voice/voice.mp3')
                self.voiceclient.play(source = discord.FFmpegPCMAudio(source = 'cogs/voice/voice.mp3'))
                return await interaction.response.send_message(content = '🟢')
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Text to speech listener
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.voiceclient is not None and message.channel.id is self.voiceclient.channel.id and message.author.id is not self.bot.user.id:
            gTTS(text = message.content, lang = 'es', slow = False).save('cogs/voice/voice.mp3')
            self.voiceclient.play(source = discord.FFmpegPCMAudio(source = 'cogs/voice/voice.mp3'))

async def setup(bot: commands.Bot):   
    await bot.add_cog(Voice(bot), guild = discord.Object(id = guild_id))        