import datetime
import mufadb as db 

def register(playerID,username, guild_id, date):
    db.Player(identification = playerID,
              name = username, 
              guild_id = guild_id,
              last_action_date= datetime.datetime.now(),
              descendant_options = [db.descendant()],
              creation_date = datetime.datetime.now()
             ).save()
   
def spawn(playerID, name, descendant: db.descendant, guildID):
    if descendant.character_name == None :
        descendant.character_name = name
    coords = db.GuildHub.get(id = guildID).coordinates
    n_char = db.character(name = descendant.character_name,
                 willpower = descendant.will_bonus,
                 vitality = descendant.vitality_bonus,
                 agility = descendant.agility_bonus,
                 strength = descendant.strength_bonus,
                 karma = descendant.starting_karma,
                 current_health = descendant.vitality_bonus*10,
                 current_sanity = descendant.will_bonus*10,
                 coordinates = coords)
    db.Player.objects(id = playerID).update(push__characters_list = n_char)
    curP = db.Player.get(id = playerID)
    db.Player.objects(id = playerID).update(set__active_character =  len(curp.characters_list))
    db.Player.objects(id = playerID).update(set__descendant_options = [db.descendant()])

def checkRegistration(playerID):
    if db.Player.get(id = playerID) == None:
        return False
    else :
        return True
    
def show(playerID):
    pObject = db.Player.get(id = playerID)
    if pObject == None:
        return "User not found"
    embed = discord.Embed(
        title = pObject.name + " Profile",
        description = "Powered by Josephkhland",
        colour = discord.Colour.red()
    )
    embed.set_footer(text="Profile("+playerID+") powered by Josephkhland")
    embed.add_field(name="Guild", value=pObject.guild_id, inline=False)
    embed.add_field(name="Stored Money", value=pObject.money_stored, inline=False)
    embed.add_field(name="Last Time Active", value=pObject.last_action_date, inline=False)
    embed.add_field(name="Active Character", value=pObject.getCharacter().name, inline=False)
    
    playable_characters = "`"
    unavailable_characters = "`"
    for c in pObject.characters_list:
        for con in c.conditions:
            if con.name == "PETRIFIED" or con.name == "DEAD":
                unavailable_characters += c.name +"` "
            else: 
                playable_characters += c.name
    embed.add_field(name="Available Characters", value=playable_characters, inline = False)
    embed.add_field(name="Unavailable Characters", value=unavailable_characters, inline= False)
    embed.add_field(name="Date Joined", value= pObject.creation_date, inline = False)
    return embed