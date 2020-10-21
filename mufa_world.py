import pymongo
import random
import mongoengine
import mufadb as db 
import mufa_constants as mconst
import time 

def generate():
    for i in range(mconst.world_size.get('x')):
        for j in range(mconst.world_size.get('y')):
            db.WorldNode(coordinates = [i,j]).save()
    
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
    
def insert_guild(guild_to_add : str):
    list_of_free_nodes = []
    for node in db.WorldNode.objects(guild_id=None):
        list_of_free_nodes.append(node.coordinates)
    node_to_fill = random.randint(0,len(list_of_free_nodes)-1)
    db.WorldNode.objects(coordinates=list_of_free_nodes[node_to_fill]).update(set__guild_id = guild_to_add)
    db.GuildHub(guild_id= guild_to_add, coordinates = list_of_free_nodes[node_to_fill]).save()

def remove_guild(guild_to_remove : str):
    db.WorldNode.objects(guild_id = guild_to_remove).update(set__guild_id = None)
    db.GuildHub.objects(guild_id = guild_to_remove).delete()
    db.GuildHub.objects(alliances__S =guild_to_remove).update(set__alliances__S = None)

def visualize():
    list_of_nodes = []
    for node in db.WorldNode.objects():
        if node.guild_id != None : list_of_nodes.append(1)
        else : list_of_nodes.append(0)
    return list_of_nodes
    
def node_enter(node_id, battler_id):
    this_node = db.Node.objects.get(id = node_id)
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    this_node.members.append(battler.to_dbref())
    this_node.save()
    pCharac.enterInstance(this_node.to_dbref())
    try: 
        coords = this_node.coordinates
        pCharac.coordinates = coords
    except:
        pass
    battler.updateCurrentCharacter(pCharac)
    battler.save()

def node_exit(node_id, battler_id):
    this_node = db.Node.objects.get(id = node_id)
    battler = db.Battler.objects.get(battler_id = battler_id)
    pCharac = battler.getCharacter()
    pCharac.exitInstance()
    try:
        this_node.members.remove(battler.to_dbref())
        this_node.save()
    except:
        print("Battler wasn't found in node list. He couldn't be removed")
    battler.updateCurrentCharacter(pCharac)
    battler.save()

def travel_to_node(node_id, battler_id):
    node_exit(node_id, battler_id)
    node_enter(node_id, battler_id)