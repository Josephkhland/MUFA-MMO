import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import character
import datetime
import discord
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='myprofile')
    async def show(self,ctx, user: discord.User = None):
        """Shows your Profile, or the profile of a mentioned user."""
        userID = str(ctx.author.id)
        if user != None :
            userID = str(user.id)
        await ctx.channel.send(embed=character.show(userID))

    @commands.command(name='myimage')
    async def image(self,ctx, *args):
        """Shows your active character's image
           
           +myimage set imageURL 
           In order to set a new picture for your character.
        """
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        pCharac = battler.getCharacter()
        if len(args)==0:
            await ctx.send(pCharac.imageURL)
        else:
            if len(args) == 2 and args[0] == "set":
                pCharac.imageURL = args[1]
                battler.updateCurrentCharacter(pCharac)
                battler.save()
    @commands.command(name='mycharacter')
    async def my_character(self, ctx, *args):
        """Shows the details of your currently Active Character"""
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        pCharac = battler.getCharacter()
        healthString = mdisplay.digits_panel(pCharac.current_health,pCharac.vitality*10, 8) + ":heart: "
        sanityString = mdisplay.digits_panel(pCharac.current_sanity,pCharac.willpower*10, 8) + ":brain: "
        actionsString = mdisplay.digits_panel(pCharac.actions_left, pCharac.max_actions, 8) + ":zap: "
        embed = discord.Embed(
            title = pCharac.name + " ("+playerID+")",
            description = healthString + sanityString + actionsString,
            colour = discord.Colour.red(),
            timestamp = datetime.datetime.now()
        )
        embed.set_footer(text="Instance: "+str(pCharac.getInstance().node_id) +" ("+str(pCharac.coordinates[0])+","+str(pCharac.coordinates[1])+")")
        
        #Setting up the field for the Primary Stats.
        primaryStatsString = mdisplay.line("Willpower",pCharac.willpower)
        primaryStatsString += mdisplay.line("Vitality",pCharac.vitality)
        primaryStatsString += mdisplay.line("Agility",pCharac.agility)
        primaryStatsString += mdisplay.line("Strength",pCharac.strength)
        primaryStatsString += mdisplay.line("Karma",pCharac.karma)
        embed.add_field(name="Primary Stats", value=primaryStatsString, inline=True)
        
        #Setting up the field for the Progression Stats
        progressionStatsString = mdisplay.line("Level", pCharac.level)
        progressionStatsString += "Experience: "+ mdisplay.digits_panel(pCharac.experience, pCharac.exp_to_next_level,12) + "\n"
        progressionStatsString += mdisplay.line("Unused Points", pCharac.unused_points)
        embed.add_field(name="Progression", value=progressionStatsString, inline=True)
        
        #Setting up the field for the Armor
        armorString = mdisplay.equipment(0,pCharac.armor_equiped[0])
        armorString += mdisplay.equipment(1,pCharac.armor_equiped[1])
        armorString += mdisplay.equipment(2,pCharac.armor_equiped[2])
        if pCharac.set_bonus_specification == 1:
            armorString += " :small_blue_diamond:*Set Bonus*: `"+pCharac.armor_set.name
            if pCharac.armor_set.two_items_set_bonus[0] != 0:
                armorString += " "+ str(pCharac.armor_set.two_items_set_bonus[0]) + " WILL"
            if pCharac.armor_set.two_items_set_bonus[1] != 0:
                armorString += " "+ str(pCharac.armor_set.two_items_set_bonus[1]) + " VIT"
            if pCharac.armor_set.two_items_set_bonus[2] != 0:
                armorString += " "+ str(pCharac.armor_set.two_items_set_bonus[2]) + " AGI"
            if pCharac.armor_set.two_items_set_bonus[3] != 0:
                armorString += " "+ str(pCharac.armor_set.two_items_set_bonus[3]) + " STR"
            armorString += "`\n"
        if pCharac.set_bonus_specification == 2:
            armorString += " :small_orange_diamond:*Set Bonus*: `"+pCharac.armor_set.name
            if pCharac.armor_set.full_set_bonus[0] != 0:
                armorString += " "+ str(pCharac.armor_set.full_set_bonus[0]) + " WILL"
            if pCharac.armor_set.full_set_bonus[1] != 0:
                armorString += " "+ str(pCharac.armor_set.full_set_bonus[1]) + " VIT"
            if pCharac.armor_set.full_set_bonus[2] != 0:
                armorString += " "+ str(pCharac.armor_set.full_set_bonus[2]) + " AGI"
            if pCharac.armor_set.full_set_bonus[3] != 0:
                armorString += " "+ str(pCharac.armor_set.full_set_bonus[3]) + " STR"
            armorString += "`\n"
        embed.add_field(name="Armor", value=armorString, inline=False)
        
        #Setting up the field for Weapons
        weaponString = mdisplay.equipment(3,pCharac.weapons_equiped[0])
        weaponString += mdisplay.equipment(4,pCharac.weapons_equiped[1])
        weaponString += mdisplay.equipment(5,pCharac.weapons_equiped[2])
        weaponString += mdisplay.equipment(6,pCharac.weapons_equiped[3])
        embed.add_field(name=":crossed_swords:Weapons:crossed_swords:", value=weaponString, inline=True)
        
        #Setting up the Spells Field
        spellString = ":diamond_shape_with_a_dot_inside:`Fireball`\n:diamond_shape_with_a_dot_inside:`Diamond Spray`"
        embed.add_field(name=":book:Spells:book:", value=spellString, inline=True)
        
        #Setting up Inventory Field
        inventoryString = "Use `+myinventory` to access your inventory\n\n"
        inventoryString+= ":scales:Carrying `"+str(len(pCharac.inventory))+"/"+str(pCharac.strength*5)+"` items   "
        inventoryString+= ":coin: Gold Carried `"+str(pCharac.money_carried)+"`"
        embed.add_field(name=":handbag:Inventory:handbag:", value=inventoryString, inline=False)
        embed.set_thumbnail(url= pCharac.imageURL)
        await ctx.send(embed = embed)
        
    
    @commands.command(name='mycharacters')
    async def my_characters(self, ctx):
        """Shows an index of your characters"""
        await ctx.send("COMMAND NOT READY")


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Profile(bot))