import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
from __init__ import guild_id, Cache

import urllib.request, json, datetime

class Minecraft(commands.GroupCog, name = 'minecraft'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.getserverstatus.start()

        super().__init__()

    def get_server_info(self, ip:str):
        with urllib.request.urlopen("https://api.mcsrvstat.us/2/" + ip) as url:
            requestdata = json.load(url)
            if requestdata['online'] == True:
                data = f"**Ip. {ip}**\nHost. `{requestdata['hostname']}`\nVersión. `{requestdata['version']}`\nJugadores. `{requestdata['players']['online']}` de `{requestdata['players']['max']}`"
            else:
                data = f"{requestdata['hostname']} is offline"
            return data

    @app_commands.command(name = 'status', description = 'Obtener el estatus de un server de minecraft')
    @app_commands.describe(ip = 'Ip del servidor')
    async def send(self, interaction: discord.Interaction, ip:str = Cache.hget('minecraft', 'serverip')):
        await interaction.response.send_message(content = f'🟢 {self.get_server_info(ip)}', ephemeral = True)

    #Revisar el estado del server.
    @tasks.loop(minutes=5)
    async def getserverstatus(self): 
        link = str(Cache.hget('messages', 'minecraft_status')).split('/')
        channel = self.bot.get_channel(int(link[-2]))
        message = await channel.fetch_message(int(link[-1]))
        await message.edit(content = f"{self.get_server_info(Cache.hget('minecraft', 'serverip'))}\nDynmap. {Cache.hget('minecraft', 'serverdynmap')}")
        
    @getserverstatus.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):  
    await bot.add_cog(Minecraft(bot), guild = discord.Object(id = guild_id))