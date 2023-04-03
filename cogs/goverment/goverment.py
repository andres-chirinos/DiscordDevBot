from __init__ import guild_id, Cache

import discord
from discord import app_commands
from discord.ext import commands

class Meeting_modal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = 'Solicitud a reunión', custom_id = 'meeting_modal', timeout = None)
        self.reason = discord.ui.TextInput(label = 'Pais', min_length = 3, max_length = 20, required = False)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if interaction.user.nick is None: reason = interaction.user.name
            else: reason = interaction.user.nick
            thread = await interaction.channel.create_thread(name = f'{reason}', type = discord.ChannelType.private_thread, invitable = False)
            await thread.add_user(interaction.user)
            #await thread.send(content = f'Bienvenido {interaction.user.mention}, presentese por favor.')
            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

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

                await interaction.response.send_modal(Meeting_modal())
                """if interaction.user.nick is None: reason = interaction.user.name
                else: reason = interaction.user.nick
                thread = await interaction.channel.create_thread(name = f'{reason}', type = discord.ChannelType.private_thread, invitable = False)
                await thread.send(content = f'Bienvenido {interaction.user.mention}, presentese por favor.')
                return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)"""

            await interaction.response.send_message(content = f'🔴 Please wait {round(retry)}s.', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)

class Goverment(commands.GroupCog, name = 'goverment'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    #Poner boton para solicitar una misión
    @app_commands.command(name = 'meeting', description = 'Boton para poder pedir una reunión')
    async def meeting(self, interaction: discord.Interaction): 
        try: 
            await interaction.channel.send(content = 'Para solicitar una reunión', view = Meeting_view())

            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)

    #Mencionar al hacer una propuesta
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == int(Cache.hget('channels', 'parlamentforum_id')):
            await thread.send(content = f"🟢 <@&{int(Cache.hget('roles', 'ciudadano_id'))}>")

async def setup(bot: commands.Bot):
    bot.add_view(Meeting_view())
    await bot.add_cog(Goverment(bot), guild = discord.Object(id = guild_id))        