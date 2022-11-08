import os
import discord
from discord.ext import commands

#Variables / Test bot values
Prefix = os.getenv('PREFIX', '|')
ApplicationId = int(os.getenv('APPID', '1031315927679123637'))
ServerId = int(os.getenv('SERVERGUILD', '1018676558652776558'))
Token = os.getenv('TOKEN', 'MTAzMTMxNTkyNzY3OTEyMzYzNw.GEEof1.zynT3R5CcMLm7hI08fW9D_9KKyOOU3Qg_uVnko')
Description = 'Test bot description'

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix = commands.when_mentioned_or(Prefix), help_command = None, case_insensitive = True, description = Description, intents = discord.Intents.all(), aplicaction_id = ApplicationId)

        self.initial_extensions = [
            'cogs.voice',
            'cogs.webhook',
            'cogs.thread',
        ]
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild = discord.Object(id = ServerId)) 

    async def close(self):
        await super().close()

    async def on_ready(self):
        await bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(f'[{Prefix}] Sustentando al gobierno de Dinamarca'))
        print(f'{self.user} has connected to Discord!') 

    async def on_command_error(self, context, exception):
        print(f"[Error] {context.message.author} {exception}")
        await context.send(f'{exception}')

bot = MyBot()
bot.run(token = Token)
