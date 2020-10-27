import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import character
import datetime
import discord
from discord.ext import commands

class GuildActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='guild_discover')
    async def rename(self, ctx):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        playerUser = self.bot.get_user(ctx.author.id)
        battler = db.Battler.objects.get(battler_id = playerID)
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if node.guild_id != None:
            guild = db.GuildHub.objects.get(guild_id = node.guild_id)
            if guild.privacy_setting == db.GuildPrivacy.OPEN.value:
                #Check if the user is already a member of the guild and send invite.
                this_guild = self.bot.get_guild(int(node.guild_id))
                if guild.invites_channel == None:
                    message_to_invite = this_guild.text_channels[0]
                else:
                    message_to_invite = self.bot.get_channel(int(guild.invites_channel))
                link = await message_to_invite.create_invite(max_age = 300, max_uses = 1, temporary = True, reason = "Server Discovery by user:"+ ctx.author.name)
                message_to_send = "Here is an instant invite to `"+guild.name+"` Server: " + str(link) +"\nThis invite will expire after 5 minutes."
                await playerUser.send(message_to_send)
            else:
                await ctx.send("The Guild in the current Location is not OPEN to public")
        else:
            await ctx.send("There is no Guild in this Location.")
            
            
    @commands.command(name='browse_shop')
    @commands.guild_only()
    async def browse_shop(self, ctx, *args):
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        playerUser = self.bot.get_user(ctx.author.id)
        battler = db.Battler.objects.get(battler_id = playerID)
        if len(battler.characters_list) == 0:
            return await ctx.send("You don't have an active character.")
        pCharac = battler.getCharacter()
        if pCharac.is_dead == 0:
            return await ctx.send("You can't use the shop with a dead character.")
        guild = db.GuildHub.objects.get(guild_id = str(ctx.guild.id))
        
        analytic = False
        if args[0] == "-i":
            analytic = True
        embedList = mdisplay.displayShopList(guild, analytic)
        totalTabs = len(embedList)
        c_t = 0
        if len(embedList) == 0 : 
            return await ctx.send("You have no items in your inventory!")
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
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(GuildActions(bot))