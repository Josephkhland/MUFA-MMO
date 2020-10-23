import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import character
import datetime
import discord
from discord.ext import commands

class GuildSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='guild_rename')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)  
    async def rename(self, ctx, *args):
        if len(args) == 0 or len(args)>1:
            await ctx.send('This command only needs 1 argument. If the name you want to give your guild has more than 1 words make sure to include it within quotation marks\nExample: !guild rename "New Guild Name" ') 
        else:
            guildo = db.GuildHub.objects.get(guild_id = str(ctx.guild.id))
            guildo.name = args[0]
            guildo.save()
            await ctx.send("Your guild name has been changed to: `"+ args[0] +"`. Within the context of the game it shall be viewed with that name.")

     
    @commands.command(name='guild_privacy')
    @commands.guild_only()
    @commands.has_permissions(administrator=True) 
    async def privacy(self, ctx, *args):
        if len(args) == 0 or len(args)>1:
            await ctx.send("This command only needs exactly 1 argument. Available options: `OPEN`, `CLOSED`, `ALLIANCE`.") 
        else:
            guildo = db.GuildHub.objects.get(guild_id = str(ctx.guild.id))
            if args[0].lower() == "open":
                guildo.privacy_setting = db.GuildPrivacy.OPEN.value
            elif args[0].lower() == "alliance":
                guildo.privacy_setting = db.GuildPrivacy.ALLIANCE.value
            elif args[0].lower() == "closed": 
                guildo.privacy_setting = db.GuildPrivacy.CLOSED.value
            else:
                await ctx.send("Invalid argument.")
                return
            guildo.save()
        await ctx.send("Your Guild's privacy setting has been updated to: `" +args[0].upper()+"`.")
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(GuildSettings(bot))