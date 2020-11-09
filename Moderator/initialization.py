import mufadb as db
import mufa_constants as mconst
import mufa_world
import basic_pack
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
            mufa_world.insert_guild(str(guild.id),guild.name)
    
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
            msg_to_send = "```\n"
            for i in range(mconst.world_size.get('x')):
                for j in range(mconst.world_size.get('y')):
                    msg_to_send += str(n_list[i*5 + j]) +" "
                msg_to_send += "\n"
            msg_to_send += "```"
            await ctx.send(msg_to_send)
    
    @commands.command(name='initialize')
    async def initialize(self, ctx):
         user = str(ctx.author.id)
         guild = ctx.guild
         if user in moderators_list:
            mufa_world.generate()
            mufa_world.insert_guild(str(guild.id),guild.name)
            mufa_world.createDemoArmorSet()
            mufa_world.createNullObject()
            for i in range(7):
                if i<3:
                    mufa_world.createDemoArmor(i)
                if i >=3:
                    mufa_world.createDemoWeapon(i-3)
            guildhub = db.GuildHub.objects.get(guild_id = str(ctx.guild.id))
            mufa_world.demoItemsGuild(guildhub)
    
    @commands.command(name='import')
    async def initialize(self, ctx, *args):
         user = str(ctx.author.id)
         guild = ctx.guild
         if user in moderators_list:
            if len(args) != 1 :
                return await ctx.send("You must specify which pack you wish to import")
            if args[0] == "basic":
                if db.PackageNames.objects.get(name = "basic") == None:
                    basic_pack.install_pack()
                else:
                    await ctx.send("`basic` pack already installed") 
                    
    
    @commands.command(name='moderator_monster')
    async def mod_mon_summon(self,ctx, *args):
        user = str(ctx.author.id)
        guild = ctx.guild    
        if user in moderators_list:
            if len(args) != 1:
                await ctx.send("Invalid number of arguments")
                return
            try: 
                node = db.Node.objects.get(node_id = args[0])
            except:
                await ctx.send("Instance not found!")
                return
            null_obj = db.Item.objects.get(name = "null_object").to_dbref()
            weapon_slash = db.Weapon.objects.get(name = "Demo Slash").to_dbref()
            n_char = db.character(name = "Test",
                                willpower = 1,
                                vitality = 1,
                                agility = 1,
                                strength = 1,
                                karma = 1,
                                current_health = 10,
                                current_sanity = 10,
                                armor_equiped = [null_obj,null_obj,null_obj],
                                weapons_equiped = [weapon_slash,null_obj,null_obj,null_obj],
                                instance_stack = [node.to_dbref()]
                                )
            new_id = mufa_world.generateMonsterID()
            db.Monster(battler_id = new_id, name =n_char.name ,character_stats=n_char).save()
            monstro = db.Monster.objects.get(battler_id = new_id).to_dbref()
            node_placed = db.Node.objects.no_dereference().get(node_id = args[0])
            node_placed.members.append(monstro)
            node_placed.save()
            await ctx.send("Monster Spawned")
    
    

    
def setup(bot):
    bot.add_cog(Initialization(bot))