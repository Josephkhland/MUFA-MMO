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
    
@bot.event
async def on_guild_join(guild):
    print ("New Guild joined")
    mufa_world.insert_guild(str(guild.id))

@bot.event    
async def on_guild_remove(guild):
    print ("Guild Left!")
    mufa_world.remove_guild(str(guild.id))
    
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def test(ctx):
    n_list = mufa_world.visualize()
    msg_to_send = "```"
    for i in range(5):
        for j in range(5):
            msg_to_send += str(n_list[i*5 + j])
        msg_to_send += "\n"
        
    msg_to_send += "```"
    await ctx.send(msg_to_send)

bot.run(TOKEN)

