import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import mufabattle as mb
import character
import discord
import asyncio
from discord.ext import commands

class Battle_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='attack')
    async def attack_cool(self, ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        if len(args) == 0 or len(args) >1:
            return await ctx.send("Invalid number of arguments.")
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if not isinstance(node, db.Battle): 
            return await ctx.send("You can only use this command in a Battle.")
        await ctx.send("YOU DID A VERY POWERFUL ATTACK!")

def setup(bot):
    bot.add_cog(Battle_Commands(bot))    