import mufadb as db
import mufa_constants as mconst
import mufa_world as mw 
import mufadisplay as mdisplay
import mufa_item_management as mim
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
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        userID = str(ctx.author.id)
        if user != None :
            userID = str(user.id)
        await ctx.channel.send(embed=character.show(userID, self.bot))

    @commands.command(name='myimage')
    async def image(self,ctx, *args):
        """Shows your active character's image
           
           +myimage set imageURL 
           In order to set a new picture for your character.
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
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
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        pCharac = battler.getCharacter()
        status = ":bust_in_silhouette: "
        if pCharac.is_dead:
            status = ":skull: "
        healthString = mdisplay.digits_panel(pCharac.current_health,pCharac.vitality*10, 8) + ":heart: "
        sanityString = mdisplay.digits_panel(pCharac.current_sanity,pCharac.willpower*10, 8) + ":brain: "
        actionsString = mdisplay.digits_panel(pCharac.actions_left, pCharac.max_actions, 8) + ":zap: "
        embed = discord.Embed(
            title = status+pCharac.name + " ("+playerID+")",
            description = healthString + sanityString + actionsString,
            colour = discord.Colour.red(),
            timestamp = datetime.datetime.now()
        )
        embed.set_footer(text="Instance: "+str(pCharac.getInstance().node_id) +" ("+str(pCharac.coordinates[0])+","+str(pCharac.coordinates[1])+")")
        
        #Setting up the field for the Primary Stats.
        primaryStatsString = mdisplay.line("Willpower",pCharac.willpower,12)
        primaryStatsString += mdisplay.line("Vitality",pCharac.vitality,12)
        primaryStatsString += mdisplay.line("Agility",pCharac.agility,12)
        primaryStatsString += mdisplay.line("Strength",pCharac.strength,12)
        primaryStatsString += mdisplay.line("Karma",pCharac.karma,12)
        embed.add_field(name="Primary Stats", value=primaryStatsString, inline=True)
        
        #Setting up the field for the Progression Stats
        progressionStatsString = mdisplay.line("Level", pCharac.level,12)
        progressionStatsString += "Experience: "+ mdisplay.digits_panel(pCharac.experience, pCharac.exp_to_next_level,12) + "\n"
        progressionStatsString += mdisplay.line("Unused Points", pCharac.unused_points,12)
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
        inventoryString+= ":scales:Carrying `"+str(len(pCharac.inventory))+"/"+str(pCharac.strength*6)+"` items   "
        inventoryString+= ":coin: Gold Carried `"+str(pCharac.money_carried)+"`"
        embed.add_field(name=":handbag:Inventory:handbag:", value=inventoryString, inline=False)
        embed.set_thumbnail(url= pCharac.imageURL)
        await ctx.send(embed = embed)
        
    
    @commands.command(name='mycharacters')
    async def my_characters(self, ctx):
        """Shows an index of your characters"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        embed = discord.Embed(
            title = battler.name + " ("+playerID+")",
            description = "Index of your characters. Use the indexes here when attempting to select another of your characters",
            colour = discord.Colour.red(),
            timestamp = datetime.datetime.now()
        )
        counter = 0
        for chara in battler.characters_list:
            disabling_conditions = [False,False,False]
            this_value = "Conditions: "
            for con in chara.conditions:
                if con.name == 'DEAD':
                    disabling_conditions[0] = True
                if con.name == 'PETRIFIED':
                    disabling_conditions[1] = True
                if con.name == 'ASLEEP':
                    disabling_conditions[2] = True
                this_value += "`"+con.name+"` "
            name_plugin = " "
            if disabling_conditions[2]:
                name_plugin += ":zzz: "
            if disabling_conditions[1]:
                name_plugin += ":rock: "
            if disabling_conditions[0]:
                name_plugin += ":skull: "
            embed.add_field(name=str(counter) +": " + chara.name +name_plugin, value= this_value, inline = False)
            counter += 1
        await ctx.send(embed = embed)
    
    @commands.command(name='suicide')
    async def suicide(self, ctx):
        """Kills your currently active character"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        pCharac = battler.getCharacter()
        message_to_send = pCharac.kill()
        battler.updateCurrentCharacter(pCharac)
        battler.save()
        await ctx.send(message_to_send)
    
    @commands.command(name='switch_to_character')
    async def switch_to_character(self, ctx, *args):
        """Switch your Active character to the one you define with an index.
           Use the index as seen in your character's list. ( !mycharacters ) 
           Correct usage: !switch_to_character index
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        if int(args[0]) <0 or int(args[0]) >= len(battler.characters_list):
            message_to_send = "Invalid argument"
        else:
            battler.active_character = int(args[0])
            battler.save()
            message_to_send = "Successfully changed active character to: **"+battler.getCharacter().name+"**."
        await ctx.send(message_to_send)
    
    @commands.command(name='abandon_character')
    async def abandon_character(self, ctx, *args):
        """Permamently deletes a character.
           Use it to clear up space for more characters.
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        if int(args[0]) <0 or int(args[0]) >= len(battler.characters_list):
            message_to_send = "Invalid argument"
        else:
            temp = battler.characters_list[int(args[0])].name
            del battler.characters_list[int(args[0])]
            if battler.active_character >= int(args[0]):
                battler.active_character = max(0, battler.active_character -1)
            battler.save()
            message_to_send = "Goodbye forever: **"+temp+"**."
        await ctx.send(message_to_send)
    
    @commands.command(name='mydescendants', aliases = ['descendants', 'character_options'])
    async def show_descendants(self, ctx, *args):
        """
            Shows your available descendants. 
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        embedList = mdisplay.displayDescendants(battler)
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
    
    @commands.command(name='myinventory', aliases = ['inventory', 'inv', 'i'])
    async def show_inventory(self, ctx, *args):
        """
            Shows your inventory
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.get(battler_id = playerID)
        if len(battler.characters_list) == 0:
            return await ctx.send("You don't have an active character")
        
        pCharac = battler.getCharacter()
        embedList = mdisplay.displayInventoryList(pCharac)
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

    @commands.command(name='migrate')
    @commands.guild_only()
    async def migrate(self, ctx):
        """Change the Serve/Guild you are registered to."""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        playerID = str(ctx.author.id)
        guildID = str(ctx.guild.id)
        battler = db.Player.objects.get(battler_id = playerID)
        battler.guild_id = guildID
        battler.save()
        await ctx.send("Migrated to **"+ ctx.guild.name + "** succesfully!")
    
    @commands.command(name='compare')
    async def compare_items(self, ctx, *args):
        """Compare an item, with the one you have equipped in the according slot, use with"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        
        if len(args) <1 or len(args) >2:
            return await ctx.send("Invalid number of arguments")
        storage_aliases = ["-s", "s", "storage", "vault", "house"]
        if args[1] in storage_aliases:
            return await ctx.send(embed =mim.compare_item(int(args[0]),battler,True))
        else: 
            return await ctx.send(embed =mim.compare_item(int(args[0]),battler,False))
    
    @commands.command(name='equip')
    async def equip_item(self, ctx, *args):
        """Equip an item from your inventory"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if isinstance(node, db.Battle):
            return await ctx.send("You can't change your equipment during a battle.")
        if len(args) <1 or len(args) >2:
            return await ctx.send("Invalid number of arguments")
        item_index = int(args[0])
        try:
            slot_index = int(args[1])
        except: 
            slot_index = 0
        return await ctx.send(mim.equipItem(item_index,battler,slot_index))
    
    @commands.command(name='unequip')
    async def unequip_item(self, ctx, *args):
        """Place an equipped item in your inventory"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if isinstance(node, db.Battle):
            return await ctx.send("You can't change your equipment during a battle.")
        if len(args) !=1 :
            return await ctx.send("Invalid number of arguments")
        slot_index = int(args[0])
        return await ctx.send(mim.unequipItem(battler,slot_index))
    
    @commands.command(name='storeitem')
    @commands.guild_only()
    async def store_item(self, ctx, *args):
        """Place an item from inventory to Storage"""
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if not await character.playabilityCheck(ctx, str(ctx.author.id)):
            return
        battler = db.Player.objects.get(battler_id = str(ctx.author.id))
        pCharac = battler.getCharacter()
        node = pCharac.getInstance()
        if node.guild_id != battler_id.guild_id:
            return await ctx.send("Your currently active character is not near your guild.")
        if len(args) !=1 :
            return await ctx.send("Invalid number of arguments")
        slot_index = int(args[0])
        await ctx.send(storeItem(pCharac.inventory, slot_index, battler))
        inventory = pCharac.inventory
        del inventory[slot_index]
        pCharac.inventory = inventory
        battler.updateCurrentCharacter(pCharac)
        battler.save()
        return

    @commands.command(name='set_pve_password')
    async def set_pve_password(self,ctx, *args):
        """If you wish for your PvE Sessions to be password protected, use this
           Command in order to create a password.
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if len(args) == 0:
            return await ctx.send("This command requires at least one argument")
        if len(args[0]) < 6:
            return await ctx.send("If you wish to set a new password it needs to be at least 6 Characters.")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.no_dereference().get(battler_id = playerID)
        battler.pve_join_password = args[0]
        battler.save()
        await ctx.send("You have successfully created a password for your PvE Sessions")
        return
    
    @commands.command(name='remove_pve_password')
    async def remove_pve_password(self,ctx, *args):
        """Use this if you have created a password for your PvE sessions, and you wish to make them public once again.
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        
        playerID = str(ctx.author.id)
        battler = db.Player.objects.no_dereference().get(battler_id = playerID)
        battler.pve_join_password = None
        battler.save()
        await ctx.send("You have successfully turned your PvE Sessions Public.")
        return
    
    @commands.command(name='set_party_limit')
    async def set_party(self,ctx, *args):
        """Use this to determine the maximum number of players in your party for Battle instances and Dungeons.
        """
        if not character.checkRegistration(str(ctx.author.id)):
            return await ctx.send("You are not registered. Please register by using the command `!register`")
        if len(args) == 0:
            return await ctx.send("This command requires at least one argument")
        if int(args[0]) < 1:
            return await ctx.send("Party size limit can't be less than 1")
        playerID = str(ctx.author.id)
        battler = db.Player.objects.no_dereference().get(battler_id = playerID)
        battler.pve_player_limit = int(args[0])
        battler.save()
        await ctx.send("You have successfully changed your Party Limit.")
        return
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(Profile(bot))