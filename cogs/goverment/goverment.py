import discord
from discord import app_commands
from discord.ext import commands

from __init__ import ServerId

class Meeting_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
    
    @discord.ui.button(label = "Solicitar", style = discord.ButtonStyle.red, custom_id = 'request_meeting')
    async def Solicitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            interaction.channel.slowmode_delay
            interaction.message.author = interaction.user
            bucket = self.cooldown.get_bucket(interaction.message)
            retry = bucket.update_rate_limit()
            if not retry:

                return await interaction.response.send_modal(Meeting_modal())

            await interaction.response.send_message(content = f'🔴 Please wait {round(retry)}s.', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

class Meeting_modal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = 'Solicitud a reunión', custom_id = 'meeting_modal', timeout = None)
        self.reason = discord.ui.TextInput(label = 'Pais u Organización', placeholder = 'ONU / Groenlandia * si no tiene dejar en blanco', min_length = 3, max_length = 20, required = False)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if interaction.user.nick is None: reason = interaction.user.name
            else: reason = interaction.user.nick
            thread = await interaction.channel.create_thread(name = f'{reason}', type = discord.ChannelType.private_thread, invitable = False)
            #await thread.add_user(interaction.user)
            await thread.send(content = f'Bienvenido {interaction.user.mention}, presentese por favor.')
            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

class Goverment(commands.GroupCog, name = 'goverment'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        super().__init__()

    #Poner boton para solicitar una misión
    @app_commands.command(name = 'meeting', description = 'set a request meeting message')
    async def meeting(self, interaction: discord.Interaction): 
        try: 
            await interaction.channel.send(content = 'Para solicitar una reunión', view = Meeting_view())

            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

async def setup(bot: commands.Bot):
    bot.add_view(Meeting_view())
    await bot.add_cog(Goverment(bot), guild = discord.Object(id = ServerId))        