import pymongo
from enum import Enum
from mongoengine import *

#Connects with the Database
connect('MUFAdatabase', host='localhost', port=27017)

#Creates an array size 15 filled with zeros. Used later for initializations.
array_zero_15 = []
for i in range(15):
    array_zero_15.append(0)

#Classes Declarations
class WorldNode(Document): pass
class GuildHub(Document): pass
class Player(Document): pass
class ArmorSet(Document): pass
class Spell(Document): pass
class Item(Document): pass
class Monster(Document): pass
class Battler(Document): pass
class Instance(Document): pass
class Dungeon(Document): pass
class activeCondition(EmbeddedDocument): pass
class descendant(EmbeddedDocument): pass
class character(EmbeddedDocument): pass

#ENUMERATIONS
class Conditions(Enum):
    POISONED = 0                    #Take 1 Damage per Action, until condition expires.
    BURNING = 1                     #Take 5 Damage per Action, until condition expires. If FROZEN appliesm, both conditions are removed
    FROZEN = 2                      #Can't move. If attacked with Crash weapon you take double damage but the condition is removed. If BURNING applies both conditions are removed.
    PARALYZED = 3                   #Agility counts as 0 for combat calculations. 
    TERRIFIED = 4                   #Can't use Slash, Pierce or Crash Weapons.
    BLINDED = 5                     #Your Precision is actively 10%
    DEAFENED = 6                    #Your Evasion is 0%
    SILENCED = 7                    #You can't use Spells
    CURSED = 8                      #Your Health doesn't heal up
    BLEEDING = 9                    #Take 1 Damage per Action, until condition expires. Prevents healing. Healing cures the condition.
    SLOWED = 10                     #Agility is halved for any calculations
    WEAKENED = 11                   #Strength is halved for any calculations
    ASLEEP = 12                     #Can't move. Wakes up on Damage or After 1 Hour. 
    PETRIFIED = 13                  #Can't move. Double Crash Damage.
    DEAD = 14                       #Can't move. Can't be healed. Can't be selected as active character.

class Buffs(Enum):
    ARMOR_UP = 0                    #Increases Physical DR_p by 10% and Physical DR_f by 10.
    EVASION_UP = 1                  #Increases Evasion by 5%
    MARMOR_UP = 2                   #Increases Magical DR_p by 10% and Magical DR_f by 10.
    PRECISION_UP = 3                #Increases Precision by 5%
    DAMAGE_UP = 4                   #Increases total DAMAGE you deal by 1%
    KARMA_UP =5                     #Increases Karma by 1%
    SPELL_RES_UP = 6                #Increases Spell Resist by 10 %
    MENTAL_EFF_RES_UP = 7           #Increases Resistance to Effect of a Mental Source by 10%
    PHYSICAL_EFF_RES = 8            #Increases Resistance to Effect of a Physical Source by 10%
    CRAFT_UP = 9                    #Increases Crafting chances / Dismantling chances by 10%
    F_EXHAUSTION_RES_UP =10         #Increases Forced Exhaustion damage resistance by 10%
    CONDITION_RES_POISONED = 11     #Increases corresponding condition resistance by 10%
    CONDITION_RES_BURNING = 12
    CONDITION_RES_FROZEN = 13
    CONDITION_RES_PARALYZED = 14
    CONDITION_RES_TERRIFIED = 15
    CONDITION_RES_BLINDED = 16
    CONDITION_RES_DEAFENED = 17
    CONDITION_RES_SILENCED = 18
    CONDITION_RES_CURSED = 19
    CONDITION_RES_BLEEDING = 20
    CONDITION_RES_SLOWED = 21
    CONDITION_RES_WEAKENED = 22
    CONDITION_RES_ASLEEP = 23
    CONDITION_RES_PETRIFIED = 24
    CONDITION_RES_DEAD = 25
    
class GuildPrivacy(Enum):
    CLOSED = 0                      #The Guild can't be entered by those that discover its node. 
    ALLIANCE = 1                    #The Guild can only be entered by Players with a Base within an Allied Guild.
    OPEN = 2                        #The Guild is open and anyone that finds it can enter. 

#Classes definitions

class WorldNode(Document):
    coordinates = ListField(IntField())
    guild_id = StringField(max_length = 20)
    dungeon_id = StringField(max_length = 20)
    resources_id = ListField(IntField(), default = [])

class GuildHub(Document):
    coordinates = ListField(IntField())
    privacy_setting = IntField(default = GuildPrivacy.CLOSED.value) 
    alliances = ListField(StringField(max_length = 20), default =[])  #List of Guild_ids that this guild is friendly with.

class Player(Document):
    name = StringField()
    characters_list = ListField(EmbeddedDocumentField(character), default = [])
    active_character = IntField()
    money_stored = IntField()
    items_stored = ListField(ReferenceField(Item))
    descendant_options = ListField(EmbeddedDocumentField(descendant), default = [])
    guild_id = StringField(max_length = 20)
    last_action_date = DateTimeField()    

class ArmorSet(Document):
    name = StringField(max_length = 20)
    two_items_set_bonus = ListField(IntField(), default = [0,0,0,0]) #Armor Set Bonus increase [Will, Vitality, Agility, Strength] while equipped.
    full_set_bonus = ListField(IntField(), default = [0,0,0,0])

