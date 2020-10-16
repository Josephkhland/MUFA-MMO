import pymongo
from mongoengine import *

connect('MUFAdatabase', host='localhost', port=27017)


#Classes declarations

class WorldNode(Document):
    coordinates = ListField(IntField())
    guild_id = StringField(max_length = 20)
    dungeon_id = StringField(max_length = 20)
    resources_id = ListField(IntField(), default = [])
    
    #def __init__(self, coords : (int,int), guild_id : str = None , dungeon_id : str = None)   
    #    self.coordinates = coords,
    #    self.guild_id = guild_id ,
    #    self.dungeon_id= dungeon_id,



new_guild_hub = {
    "_id" : '=guild_id',
    "coordinates" : (0,0),
    "privacy_setting" : "CLOSED", #This setting determines whether this guild can be accessed from the world map CLOSED|OPEN|ALLIANCE
    "alliances": [] #List of Guild_ids that this guild is friendly with.
    #MUST DESIGN OTHER VARIABLES
}

new_descendant_parameters = {
    "will_bonus" : 0,
    "vitality_bonus" : 0,
    "agility_bonus" : 0,
    "strength_bonus" : 0,
    "starting_karma" : 0,
    "mutations" : [],
    "character_name" : 'name', #Name is selected upon birth of a new descendant option.
}

new_player = {
    "_id" : '=user_id',
    "characters_list" : [],
    "money_stored" : 0,
    "items_stored" : [],
    "descendant_options" : [new_descendant_parameters],
    "guild" : '=guild_id where Home is based'
}

new_character = {
    "willpower" : 10,
    "vitality" : 10,
    "agility" : 10,
    "strength" : 10,
    "money_carried" : 0,
    "inventory" : [],
    "armor_equiped" : {"helmet": None, "chestpiece" : None , "boots" : None},
    "weapons_equiped" : {"slash" : None, "pierce" : None , "crash" : None , "ranged" : None } ,
    "precision_base" : 0,
    "evasion_base" : 0,
    "coordinates" : (0,0),
    "instance_stack" : []
}

new_armor_piece: {
    "_id": 'unique id' ,
    "name": 'item name -> Concat(material + type + "of armor_set.name")', #Example : Diamond helmet of Cilanthis
    "type": 'helmet | chestpiece | boots' ,
    "armor_set_id" : '_id of the armor set it belongs',
    "evasion_chance_reduction" :  0,    #Decrease evasion by X% 
    "physical_damage_reduction_f" : 0,  #Flat
    "magic_damage_reduction_f": 0,      #Flat
    "physical_damage_reduction_p" : 0,  #Percentage
    "magic_damage_reduction_p" : 0      #Percentage
}

new_weapon: {
    "_id" : 'unique_id',
    "name" : 'item name',
    "type" : 'slash | pierce| crash | ranged',
    "precision_scale" : 0, #For each point in agility this is added to the precision%.
    "damage_amp_scale" : 0, #For each point in strength this is added to damage_amplification%
    "damage_per_amp" : 0 , #Bonus damage each time the damage is amplified.
    "damage_base" : 0 #Damage dealt with each hit.
}

new_armor_set: {
    "_id" : 'unique_id',
    "name" : 'Set_name',
    "two_items_set_bonus" : {"willpower": 0 , "vitality": 0, "agility": 0 , "strength": 0},
    "full_set_bonus" : {"willpower": 0 , "vitality": 0, "agility": 0 , "strength": 0}   
}

new_battle_instance: {
    "_id" : 'unique_id',
    "participants_side_A" : [],
    "participants_side_B" : [],
    "actions_taken" : []
}