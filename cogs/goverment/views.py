import discord
from discord.ext import commands

class Vote_view(discord.ui.View):
    def __init__(self) -> None:
        self.datavotes = dict()
        self.ciudadanoid = 1038518797021216809
        super().__init__(timeout = None)
    
    @discord.ui.select(
        custom_id = 'Vote',
        placeholder = 'Vote!',
        row = 2,
        options = [
            discord.SelectOption(label = 'Si', value = 'Aye', emoji = '✔'),
            discord.SelectOption(label = 'No', value = 'Nay', emoji = '✖'),
            discord.SelectOption(label = 'Nulo', value = 'Abs', emoji = '➖'),
        ],
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            
            if interaction.user.get_role(self.ciudadanoid) is not None:
                self.datavotes[interaction.user.id] = select.values
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)
        
    @discord.ui.button(label = "stop", style = discord.ButtonStyle.grey, custom_id = 'stopvote')
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.get_role(1020129264726712371) is not None:

                ciudadano = interaction.user.get_role(self.ciudadanoid)

                voteslist = list()
                for i in self.datavotes.values():
                    voteslist.append(i[0])

                aye = voteslist.count('Aye')
                nay = voteslist.count('Nay')
                abs = len(ciudadano.members)- aye - nay

                await interaction.channel.send(content = f'{aye} {nay} {abs} {voteslist}')
                return await interaction.response.send_message(content = '🟢', ephemeral = True)
            await interaction.response.send_message(content = '🔴', ephemeral = True)
        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True)
