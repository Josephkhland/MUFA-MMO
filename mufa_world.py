import pymongo
import random
import mongoengine
import mufadb as db 
import mufa_constants as mconst
import discord
import datetime
import time 

def generate():
    for i in range(mconst.world_size.get('x')):
        for j in range(mconst.world_size.get('y')):
            x_zeroed = str(i)
            y_zeroed = str(j)
            id_to_give = "WN_X" + x_zeroed.zfill(4) +"_Y" + y_zeroed.zfill(4) 
            db.WorldNode(node_id = id_to_give, coordinates = [i,j]).save()
    
    for i in range(mconst.world_size.get('x')):
        for j in range(mconst.world_size.get('y')):
            temp = db.WorldNode.objects.get(coordinates = [i,j])
            try:
                #print(db.WorldNode.objects.get(coordinates = [i,j+1]).id)
                temp.north_exit = str(db.WorldNode.objects.get(coordinates = [i,j+1]).id)
            except:
                #print("North Exit - None")
                temp.north_exit = None
            try:
                #print(db.WorldNode.objects.get(coordinates = [i+1,j]).id)
                temp.east_exit = str(db.WorldNode.objects.get(coordinates = [i+1,j]).id)
            except:
                #print("East Exit - None")
                temp.east_exit = None
            
            try:
                #print(db.WorldNode.objects.get(coordinates = [i,j-1]).id)
                temp.south_exit = str(db.WorldNode.objects.get(coordinates = [i,j-1]).id)
            except:
                #print("South Exit - None")
                temp.south_exit = None
            
            try:
                #print(db.WorldNode.objects.get(coordinates = [i-1,j]).id)
                temp.west_exit = str(db.WorldNode.objects.get(coordinates = [i-1,j]).id)
            except:
                #print("West Exit - None")
                temp.west_exit = None
            temp.entrance_message = "("+str(i)+","+str(j)+")"
            temp.save()
    
def insert_guild(guild_to_add : str, name_to_give):
    list_of_free_nodes = []
    for node in db.WorldNode.objects(guild_id=None):
        list_of_free_nodes.append(node.coordinates)
    node_to_fill = random.randint(0,len(list_of_free_nodes)-1)
    db.WorldNode.objects(coordinates=list_of_free_nodes[node_to_fill]).update(set__guild_id = guild_to_add)
    db.GuildHub(guild_id= guild_to_add, name = name_to_give ,coordinates = list_of_free_nodes[node_to_fill]).save()

def remove_guild(guild_to_remove : str):
    db.WorldNode.objects(guild_id = guild_to_remove).update(set__guild_id = None)
    db.GuildHub.objects(guild_id = guild_to_remove).delete()
    db.GuildHub.objects(alliances__S =guild_to_remove).update(set__alliances__S = None)

def visualize():
    list_of_nodes = []
    for node_o in db.WorldNode.objects():
        if node_o.guild_id != None : list_of_nodes.append(1)
        else : list_of_nodes.append(0)
    return list_of_nodes
    
def node_information(node):
    embed = discord.Embed(
        title = "Instance Information",
        description = "**Description:** "+ str(node.entrance_message),
        colour = discord.Colour.green()
    )
    
    #Creating the Field where the available subnodes are written.
    if len(node.sub_nodes_ids) == 0:
        sub_nodes_string = "None"
    else:
        sub_nodes_string = ""
        for s_node in node.sub_nodes_ids:
            sub_nodes_string += " `"+ str(s_node) + "` " 
    embed.add_field(name = "Sub instances", value = sub_nodes_string, inline = False)
    
    #Creating the Field where the Guild Information is visible .
    if isinstance(node,db.WorldNode):
        if node.guild_id != None:
            guild = db.GuildHub.objects.get(guild_id = node.guild_id)
            if guild.privacy_setting == db.GuildPrivacy.CLOSED.value:
                details = "The guild in this locations has its Privacy Setting set to CLOSED and can't be accessed."
            elif guild.privacy_setting == db.GuildPrivacy.OPEN.value:
                details = "**"+guild.name +"** ("+guild.id+")\nUse `!guild_discover` command to ask for an invitation."
            else:
                details = "ALLIANCES NOT IMPLEMENTED YET"
            embed.add_field(name = "Guild" , value = details, inline = False)
    
    #Creating Field for traveling directions
    exits_string = "->"
    if node.north_exit != None:
        exits_string += "`North` "
    if node.east_exit != None:
        exits_string += "`East` "
    if node.south_exit != None:
        exits_string += "`South` "
    if node.west_exit != None:
        exits_string += "`West` "
    if exits_string != "->":
        embed.add_field(name = "Paths" , value = exits_string, inline = False)
    return embed
    
def node_enter(node_id, battler_id):
    this_node = db.Node.objects.no_dereference().get(node_id = node_id)
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    this_node.members.append(battler.to_dbref())
    this_node.save()
    counter = 0
    for mn in pCharac.instance_stack:
        pCharac.instance_stack[counter] = mn.to_dbref()
        counter += 1
    pCharac.enterInstance(this_node.to_dbref())
    try: 
        coords = this_node.coordinates
        pCharac.coordinates = coords
    except:
        pass
    battler.updateCurrentCharacter(pCharac)
    battler.save()
    return node_information(this_node)

def node_exit(battler_id):
    # = db.Node.objects.get(id = node_id)
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    this_node =pCharac.exitInstance()
    counter_inst = 0
    for inst in pCharac.instance_stack:
        pCharac.instance_stack[counter_inst] = inst.to_dbref()
        counter_inst += 1
    try:
        this_node.members.remove(battler.to_dbref())
        counter = 0
        for mn in this_node.members:
            this_node.members[counter] = mn.to_dbref()
            counter += 1
        this_node.save()
    except:
        print("Battler wasn't found in node list. He couldn't be removed")
    battler.updateCurrentCharacter(pCharac)
    battler.save()

def travel_to_node(node_id, battler_id):
    node_exit(battler_id)
    return node_enter(node_id, battler_id)

def node_go_deeper(node_id, battler_id):
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    current_node = pCharac.getInstance()
    try:
        current_node.members.remove(battler.to_dbref())
        counter = 0
        for mn in current_node.members:
            current_node.members[counter] = mn.to_dbref()
            counter += 1
        current_node.save()
    except:
        print("Battler wasn't found in node list. He couldn't be removed")
    return node_enter(node_id, battler_id)

def node_return_upper(battler_id):
    node_exit(battler_id)
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    current_node = pCharac.getInstance()
    counter = 0
    for mn in current_node.members:
        current_node.members[counter] = mn.to_dbref()
        counter += 1
    current_node.members.append(battler.to_dbref())
    
    current_node.save()
    return node_information(current_node)

def getGuildNode(guild_id):
    return db.WorldNode.objects.get(guild_id = guild_id).node_id

def get_battler_coordinates(battler_id):
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    try: 
        return pCharac.coordinates
    except:
        return None

def createNullObject():
    db.Item(name = "null_object").save()

def generateMonsterID():
    num = len(db.Monster.objects)
    date = datetime.datetime.now()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%y")
    return "MON"+str(day)+str(month)+str(year)+str(num)