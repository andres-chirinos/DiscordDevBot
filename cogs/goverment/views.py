import discord
from discord.ext import commands
    
class Vote_view(discord.ui.View):
    def __init__(self) -> None:
        self.datavotes = dict()
        super().__init__(timeout = None)
    
    @discord.ui.select(
        custom_id = 'Vote',
        placeholder = 'Vote!',
        row = 2,
        options = [
            discord.SelectOption(label = 'Aye', value = 'Aye', emoji = '✔'),
            discord.SelectOption(label = 'Nay', value = 'Nay', emoji = '✖'),
            discord.SelectOption(label = 'Abs', value = 'Abs', emoji = '➖'),
        ],
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.get_role(1038518797021216809) is not None:
                self.datavotes[interaction.user.id] = select.values
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)
        
    @discord.ui.button(label = "stop", style = discord.ButtonStyle.grey, custom_id = 'stopvote')
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.get_role(1020129264726712371) is not None:
                await interaction.channel.send(content = f'{self.datavotes.values()}')
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)
        