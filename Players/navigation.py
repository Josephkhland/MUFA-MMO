import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import character
import discord
import asyncio
from discord.ext import commands

class Navigation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='teleport', aliases=['warp'])
    @commands.guild_only()
    async def teleport(self, ctx):
        """This command can be used by a registered player in order to teleport to the coordinates of a Server."""
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        p_coords = mw.get_battler_coordinates(str(ctx.author.id))
        n_id = mw.getGuildNode(str(ctx.guild.id))
        embed = mw.travel_to_node(str(n_id),str(ctx.author.id))
        n_coords = mw.get_battler_coordinates(str(ctx.author.id))
        try:finalize_message = "**Teleported to : ("+str(n_coords[0])+","+str(n_coords[1])+")**\nPrevious location ("+str(p_coords[0])+","+str(p_coords[1])+")"
        except:
            finalize_message = "There was an error"
            print(n_coords)
        await ctx.send(finalize_message, embed= embed)

    @commands.command(name='move', aliases=['travel'])
    async def move(self, ctx, *args):
        """Use this command to travel East, West, North or South in the World Map."""
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        temp_o = db.Battler.objects.get(battler_id = str(ctx.author.id))
        pCharac = temp_o.getCharacter()
        c_node = pCharac.getInstance()
        embed = discord.Embed(
            title = "Instance Information",
            description = "**Description:** "+ str(c_node.entrance_message),
            colour = discord.Colour.green()
        )
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
                embed = mw.travel_to_node(c_node.south_exit, str(ctx.author.id))
        elif args[0].lower() in east_aliases:
            if c_node.east_exit == None:
                prepare_message +="The path to the East is blocked\n"
            else:
                prepare_message +="Travelled East.\n"
                embed = mw.travel_to_node(c_node.east_exit, str(ctx.author.id))
        elif args[0].lower() in north_aliases:
            if c_node.north_exit == None:
                prepare_message +="The path to the North is blocked.\n"
            else:
                prepare_message +="Travelled North.\n"
                embed = mw.travel_to_node(c_node.north_exit, str(ctx.author.id))
        elif args[0].lower() in west_aliases:
            if c_node.west_exit == None:
                prepare_message +="The path to the West is blocked\n"
            else:
                prepare_message +="Travelled West.\n"
                embed = mw.travel_to_node(c_node.west_exit, str(ctx.author.id))
        else:
            prepare_message +="["+args[0]+"] is not a valid direction.\n"
        
        c_coords = mw.get_battler_coordinates(str(ctx.author.id))
        prepare_message+= "Your current coordinates:  (x: "+str(c_coords[0])+ ", y: "+str(c_coords[1])+ ")"
        finalize_message = prepare_message + "```"
        await ctx.send(finalize_message, embed = embed)

    @commands.command(name='info')
    async def show_instance_information(self, ctx, *args):
        """Shows the information of the instance where your active character is at"""
        battler = db.Battler.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        await ctx.send(embed = mw.node_information(node))
    
    @commands.command(name='here')
    async def show_node_members(self,ctx, *args):
        battler = db.Battler.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        nodeMemberStrings = mdisplay.node_members(node)
        players = nodeMemberStrings[0]
        monsters = nodeMemberStrings[1]
        embed = discord.Embed(
            title = "Instance Members",
            description = "The players and monsters in the Instance are visible below",
            colour = discord.Colour.blue()
        )
        c_t = 0 #Current Tab
        totalTabs = len(max(players,monsters))
        if players[c_t] == None or players[c_t] == '' :
            players[c_t] = "NONE"
        if monsters[c_t] == None or monsters[c_t] == '':
            monsters[c_t] = "NONE"
        embed.set_footer(text="Instance("+node.node_id+") - Members: Tab "+str(c_t+1)+"/" +str(totalTabs))
        embed.add_field(name = "Players", value = players[c_t], inline = False)
        embed.add_field(name = "Monsters", value = monsters[c_t], inline = False)
        msg = await ctx.send(embed = embed)
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
                    embed_edited = discord.Embed(
                        title = "Instance Members",
                        description = "The players and monsters in the Instance are visible below",
                        colour = discord.Colour.blue()
                    )
                    embed_edited.set_footer(text="Instance("+node.node_id+") - Members: Tab "+str(c_t+1)+"/" +str(totalTabs))
                    if c_t >= len(players): 
                        embed_edited.add_field(name = "Players", value = players[-1], inline = False)
                    else:
                        if players[c_t] == None or players[c_t] == '':
                            players[c_t] = "NONE"
                        embed_edited.add_field(name = "Players", value = players[c_t], inline = False)
                    if c_t >= len(monsters):
                        embed_edited.add_field(name = "Monsters", value = monsters[-1], inline = False)
                    else:
                        if monsters[c_t] == None or monsters[c_t] == '':
                            monsters[c_t] = "NONE"
                        embed_edited.add_field(name = "Monsters", value = monsters[c_t], inline = False)
                    await msg.edit(embed = embed_edited)
                    pending_collectors = None
                    done_collectors = None
                except asyncio.TimeoutError:
                    await msg.add_reaction('💤')
                    loop = False
            

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Navigation(bot))