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
    n_char = db.character(name = descendant.character_name,
                 willpower = descendant.will_bonus,
                 vitality = descendant.vitality_bonus,
                 agility = descendant.agility_bonus,
                 strength = descendant.strength_bonus,
                 karma = descendant.starting_karma,
                 current_health = descendant.vitality_bonus*10,
                 current_sanity = descendant.will_bonus*10,
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
    
def show(playerID):
    pObject = db.Battler.objects.get(battler_id= playerID)
    if pObject == None:
        return "User not found"
    charac = pObject.getCharacter()
    print(charac)
    embed = discord.Embed(
        title = pObject.name + " Profile",
        description = "Powered by Josephkhland",
        colour = discord.Colour.red()
    )
    embed.set_footer(text="Profile("+playerID+") powered by Josephkhland")
    embed.add_field(name="Guild", value=pObject.guild_id, inline=False)
    embed.add_field(name="Stored Money", value=pObject.money_stored, inline=False)
    embed.add_field(name="Last Time Active", value=pObject.last_action_date.ctime(), inline=False)
    embed.add_field(name="Active Character", value=charac.name, inline=False)
    
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