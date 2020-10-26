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
    async def attack_target(self, ctx, *args):
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
        #Doesn't work for PvP -> Have to come up with something
        targetted_monster = getFactionMember(int(args[0]),1)
        if targetted_monster == None:
            return await ctx.send("There is no such target in this Instance.")
        message_to_display =mb.attack(battler,targetted_monster,0,targetted_monster, targetted_monster.getCharacter().name)
        print(message_to_display)
        await ctx.send("YOU DID A VERY POWERFUL ATTACK!")

def setup(bot):
    bot.add_cog(Battle_Commands(bot))    