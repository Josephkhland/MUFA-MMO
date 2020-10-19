# bot.py
import os
import random
import mufa_constants as mconst
import mufadb
import mufa_world
import battle
import datetime
import character
import discord
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

@bot.command()
async def test2(ctx):
    battle.create()
    await ctx.send("Done")

@bot.command()
async def args(ctx, *args):
    messages = ""
    for a in args:
        messages += a + "|"
    await ctx.send(messages)

@bot.command()
async def register(ctx):
    guildID = ctx.message.guild.id
    user = ctx.author
    character.register(user.id, user.name, guildID, datetime.datetime.now())
    
@bot.command()
async def spawn(ctx, *args):
    userID = ctx.author.id
    if not character.checkRegistration(userID):
        return print ("Not registered Player")
    if len(args) <= 0:
        return print("Less Arguments than expected")
    player_entity = db.Player.get(id = userID)
    guildID = player_entity.guild_id
    if int(args[0]) <0 or int(args[0]) > len(player_entity.characters_list):
        return print("Invalid Argument")
    if int(args[0]) == 0 and len(args) < 2:
        return "Name must be provided"
    character.spawn(userID, args[1], player_entity.descendant_options[int(args[0])], guildID)
    await ctx.send("Done")
    
@bot.command()
async def show(ctx, user: discord.User):
    userID = user.id
    if user == None :
        userID = ctx.author.id
    await ctx.send(character.show(userID))
bot.run(TOKEN)

