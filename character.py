import datetime
import discord
import mufadb as db 

def register(playerID,username, guild_id, date):
    db.Player(battler_id = playerID,
              name = username, 
              guild_id = guild_id,
              last_action_date= datetime.datetime.now(),
              descendant_options = [db.descendant()],
              creation_date = datetime.datetime.now()
             ).save()
   
def spawn(playerID, name, descendant, guildID):
    if descendant.character_name == None :
        descendant.character_name = name
    coords = db.GuildHub.objects.get(guild_id = guildID).coordinates
    temp = db.WorldNode.objects.get(coordinates = coords)
    null_obj = db.Item.objects.get(name = "null_object").to_dbref()
    n_char = db.character(name = descendant.character_name,
                 willpower = descendant.will_bonus,
                 vitality = descendant.vitality_bonus,
                 agility = descendant.agility_bonus,
                 strength = descendant.strength_bonus,
                 karma = descendant.starting_karma,
                 current_health = descendant.vitality_bonus*10,
                 current_sanity = descendant.will_bonus*10,
                 armor_equiped = [null_obj,null_obj,null_obj],
                 weapons_equiped = [null_obj,null_obj,null_obj,null_obj],
                 instance_stack = [temp.to_dbref()],
                 coordinates = coords)
    db.Battler.objects(battler_id = playerID).update(push__characters_list = n_char)
    curp = db.Battler.objects.get(battler_id = playerID)
    db.Battler.objects(battler_id = playerID).update(set__active_character =  len(curp.characters_list)-1)
    db.Battler.objects(battler_id= playerID).update(set__descendant_options = [db.descendant()])

def checkRegistration(playerID):
    print(db.Battler.objects.get(battler_id = playerID))
    if db.Battler.objects.get(battler_id= playerID) == None:
        return False
    else :
        return True
        
def getHaltingConditions(battler_id):
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    disabling_conditions = []
    for con in pCharac.conditions:
        if con.name == "PETRIFIED" or con.name == "DEAD" or con.name == "ASLEEP":
            disabling_conditions.append(con.name)
    return disabling_conditions

def speculate_condition(mcondition):
    if (condition.duration < 0):
        #The Condition is permament - Won't be removed until it is cured
        return condition.duration
    else:
        end_time = condition.date_added + timedelta(hours =condition.duration)
        if (datetime.now() >= end_time):
            return 0
        else:
            return (datetime.now() - end_time).total_seconds()

def solve_battler_conditions(battler_id):
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    output_message = []
    to_remove = []
    for con in pCharac.conditions:
        if (speculate_condition(con)< 0):
           output_message.append(con.name + " won't be removed over time.")
        elif (speculate_condition(con) == 0):
            output_message.append(con.name + " has been removed.")
            to_remove.append(con)
        else:
            tminute = divmod(speculate_condition(con),60)
            output_message.append(con.name + " will be removed in " + tminute[0] + "minutes and " +tminute[1] + "seconds.")
    for i in to_remove:
        pCharac.conditions.remove(i)
    return output_message

async def playabilityCheck(ctx, battler_id):
    try:
        tempList = getHaltingConditions(battler_id)
    except:
        await ctx.send("No Playable Character available in this Account")
    if len(tempList) == 0:
        return True
    else:
        await ctx.send("Your current character is not playable due to the following condition(s): " + str(tempList) + ".\n")
        return False
    
def show(playerID,bot):
    pObject = db.Battler.objects.get(battler_id= playerID)
    gild = bot.get_guild(int(pObject.guild_id))
    if gild == None: 
        embed = discord.Embed(
            title = "Error: Guild Not Found",
            description = "The server you have registered to is no longer participating in the game. Please migrate to a new server before you can see your profile again",
            colour = discord.Colour(0xFFFF00)
        )
        return embed
    has_character = True
    if pObject == None:
        return "User not found"
    try:
        charac = pObject.getCharacter()
    except:
        has_character = False
    embed = discord.Embed(
        title = pObject.name + " Profile",
        description = "Powered by Josephkhland",
        colour = discord.Colour.red()
    )
    embed.set_footer(text="Profile("+playerID+") - Last Active : " + pObject.last_action_date.ctime())
    embed.add_field(name="Guild", value=gild.name +"("+pObject.guild_id+")", inline=False)
    embed.add_field(name="Stored Money", value=pObject.money_stored, inline=False)
    #embed.add_field(name="Last Time Active", value=pObject.last_action_date.ctime(), inline=False)
    if has_character:
        value_to_display = "`" + charac.name + "`"
        embed.add_field(name="Active Character", value=value_to_display, inline=False)
    
    playable_characters = "Names: "
    unavailable_characters = "Names: "
    for c in pObject.characters_list:
        flag_c = False
        for con in c.conditions:
            if con.name == "PETRIFIED" or con.name == "DEAD":
                unavailable_characters += "`"+c.name +"` "
                flag_c = True
                break
        if flag_c == False:    
            playable_characters += "`"+c.name +"` "
    embed.add_field(name="Available Characters", value=playable_characters, inline = False)
    embed.add_field(name="Unavailable Characters", value=unavailable_characters, inline= False)
    embed.add_field(name="Date Joined", value= pObject.creation_date.ctime(), inline = False)
    return embed