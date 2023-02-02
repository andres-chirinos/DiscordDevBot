import discord

class MyModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = 'Modal', custom_id = 'Modal',timeout = None)
        self.nickname = discord.ui.TextInput(label = 'Minecraft nick', placeholder = 'Diandrewun', min_length = 4, max_length = 16)
        self.add_item(self.nickname)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.edit(nick = f'{self.nickname.value}')
        #await interaction.response.send_message(content = f'🟢 {self.nickname.value}', ephemeral = True)