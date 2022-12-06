import os
import discord
from discord import app_commands
from discord.ext import commands

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
        except:
            await interaction.response.send_message(content = '🔴', ephemeral = True)

async def setup(bot: commands.Bot):   
    await bot.add_cog(Message(bot), guild = discord.Object(id = int(os.getenv('SERVERGUILD', '1018676558652776558'))))        