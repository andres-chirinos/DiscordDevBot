import os
import discord
from discord import app_commands
from discord.ext import commands

from __init__ import ServerId

class Register_modal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = 'Registro', custom_id = 'register_modal', timeout = None)

        self.foreignroleid = 1038518544012431390

        self.nick = discord.ui.TextInput(label = 'Nick de minecraft', placeholder = 'Steve', min_length = 3, max_length = 16, required = True)
        self.add_item(self.nick)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if len(interaction.user.roles)==1:
                role = interaction.user.guild.get_role(self.foreignroleid)
                await interaction.user.edit(nick = str(self.nick), roles = [role], reason = 'Registro')
            else:
                await interaction.user.edit(nick = str(self.nick), reason = 'Actualización')
            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

class Register_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "Registro", style = discord.ButtonStyle.red, custom_id = 'register_view')
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(Register_modal())
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

class Register(commands.GroupCog, name = 'register'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.foreignroleid = 1038518544012431390
        self.inviteroleid = 1058390264588292199

        super().__init__()
    
    #Para registrarse
    @app_commands.command(name = 'user', description = 'Registro manual')
    async def register(self, interaction: discord.Interaction, user: discord.Member, nick:str): 
        try:
            if len(user.roles)==1:
                role = user.guild.get_role(self.foreignroleid)
                await user.edit(nick = nick, roles = [role], reason = 'Registro')
            else:
                await user.edit(nick = nick, reason = 'Actualización')

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Para poner boton de registro
    @app_commands.command(name = 'set', description = 'Poner boton de registro')
    async def registerbutton(self, interaction: discord.Interaction): 
        try:
            message = await interaction.channel.send(view = Register_view())

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):
    bot.add_view(Register_view())
    await bot.add_cog(Register(bot), guild = discord.Object(id = ServerId))        