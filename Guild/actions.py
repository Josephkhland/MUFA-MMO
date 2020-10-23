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
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(GuildActions(bot))