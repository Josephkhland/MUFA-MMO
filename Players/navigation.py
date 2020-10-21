import mufadb as db
import mufa_constants as mconst
import discord
from discord.ext import commands

class Navigation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='teleport', aliases=['warp'])
    @commands.guild_only()
    async def teleport(self, ctx):
        """This command can be used by a registered player in order to teleport to the coordinates of a Server."""
        temp_o = db.Battler.objects.get(identification = str(ctx.author.id))
        pCharac = temp_o.getCharacter()
        prepare_message = "Previous Coordinates ("+str(pCharac.coordinates[0])+","+str(pCharac.coordinates[1])+")"
        pCharac.coordinates = db.GuildHub.objects.get(guild_id = str(ctx.guild.id)).coordinates
        world_pos = db.WorldNode.objects.get(coordinates = pCharac.coordinates)
        pCharac.instance_stack = [world_pos.to_dbref()]
        temp_o.updateCurrentCharacter(pCharac)
        temp_o.save()
        prepare_message = "```Teleported to ("+str(pCharac.coordinates[0])+","+str(pCharac.coordinates[1])+") "+ ctx.guild.name+ ".\n" + prepare_message 
        finalize_message = prepare_message + "```"
        await ctx.send(finalize_message)

    @commands.command(name='move', aliases=['travel'])
    async def move(self, ctx, *args):
        """Use this command to travel East, West, North or South in the World Map."""
        temp_o = db.Battler.objects.get(identification = str(ctx.author.id))
        pCharac = temp_o.getCharacter()
        c_coords = pCharac.coordinates
        prepare_message = "```"
        if args[0].lower() == "s" or args[0].lower() == "south" or args[0].lower() == "y-":
            if c_coords[1] == 0:
                prepare_message += "The path to the South is blocked.\n"
            else:
                prepare_message +="Travelled South.\n"
                c_coords[1] -= 1
        elif args[0].lower() == "e" or args[0].lower() == "east" or args[0].lower() == "x+":
            if c_coords[0] == mconst.world_size.get('x') -1:
                prepare_message +="The path to the East is blocked\n"
            else:
                prepare_message +="Travelled East.\n"
                c_coords[0] += 1
        elif args[0].lower() == "n" or args[0].lower() == "north" or args[0].lower() == "y+":
            if c_coords[1] == mconst.world_size.get('y') -1:
                prepare_message +="The path to the North is blocked.\n"
            else:
                prepare_message +="Travelled North.\n"
                c_coords[1] += 1
        elif args[0].lower() == "w" or args[0].lower() == "west" or args[0].lower() == "x-":
            if c_coords[0] == 0:
                prepare_message +="The path to the West is blocked\n"
            else:
                prepare_message +="Travelled West.\n"
                c_coords[0] -= 1
        else:
            prepare_message +="["+args[0]+"] is not a valid direction.\n"
        pCharac.coordinates = c_coords
        temp_o.updateCurrentCharacter(pCharac)
        temp_o.save()
        prepare_message+= "Your current coordinates:  [ x : "+str(c_coords[0])+ "]" + "[ y : "+str(c_coords[1])+ "]"
        finalize_message = prepare_message + "```"
        await ctx.send(finalize_message)

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')
    
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Navigation(bot))