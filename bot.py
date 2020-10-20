# bot.py
import os
import random
import mufa_constants as mconst
import mufadb as db
import mufa_world
import battle
import datetime
import character
import discord
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
import sys, traceback
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
# 2
#bot = commands.Bot(command_prefix='!')
def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['!', 'm!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ! to be used in DMs
        return '!'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)
# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['Players.navigation']

bot = commands.Bot(command_prefix=get_prefix)

# Here we load our extensions listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
     # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name="Multiple Unidentified Futures Anthem"))
    print(f'Successfully logged in and booted...!')
    
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
    character.register(str(user.id), user.name, str(guildID), datetime.datetime.now())
    
@bot.command()
async def spawn(ctx, *args):
    userID = str(ctx.author.id)
    if not character.checkRegistration(userID):
        return print ("Not registered Player")
    if len(args) <= 0:
        return print("Less Arguments than expected")
    player_entity = db.Battler.objects.get(identification = userID)
    guildID = player_entity.guild_id
    if int(args[0]) <0 or int(args[0]) > len(player_entity.characters_list):
        return print("Invalid Argument")
    if int(args[0]) == 0 and len(args) < 2:
        return "Name must be provided"
    character.spawn(userID, args[1], player_entity.descendant_options[int(args[0])], guildID)
    await ctx.send("Done")
    
@bot.command()
async def show(ctx, user: discord.User = None):
    userID = str(ctx.author.id)
    if user != None :
        userID = str(user.id)
    await ctx.channel.send(embed=character.show(userID))
bot.run(TOKEN, bot=True, reconnect=True)

