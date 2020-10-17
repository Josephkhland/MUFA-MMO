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
    
def insert_guild(guild_to_add : str):
    list_of_free_nodes = []
    for node in db.WorldNode.objects(guild_id=None):
        #if node.guild_id == None:
        list_of_free_nodes.append(node.coordinates)
    node_to_fill = random.randint(0,len(list_of_free_nodes)-1)
    #print(list_of_free_nodes)
    #print("Node Selected: "+str(list_of_free_nodes[node_to_fill]))
    db.WorldNode.objects(coordinates=list_of_free_nodes[node_to_fill]).update(set__guild_id = guild_to_add)

def remove_guild(guild_to_remove : str):
    db.WorldNode.objects(guild_id = guild_to_remove).update(set__guild_id = None)

def visualize():
    list_of_nodes = []
    for node in db.WorldNode.objects():
        if node.guild_id != None : list_of_nodes.append(1)
        else : list_of_nodes.append(0)
    return list_of_nodes