import mufadb as db
import mufa_constants as mconst
import mufa_world
import discord
from discord.ext import commands

moderators_list = ['91573021759791104']

class Initialization(commands.Cog , command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='force_guild_add')
    @commands.guild_only()
    async def force_guild_add(self, ctx):
        guild = ctx.guild
        user = str(ctx.author.id)
        if user in moderators_list:
            print ("New Guild joined")
            mufa_world.insert_guild(str(guild.id))
    
    @commands.command(name='force_guild_remove')
    @commands.guild_only()
    async def force_guild_remove(self, ctx):
        guild = ctx.guild
        user = str(ctx.author.id)
        if user in moderators_list:
            print ("New Guild joined")
            mufa_world.insert_guild(str(guild.id))
    
    @commands.command(name='generate_world')
    async def generate_world(self, ctx):
         user = str(ctx.author.id)
         if user in moderators_list:
            mufa_world.generate()
    
    @commands.command(name='visualize_world')
    async def visualize_world(self,ctx):
        user = str(ctx.author.id)
        if user in moderators_list:
            n_list = mufa_world.visualize()
            msg_to_send = "```"
            for i in range(5):
                for j in range(5):
                    msg_to_send += str(n_list[i*5 + j])
                msg_to_send += "\n"
            msg_to_send += "```"
            await ctx.send(msg_to_send)
    
def setup(bot):
    bot.add_cog(Initialization(bot))