import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import character
import discord
from discord.ext import commands

class Navigation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='teleport', aliases=['warp'])
    @commands.guild_only()
    async def teleport(self, ctx):
        """This command can be used by a registered player in order to teleport to the coordinates of a Server."""
        if not character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        p_coords = mw.get_battler_coordinates(str(ctx.author.id))
        n_id = mw.getGuildNode(str(ctx.guild.id))
        mw.travel_to_node(str(n_id),str(ctx.author.id))
        n_coords = mw.get_battler_coordinates(str(ctx.author.id))
        try:finalize_message = "**Teleported to : ("+str(n_coords[0])+","+str(n_coords[1])+")**\nPrevious location ("+str(p_coords[0])+","+str(p_coords[1])+")"
        except:
            finalize_message = "There was an error"
            print(n_coords)
        await ctx.send(finalize_message)

    @commands.command(name='move', aliases=['travel'])
    async def move(self, ctx, *args):
        """Use this command to travel East, West, North or South in the World Map."""
        if not character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        temp_o = db.Battler.objects.get(battler_id = str(ctx.author.id))
        pCharac = temp_o.getCharacter()
        c_node = pCharac.getInstance()
        prepare_message = "```"
        south_aliases = ["s","south","y-","-y","down","d"]
        east_aliases = ["e","east","x+","+x","right","r"]
        north_aliases = ["n","north","y+", "+y", "up", "u"]
        west_aliases = ["w", "west", "x-", "-x", "left", "l"]
        if args[0].lower() in south_aliases:
            if c_node.south_exit == None:
                prepare_message += "The path to the South is blocked.\n"
            else:
                prepare_message +="Travelled South.\n"
                mw.travel_to_node(c_node.south_exit, str(ctx.author.id))
        elif args[0].lower() in east_aliases:
            if c_node.east_exit == None:
                prepare_message +="The path to the East is blocked\n"
            else:
                prepare_message +="Travelled East.\n"
                mw.travel_to_node(c_node.east_exit, str(ctx.author.id))
        elif args[0].lower() in north_aliases:
            if c_node.north_exit == None:
                prepare_message +="The path to the North is blocked.\n"
            else:
                prepare_message +="Travelled North.\n"
                mw.travel_to_node(c_node.north_exit, str(ctx.author.id))
        elif args[0].lower() in west_aliases:
            if c_node.west_exit == None:
                prepare_message +="The path to the West is blocked\n"
            else:
                prepare_message +="Travelled West.\n"
                mw.travel_to_node(c_node.west_exit, str(ctx.author.id))
        else:
            prepare_message +="["+args[0]+"] is not a valid direction.\n"
        
        c_coords = mw.get_battler_coordinates(str(ctx.author.id))
        prepare_message+= "Your current coordinates:  (x: "+str(c_coords[0])+ ", y: "+str(c_coords[1])+ ")"
        finalize_message = prepare_message + "```"
        await ctx.send(finalize_message)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Navigation(bot))