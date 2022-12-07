import os
import discord
from discord import app_commands
from discord.ext import commands, tasks

import urllib.request, json, datetime

class Minecraft(commands.GroupCog, name = 'minecraft'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.serverchannelid = 1048249292122501141
        self.servermessageid = 1049759166132133969

        self.getserverstatus.start()

        super().__init__()

    def get_server_info(self, ip:str = "mc.tricraft.gq"):
        with urllib.request.urlopen("https://api.mcsrvstat.us/2/" + ip) as url:
            requestdata = json.load(url)
            if requestdata['online'] == True:
                data = f"{requestdata['hostname']} is online {requestdata['players']['online']}/{requestdata['players']['max']}"
            else:
                data = f"{requestdata['hostname']} is offline"
            return f"{data}, updated in <t:{round(datetime.datetime.now().timestamp())}>"

    @app_commands.command(name = 'serverstatus', description = 'Get a Minecraft server status')
    @app_commands.describe(ip = 'IP of server')
    async def send(self, interaction: discord.Interaction, ip:str):
        await interaction.response.send_message(content = f'🟢 {self.get_server_info(ip)}',ephemeral = True)

    #Revisar el estado del server.
    @tasks.loop(minutes=5)
    async def getserverstatus(self): 
        channel = self.bot.get_channel(self.serverchannelid)
        message = await channel.fetch_message(self.servermessageid)
        await message.edit(content = self.get_server_info())
        
    @getserverstatus.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):  
    await bot.add_cog(Minecraft(bot), guild = discord.Object(id = int(os.getenv('SERVERGUILD', '1018676558652776558'))))        