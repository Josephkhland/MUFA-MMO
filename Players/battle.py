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
        targetted_monster = node.getMember_not_in_faction(int(args[0]),battler.faction)
        if targetted_monster == None:
            return await ctx.send("There is no such target in this Instance.")
        message_to_display =mb.attack(battler,targetted_monster, targetted_monster.getCharacterInNode(node.node_id).name, 0)
        print(message_to_display)
        await ctx.send("YOU DID A VERY POWERFUL ATTACK!")
        
    @commands.command(name='enemies')
    async def show_enemies(self, ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if not isinstance(node, db.Battle): 
            return await ctx.send("You can only use this command in a Battle.")
        enemies = node.getEnemies_of_faction(battler.faction)
        
        embedList = mdisplay.display_battle_members(enemies, node.node_id)
        totalTabs = len(embedList)
        c_t = 0
        msg = await ctx.send(embed = embedList[0])
        if totalTabs > 1:
            loop = True
            previous_tab = '◀️'
            next_tab = '▶️'
            await msg.add_reaction(previous_tab)
            await msg.add_reaction(next_tab)
            def reaction_filter(reaction, user):
                return str(user.id) == str(ctx.author.id) and str(reaction.emoji) in [previous_tab,next_tab]
            while loop:
                try:
                    pending_collectors =[self.bot.wait_for('reaction_add', timeout=5, check = reaction_filter),
                                         self.bot.wait_for('reaction_remove', timeout=5, check = reaction_filter)]                  
                    done_collectors, pending_collectors = await asyncio.wait(pending_collectors, return_when=asyncio.FIRST_COMPLETED)
                    for collector in pending_collectors:
                        collector.cancel()
                    for collector in done_collectors:
                        reaction, user = await collector
                    if reaction.emoji == next_tab:
                        c_t = (c_t+1) % totalTabs
                    elif reaction.emoji == previous_tab:
                        c_t = (c_t-1) 
                        if c_t <0: 
                            c_t = totalTabs -1
                    msg.edit(embed = embedList[c_t])
                except asyncio.TimeoutError:
                    await msg.add_reaction('💤')
                    loop = False
                    
        

def setup(bot):
    bot.add_cog(Battle_Commands(bot))    