# bot.py
import os
import random
import mufa_constants as mconst
import mufadb as db
import mufa_world
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
initial_extensions = ['Players.navigation',
                      'Players.profile',
                      'Players.interact',
                      'Players.battle',
                      'Guild.settings',
                      'Guild.actions',
                      'Moderator.initialization']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents =intents)

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
    mufa_world.insert_guild(str(guild.id), guild.name)

@bot.event    
async def on_guild_remove(guild):
    print ("Guild Left!")
    mufa_world.remove_guild(str(guild.id))
    
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def register(ctx):
    guildID = ctx.message.guild.id
    user = ctx.author
    character.register(str(user.id), user.name, str(guildID), datetime.datetime.now())
    
@bot.command()
async def spawn(ctx, *args):
    userID = str(ctx.author.id)
    if not character.checkRegistration(userID):
        return await ctx.send("You are not a registered Player")
    if len(args) <= 0:
        return await ctx.send("Less Arguments than expected")
    player_entity = db.Battler.objects.get(battler_id = userID)
    if len(player_entity.characters_list) >= player_entity.maxCharacters():
        return await ctx.send("Can't have more than 6 characters. If you still want to create a new one, you will have to abandon one of your current characters.")
    guildID = player_entity.guild_id
    if int(args[0]) <0 or int(args[0]) > len(player_entity.characters_list):
        return await ctx.send("Invalid Argument")
    if int(args[0]) == 0 and len(args) < 2:
        return await ctx.send("Name must be provided")
    if len(args[1]) >24:
        return await ctx.send("Name bigger than allowed. Name mustn't exceed 24 characters")
    character.spawn(userID, args[1], player_entity.descendant_options[int(args[0])], guildID)
    await ctx.send("Done")

@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title = "About MUFA",
        description = "Powered by Josephkhland",
        colour = discord.Colour.blue()
    )
    embed.add_field(name="Help us Expand?", value = "[Invite MUFA](https://discord.com/api/oauth2/authorize?client_id=704732201199206420&permissions=8&scope=bot) to your Server", inline = False)
    await ctx.send(embed = embed)

bot.run(TOKEN, bot=True, reconnect=True)

