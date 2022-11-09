import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get

import datetime

class Register(commands.GroupCog, name = 'register'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.foreignroleid = 1038518544012431390
        self.permitmessageid = 1038536205878439966
        self.emojicheck = '🔴'

        self.nationalroleid = 1038518797021216809

        self.asemblyforumid = 1035706603741138964

        self.grantnational.start()

        super().__init__()

    #Para aceptar el permiso de entrada
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = get(self.bot.get_all_members(), id = payload.user_id)
        if member and member.id != self.bot.application_id and payload.message_id == self.permitmessageid and payload.emoji.name == self.emojicheck:
            role = member.guild.get_role(self.foreignroleid)
            await member.edit(roles=[role])
    
    #Para rechazar el permiso de entrada
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = get(self.bot.get_all_members(), id = payload.user_id)
        if member and member.id != self.bot.application_id and payload.message_id == self.permitmessageid and payload.emoji.name == self.emojicheck:
            await member.edit(roles=[])

    #Para adquirir la nacionalidad por naturalización.
    @tasks.loop(hours=24)
    async def grantnational(self):
        members = self.bot.guilds[0].members
        now = datetime.datetime.now()
        for member in members:
            if member is not self.bot and member.get_role(self.foreignroleid) is not None and int(member.joined_at.timestamp()) + 604800 <= int(now.timestamp()):
                role = member.guild.get_role(self.nationalroleid)
                await member.edit(roles=[role])

    @grantnational.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

    #Para adquirir un cargo/nacionalidad/permiso
    @app_commands.command(name = 'ascend', description = 'ascend a new role')
    @app_commands.describe(member = 'Member to ascend', role = 'Role to give', advice = 'Advice the ascend')
    async def ascend(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role, advice: bool = False): 
        try:
            await member.add_roles(role)
            if advice is True:
                await interaction.channel.send(content = f'Se ascendió a <@!{member.id}> al cargo de <@&{role.id}>')
            return await interaction.response.send_message(content = f'🟢 Ascendiste a <@!{member.id}>', ephemeral = True)
        except:
            await interaction.response.send_message(content = '🔴', ephemeral = True)

    #OnRegisterEnterpriceAdd
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == self.asemblyforumid:
            print(thread)
            await thread.send(content = f'🟢 <#{thread.id}> registrada')

async def setup(bot: commands.Bot):  
    await bot.add_cog(Register(bot), guild = discord.Object(id = int(os.getenv('SERVERGUILD', '1018676558652776558'))))        