class Spell(Document):
    name = StringField(max_length = 50)
    sanity_cost = IntField()
    spell_success_rate = IntField(default = 100)            #The success rate of the spell taking effect on a target.
    instance_type = IntField()                              #The instance this spell can be activated Free Roam: 0, Dungeon: 1, Battle: 2
    targets = IntField(default = 1)                         # Special Values: Self -> 0 , ONE_SIDE -> -1 , ALL -> -2
    damage = IntField(default = 0)                          #Negative for Healing.
    on_success_buff_chance = ListField(IntField())
    on_success_buff_duration = ListField (IntField())
    on_success_condition_inflict_chance = ListField(IntField(), default = array_zero_15)
    on_success_condition_duration = ListField(IntField(), default = array_zero_15)
    on_success_force_exhaustion_damage = IntField()              #Deals damage directly to someone's actions left. (PvP-Only)
    actions_required = IntField(default = 1)                     #The number of actions required to use this spell.

class Item(Document):
    name = StringField(max_length = 50)
    #item_types:    0 -> helmet (armor), 
    #               1 -> chestpiece (armor),
    #               2 -> boots (armor),
    #               3 -> slash (weapon)
    #               4 -> pierce (weapon)
    #               5 -> crash (weapon)
    #               6 -> ranged (weapon)
    #               7 -> artifact (use from inventory)
    #               8 -> spellbook
    item_type = IntField()
    weight = IntField()
    
    armor_set = ReferenceField(ArmorSet)
    evasion_chance_reduction = IntField(default = -1)        #Armor Stat  | Decrease evasion by X%
    physical_damage_reduction_f = IntField (default = -1)    #Armor Stat  | Flat damage reduction from Physical Sources
    magic_damage_reduction_f = IntField(default = -1)        #Armor Stat  | Flat damage reduction from Magical Sources
    physical_damage_reduction_p = IntField(default = -1)     #Armor Stat  | Percentage damage reduction from Physical Sources
    Magic_damage_reduction_p = IntField(default = -1)        #Armor Stat  | Percentage damage reduction from Magical Sources
    
    precision_scale = IntField(default = -1)                 #Weapon Stat | For each point in agility this is added to the Precision%
    damage_amp_scale = IntField(default = -1)                #Weapon Stat | For each point in strength this is added to damage_amplification%
    damage_per_amp = IntField(default = -1)                  #Weapon Stat | Amount of Bonus Damage, for each time that the damage is amplified.
    damage_base = IntField(default = -1)                     #Weapon Stat | Base damage that is dealt per Hit. 
    
    spells = ListField(ReferenceField(Spell), default = [])     #Spellbook   | Includes the available spells.   
    
    #Special Stats: 
    spell_resistance = IntField(default = 0)                 #When targeted by a spell, reduce the success chance of it's effect on you by X%
    mental_effect_resistance = IntField(default = 0)         #When targeted by an effect that is tagged as Mental, you add this to your resistance.
    physical_effect_resistance = IntField(default = 0)       #When targeted by an effect that is tagged as Physical, you add this to your resistance 
    condition_resistances = ListField(IntField(), default = array_zero_15 )
    forced_exhaustion_resistance = IntField(default = 0)
    
    on_hit_condition_inflict_chance = ListField(IntField(), default = array_zero_15)
    on_hit_condition_duration = ListField(IntField(), default = array_zero_15)
    on_hit_force_exhaustion_damage = IntField()              #Deals damage directly to someone's actions left. (PvP-Only)
    drop_chance = IntField(default = 0)                      #Chance of dropping when a character wielding it is killed. 
    
    #Crafting Stats:
    crafting_recipe = ListField(ListField(IntField()), default = [])            #List of Resources required in format List([resource_id, quantity])
    dismantling_difficulty = IntField()                      #Reduces Chance of acquiring each of its resources upon dismantling.

class Monster(Document):
    name = StringField()
    monster_type = IntField()
    character_stats = EmbeddedDocumentField(character)
    spawn_date =  DateTimeField()
    behaviour = IntField() #Monster Behaviours will be figured out later.

class Battler(Document):                
    player_entity = ReferenceField(Player)
    monster_entity = ReferenceField(Monster)

class Instance(Document):
    instance_type = IntField()
    participants_side_A = ListField(ReferenceField(Battler), default = [])
    participants_side_B = ListField(ReferenceField(Battler), default = [])
    actions_log = ListField(StringField(), default = [])

#class Dungeon(Document):
    #To Be created

class activeCondition(EmbeddedDocument):
    name = StringField()
    date_added = DateTimeField()
    duration = IntField()

class descendant(EmbeddedDocument):
    will_bonus = IntField()
    vitality_bonus = IntField()
    agility_bonus = IntField()
    strength_bonus = IntField()
    starting_karma = IntField()
    mutations = ListField(IntField(), default = [])
    character_name = StringField(max_length = 20)
    
class character(EmbeddedDocument):
    willpower = IntField()
    vitality = IntField()
    agility = IntField()
    strength = IntField()
    money_carried = IntField()
    inventory = ListField(ReferenceField(Item), default =[])
    precision_base = IntField()
    evasion_base = IntField()
    coordinates = ListField(IntField())
    instance_stack = ListField(ReferenceField(Instance), default =[])
    conditions = ListField(EmbeddedDocumentField(activeCondition))
    
    #Three values:  armor_equiped[0] -> helmet,
    #               armor_equiped[1] -> chestpiece,
    #               armor_equiped[2] -> boots
    armor_equiped = ListField(ReferenceField(Item)) 
    
    #Four values:   weapons_equiped[0] -> slash,   
    #               weapons_equiped[1] -> pierce ,
    #               weapons_equiped[2] -> crash ,
    #               weapons_equiped[3] ->ranged
    weapons_equiped = ListField(ReferenceField(Item))
    actions_left = IntField()
    karma = IntField()
    age = IntField()
    current_health = IntField()
    current_sanity = IntField()
    name = StringField()