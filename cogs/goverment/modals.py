import discord

class Register_modal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = 'Registro', custom_id = 'register_modal', timeout = None)

        self.foreignroleid = 1038518544012431390

        self.nick = discord.ui.TextInput(label = 'Nick de minecraft', placeholder = 'Diandrewun', min_length = 3, max_length = 16, required = True)
        self.add_item(self.nick)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.nick = str(self.nick)
            role = interaction.user.guild.get_role(self.foreignroleid)
            await interaction.user.edit(nick = self.nick, roles = [role])
            return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

        except Exception as expt:
            await interaction.response.send_message(content = f'🟥 {expt}', ephemeral = True, delete_after = 30)