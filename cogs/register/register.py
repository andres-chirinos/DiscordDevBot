import discord
from discord import app_commands
from discord.ext import commands

from __init__ import ServerId
from cogs.register.passport import passport
#from PIL import Image, ImageDraw, ImageFont
#from io import BytesIO
#from datetime import datetime

class Register_modal(discord.ui.Modal):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        super().__init__(title = 'Registro', custom_id = 'register_modal', timeout = None)

        self.foreignroleid = 1038518544012431390
        self.documentationchannelid = 1090382813481668739

        self.nick = discord.ui.TextInput(label = 'Nick de minecraft', placeholder = 'Steve', min_length = 3, max_length = 16, required = True)
        self.add_item(self.nick)

        self.gender = discord.ui.TextInput(label = 'Genero', placeholder = 'M/F', max_length = 1, required = True)
        self.add_item(self.gender)

        self.place = discord.ui.TextInput(label = 'Nacionalidad', min_length = 3, max_length = 16, required = True)
        self.add_item(self.place)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            
            if len(interaction.user.roles)==1:
                role = interaction.user.guild.get_role(self.foreignroleid)
                await interaction.user.edit(nick = str(self.nick), roles = [role], reason = 'Registro')
            else:
                await interaction.user.edit(nick = str(self.nick), reason = 'Actualización')

            if not interaction.user.get_role(self.foreignroleid):
                await interaction.response.defer(ephemeral = True, thinking = True)
                
                file = await passport(interaction=interaction, user=interaction.user, nick=self.nick, gender=self.gender, place=self.place)
                channel = self.bot.get_channel(self.documentationchannelid)
                await channel.send(content = interaction.user.mention, file = file)

            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

class Register_view(discord.ui.View):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        super().__init__(timeout = None)

    @discord.ui.button(label = "Registro", style = discord.ButtonStyle.red, custom_id = 'register_view')
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_modal(Register_modal(self.bot))
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

class Register(commands.GroupCog, name = 'register'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.foreignroleid = 1038518544012431390
        self.inviteroleid = 1058390264588292199

        self.documentationchannelid = 1090382813481668739

        super().__init__()
    
    #Para registrarse
    @app_commands.command(name = 'user', description = 'Registro manual')
    @app_commands.describe(user = 'Elija al usuario', nick = 'Ponga su nick', gender = 'Elija su genero', place = 'De donde es?')
    @app_commands.choices(gender=[
        app_commands.Choice(name="Masculino", value='M'),
        app_commands.Choice(name="Femenino", value='F'),
        ])
    async def register(self, interaction: discord.Interaction, user: discord.Member, nick:str, gender:str, place:str): 
        try:
            if len(user.roles)==1:
                role = user.guild.get_role(self.foreignroleid)
                await user.edit(nick = nick, roles = [role], reason = 'Registro')
            else:
                await user.edit(nick = nick, reason = 'Actualización')

            if not interaction.user.get_role(self.foreignroleid):
                await interaction.response.defer(ephemeral = True, thinking = True)
                
                file = await passport(interaction=interaction, user=user, nick=nick, gender=gender, place=place)
                channel = self.bot.get_channel(self.documentationchannelid)
                await channel.send(content = user.mention, file = file)

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

    #Para poner boton de registro
    @app_commands.command(name = 'set', description = 'Poner boton de registro')
    async def registerbutton(self, interaction: discord.Interaction): 
        try:
            message = await interaction.channel.send(view = Register_view(self.bot))

            return await interaction.response.send_message(content = '🟢', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

async def setup(bot: commands.Bot):
    bot.add_view(Register_view(bot))
    await bot.add_cog(Register(bot), guild = discord.Object(id = ServerId))        