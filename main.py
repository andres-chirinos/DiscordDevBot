import os
import discord
from discord.ext import commands
import asyncio
from quart import Quart

#Variables / Test bot values
Prefix = os.getenv('PREFIX', '|')
Port = int(os.getenv('PORT', '80'))
ApplicationId = int(os.getenv('APPID', '1031315927679123637'))
ServerId = int(os.getenv('SERVERGUILD', '1018676558652776558'))
Token = os.getenv('TOKEN', 'MTAzMTMxNTkyNzY3OTEyMzYzNw.GEEof1.zynT3R5CcMLm7hI08fW9D_9KKyOOU3Qg_uVnko')
Description = os.getenv('DESC', 'Prueba controlada sin variable')

class MyBot(commands.Bot):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.initial_extensions = [
            'cogs.voice.voice',
            'cogs.webhook',
            'cogs.thread',
            'cogs.register',
            'cogs.message',
            'cogs.minecraft',
        ]
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild = discord.Object(id = ServerId)) 

    async def close(self):
        await super().close()

    async def on_ready(self):
        await bot.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game(f'[{Prefix}] {Description}'))
        print(f'{self.user} has connected to Discord!') 

    async def on_command_error(self, context, exception):
        print(f"[Error] {context.message.author} {exception}")
        await context.send(f'{exception}')

app = Quart(__name__)
bot = MyBot(command_prefix = commands.when_mentioned_or(Prefix), help_command = None, case_insensitive = True, description = Description, intents = discord.Intents.all(), aplicaction_id = ApplicationId)

@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login(Token) #bot.run(token = Token)
    loop.create_task(bot.connect())

@app.route('/')
async def homepage():
    return 'Homepage'
    
@app.route("/send", methods=["GET"])
async def send_message():
    # wait_until_ready and check for valid connection is missing here
    channel = bot.get_channel(1018683741893312583)
    await channel.send('XYZz')
    return 'OK', 200


app.run(host = '0.0.0.0',debug = True, port = Port)#, use_reloader = False)