import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import mufabattle as mb
import mufa_item_management as mim
import character
import discord
import asyncio
from discord.ext import commands

class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='challenge')
    async def challenge_to_battle(self, ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        if len(args) == 0 or len(args) >1:
            return await ctx.send("Invalid number of arguments.")
        try:
            monster = db.Monster.objects.get(battler_id = args[0])
        except:
            return await ctx.send("'"+args[0]+"' is not a valid monster.")
        try:
            battler = db.Player.objects.get(battler_id = str(ctx.author.id))
            pCharac = battler.getCharacter()
            node = pCharac.getInstance()
            if not monster in node.members:
               return await ctx.send("The monster with the given ID is not in the same instance as you. It's possible that another user challenged this monster first, or you have typed it's ID wrong.")
        except:
            return await ctx.send("An unexpected error has occured.")
        mb.create(monster.battler_id, 1,battler)
        mb.battle_add_member(monster.battler_id, monster)
        embed = mb.battle_add_member(monster.battler_id, battler)
        await ctx.send(embed = embed)
    
    @commands.command(name='escape')
    async def escape_from_battle(self, ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if isinstance(node, db.Battle):
            embed = mb.battle_member_leaves(battler)
            await ctx.send("You have succesfully escaped!", embed = embed)
        else:
            await ctx.send("The !escape command can only be used to leave from a battle")
    
    @commands.command(name='buy')
    @commands.guild_only()
    async def buy_object_from_guild_shop(self,ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if node.guild_id != str(ctx.guild.id):
            return await ctx.send("Your currently active character is not in this Guild's location.")
        if len(args) != 1 :
            return await ctx.send("Invalid number of arguments!")
        guildplace = db.GuildHub.objects.get(guild_id = str(ctx.guild.id))
        return await ctx.send(mim.buyItem(battler, guildplace, int(args[0])))
    
    @commands.command(name='sell')
    @commands.guild_only()
    async def sell_object_to_guild_shop(self,ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if node.guild_id != str(ctx.guild.id):
            return await ctx.send("Your currently active character is not in this Guild's location.")
        if len(args) != 1 :
            return await ctx.send("Invalid number of arguments!")
        return await ctx.send(mim.sellItem(battler, int(args[0])))
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Interaction(bot))