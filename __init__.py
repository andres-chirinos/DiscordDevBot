import os
import discord
from discord.ext import commands
import asyncio
from quart import Quart

import logging
from logging.config import dictConfig

#Variables
Prefix = os.getenv('PREFIX', '|')
Port = int(os.getenv('PORT', '80'))
ApplicationId = int(os.getenv('APPID', '1031315927679123637'))
ServerId = int(os.getenv('SERVERGUILD', '1018676558652776558'))
Token = os.getenv('TOKEN', 'MTAzMTMxNTkyNzY3OTEyMzYzNw.GEEof1.zynT3R5CcMLm7hI08fW9D_9KKyOOU3Qg_uVnko')
Description = os.getenv('DESC', 'Prueba controlada sin variable')

#Setting a bot 
class MyBot(commands.Bot):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.initial_extensions = [
            'cogs.voice.voice',
            'cogs.webhook',
            'cogs.thread',
            'cogs.goverment.goverment',
            'cogs.register.register',
            'cogs.message',
            #'cogs.minecraft',
        ]
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild = discord.Object(id = ServerId)) 

    async def close(self):
        await super().close()

    async def on_ready(self):
        await bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(f'[{Prefix}] {Description}'))

    async def on_command_error(self, context, exception):
        await context.send(f'{exception}')

    async def on_error(self, event_method):
        return await super().on_error(event_method)

#setup website
app = Quart(__name__, root_path='pages')

from pages.webmain import webmain
app.register_blueprint(webmain, url_prefix = '/')

bot = MyBot(command_prefix = commands.when_mentioned_or(Prefix), help_command = None, case_insensitive = True, description = Description, intents = discord.Intents.all(), aplicaction_id = ApplicationId)

#website start bot and periodic reflesh it
@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login(Token) 
    loop.create_task(bot.connect(), name = 'Bot refresh')

#Startup
if __name__ == '__main__':
    #logFormatter = logging.Formatter(fmt=' %(name)-8s - %(levelname)-8s - %(message)s')
    #discord.utils.setup_logging(level = logging.INFO, formatter = logFormatter)
    dictConfig({
        'version': 1,
        'loggers': {
            'quart.app': {
                'level': 'INFO',
                'formatter' : ' %(name)-8s - %(levelname)-8s - %(message)s',
            },
            'discord':{
                'level': 'INFO',
                'formatter' : ' %(name)-8s - %(levelname)-8s - %(message)s',
            }
        },
    })
    
    #app.run(debug=True)
    app.run(host = '0.0.0.0', port = Port)

