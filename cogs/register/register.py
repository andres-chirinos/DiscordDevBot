import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get

from __init__ import ServerId
from cogs.register.views import Vote_view, Mission_view

import datetime

class Register(commands.GroupCog, name = 'register'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.foreignroleid = 1038518544012431390
        self.permitmessageid = 1070020430737440778
        self.emojicheck = '🔴'

        self.inviteroleid = 1058390264588292199

        self.assemblyforumid = 1035706603741138964

        self.grantinvite.start()

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
    async def grantinvite(self):
        members = self.bot.guilds[0].members
        now = datetime.datetime.now()
        for member in members:
            if member is not self.bot and member.get_role(self.foreignroleid) is not None and int(member.joined_at.timestamp()) + 604800 <= int(now.timestamp()):
                role = member.guild.get_role(self.inviteroleid)
                await member.add_roles(role)

    @grantinvite.before_loop
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
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #OnRegisterPostAdd
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == self.assemblyforumid:
            await thread.send(content = f'🟢 <@&1038518797021216809> <@&1055590689666252850>')

    #Para votar el post
    @app_commands.command(name = 'vote', description = 'create a vote')
    async def createvote(self, interaction: discord.Interaction): 
        try:
            message = await interaction.channel.send(content = '<@&1038518797021216809.> __Votación__', view = Vote_view())

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)
    
    #Para poner el solicitar una mision
    @app_commands.command(name = 'mision', description = 'create a mision')
    async def createmision(self, interaction: discord.Interaction): 
        try: 
            await interaction.channel.send(content = 'Para solicitar una misión diplomatica', view = Mission_view())

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):
    bot.add_view(Vote_view())
    await bot.add_cog(Register(bot), guild = discord.Object(id = ServerId))        