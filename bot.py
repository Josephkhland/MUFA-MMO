# bot.py
import os
import random
import mufa_constants as mconst
import mufadb
import mufa_world
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# 1
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

bot.run(TOKEN)

