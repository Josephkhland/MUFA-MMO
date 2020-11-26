import pymongo
import math
import datetime
from enum import Enum
from mongoengine import *

#Connects with the Database
connect('MUFAdatabase', host='localhost', port=27017)

#Creates an array size 15 filled with zeros. Used later for initializations.
array_zero_15 = []
array_zero_24 = []
for i in range(15):
    array_zero_15.append(0)

for i in range(24):
    array_zero_24.append(0)

#Useful function:
def nextLevelEXP(level):
    exponent = 1.5
    baseXP = 100
    return math.floor(baseXP*(level**exponent))


#Classes Declarations
class Battler(Document): meta = {'allow_inheritance': True}
class Monster(Battler): pass
class Player(Battler): pass

class Node(Document): meta = {'allow_inheritance': True}
class WorldNode(Node): pass
class GuildHub(Document): pass

class ArmorSet(Document): pass
class Spell(Document): pass
class Item(Document): meta = {'allow_inheritance': True}
class Armor(Item): pass
class Weapon(Item): pass
class Spellbook(Item): pass
class Artifact(Item): pass

class Battle(Node): pass
class Dungeon(Node): pass

class activeCondition(EmbeddedDocument): pass
class descendant(EmbeddedDocument): pass
class character(EmbeddedDocument): pass

#ENUMERATIONS
class Conditions(Enum):
    POISONED = 0                    #Take 1 Damage per Action, until condition expires.
    BURNING = 1                     #Take 5 Damage per Action, until condition expires. If FROZEN applies, both conditions are removed
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
    CRAFT_UP = 7                    #Increases Crafting chances / Dismantling chances by 10%
    F_EXHAUSTION_RES_UP =8         #Increases Forced Exhaustion damage resistance by 10%
    CONDITION_RES_POISONED = 9     #Increases corresponding condition resistance by 10%
    CONDITION_RES_BURNING = 10
    CONDITION_RES_FROZEN = 11
    CONDITION_RES_PARALYZED = 12
    CONDITION_RES_TERRIFIED = 13
    CONDITION_RES_BLINDED = 14
    CONDITION_RES_DEAFENED = 15
    CONDITION_RES_SILENCED = 16
    CONDITION_RES_CURSED = 17
    CONDITION_RES_BLEEDING = 18
    CONDITION_RES_SLOWED = 19
    CONDITION_RES_WEAKENED = 20
    CONDITION_RES_ASLEEP = 21
    CONDITION_RES_PETRIFIED = 22
    CONDITION_RES_DEAD = 23

class ItemType(Enum):
    HELMET = 0
    CHESTPIECE = 1
    BOOTS = 2
    SLASH = 3
    PIERCE = 4
    CRASH = 5
    RANGED = 6
    ARTIFACT = 7
    SPELLBOOK = 8
    
class GuildPrivacy(Enum):
    CLOSED = 0                      #The Guild can't be entered by those that discover its node. 
    ALLIANCE = 1                    #The Guild can only be entered by Players with a Base within an Allied Guild.
    OPEN = 2                        #The Guild is open and anyone that finds it can enter. 

class PrimaryStat(Enum):
    WIL = 0
    VIT = 1
    AGI = 2
    STR = 3
#Classes definitions

class Item(Document):
    item_id = IntField(primary_key = True)
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
    item_type = IntField( default = 9)
    
    #Special Stats: 
    spell_resistance = IntField(default = 0)                                    #When targeted by a spell, reduce the success chance of it's effect on you by X%
    condition_resistances = ListField(IntField(), default = array_zero_15 )     #When someone attempts to inflict a condition on you, use these to resist.
    forced_exhaustion_resistance = IntField(default = 0)                        #When someone attempts to deal damage to your actions (Exhaustion Damage) use this to resist it.
    
    #Looting
    drop_chance = IntField(default = 0)                                         #Chance of dropping when a character wielding it is killed. 
    
    #Crafting Stats:
    crafting_recipe = ListField(ListField(IntField()), default = [])            #List of Resources required in format List([resource_id, quantity])
    dismantling_difficulty = IntField()                                         #Reduces Chance of acquiring each of its resources upon dismantling.
    value = IntField(default = 0)
    meta = {'allow_inheritance': True}

class activeCondition(EmbeddedDocument):
    name = StringField()
    date_added = DateTimeField()
    duration = IntField()
    

class descendant(EmbeddedDocument):
    will_bonus = IntField( default =1)
    vitality_bonus = IntField( default =1)
    agility_bonus = IntField( default =1)
    strength_bonus = IntField(default =1)
    starting_karma = IntField( default =0)
    character_name = StringField(max_length = 20)

class ArmorSet(Document):
    name = StringField(max_length = 20)
    two_items_set_bonus = ListField(IntField(), default = [0,0,0,0]) #Armor Set Bonus increase [Will, Vitality, Agility, Strength] while equipped.
    full_set_bonus = ListField(IntField(), default = [0,0,0,0])


class character(EmbeddedDocument):
    willpower = IntField(default = 1)
    vitality = IntField(default = 1)
    agility = IntField(default = 1)
    strength = IntField(default = 1)
    money_carried = IntField( default = 0)
    inventory = ListField(ReferenceField(Item), default =[])
    precision_base = IntField( default = 10)
    evasion_base = IntField( default = 10)
    coordinates = ListField(IntField())
    instance_stack = ListField(ReferenceField(Node), default =[])
    conditions = EmbeddedDocumentListField(activeCondition, default =[])
    buffs = EmbeddedDocumentListField(activeCondition, default = [])
    
    #Three values:  armor_equiped[0] -> helmet,
    #               armor_equiped[1] -> chestpiece,
    #               armor_equiped[2] -> boots
    armor_equiped = ListField(ReferenceField(Item), default=[]) 
    armor_set = ReferenceField(ArmorSet)
    set_bonus_specification= IntField(default =0) # 0 for none, 1 for half, 2 for full
    
    #Four values:   weapons_equiped[0] -> slash,   
    #               weapons_equiped[1] -> pierce ,
    #               weapons_equiped[2] -> crash ,
    #               weapons_equiped[3] ->ranged
    weapons_equiped = ListField(ReferenceField(Item), default=[])
    max_actions = IntField(default = 100)
    actions_left = IntField(default = 100)
    karma = IntField(default = 0)
    current_health = IntField( default = 10)
    current_sanity = IntField( default = 10)
    level = IntField(default = 1)
    experience = IntField(default =0)
    exp_to_next_level = IntField(default = nextLevelEXP(1))
    unused_points = IntField(default =0)
    is_dead = BooleanField(default = False)
    imageURL = StringField(default = "https://cdn.discordapp.com/embed/avatars/0.png")
    name = StringField()
    
    spell_resistance = IntField(default = 0)                                    #When targeted by a spell, reduce the success chance of it's effect on you by X%
    condition_resistances = ListField(IntField(), default = array_zero_15 )     #When someone attempts to inflict a condition on you, use these to resist.
    forced_exhaustion_resistance = IntField(default = 0)                        #When someone attempts to deal damage to your actions (Exhaustion Damage) use this to resist it.
    
    
    def getInstance(self):
        return self.instance_stack[-1]
    
    def replaceInstance(self,new_instance):
        self.instance_stack[-1] = new_instance
        return 0
    
    def enterInstance(self, new_instance):
        self.instance_stack.append(new_instance)
        return 0
    
    def exitInstance(self):
        return self.instance_stack.pop()
    
    def checkLevel(self):
        if self.experience > self.exp_to_next_level:
            self.levelUp()
            
    
    def levelUp(self):
        self.level+= 1
        self.experience = self.experience % self.exp_to_next_level
        self.exp_to_next_level = nextLevelEXP(self.level)
        self.unused_points += 1
        self.checkLevel()
    
    def addCondition(self, condition):
        for con in self.conditions:
            if con.name == condition.name:
                if con.duration == -1: return "**"+self.name + "** *is already* `" + con.name +"`"
                if con.duration != -1 and con.duration < condition.duration:
                    con.duration = condition.duration
                con.date_added = condition.date_added
                return "**"+self.name + "** *is now* `" + con.name +"`!"
        self.conditions.append(condition)
        return "**"+self.name + "** *is now* `" + condition.name +"`!"
    
    def kill(self):
        self.current_health = 0
        self.current_sanity = 0
        self.actions_left = 0
        self.is_dead = True
        n_con =  activeCondition(name = 'DEAD',
                 date_added = datetime.datetime.now(),
                 duration = -1)
        return self.addCondition(n_con)

class Node(Document):
    node_id = StringField(primary_key = True)
    sub_nodes_ids = ListField(StringField())
    north_exit = StringField()
    east_exit =  StringField()
    south_exit = StringField()
    west_exit = StringField()
    members = ListField(ReferenceField(Battler))
    entrance_message = StringField(default = "No description Available.")
    resources = ListField(IntField())
    meta = {'allow_inheritance': True}
    

class WorldNode(Node):
    coordinates = ListField(IntField())
    guild_id = StringField(max_length = 20)

class GuildHub(Document):
    guild_id = StringField(primary_key = True)
    name = StringField()
    coordinates = ListField(IntField())
    invites_channel = StringField()
    privacy_setting = IntField(default = GuildPrivacy.CLOSED.value) 
    alliances = ListField(StringField(max_length = 20), default =[])  #List of Guild_ids that this guild is friendly with.
    shop = ListField(ReferenceField(Item), default =[])

class Battler(Document):
    battler_id = StringField(primary_key = True)
    name = StringField()
    faction = IntField()
    creation_date = DateTimeField()
    
    meta = {'allow_inheritance': True}
    def getCharacter(self):
        pass
    def updateCurrentCharacter(self, c):
        pass

class Player(Battler):
    characters_list = EmbeddedDocumentListField(character, default = [])
    active_character = IntField(default =0)
    money_stored = IntField(default =0)
    items_stored = ListField(ReferenceField(Item), default =[])
    descendant_options = EmbeddedDocumentListField(descendant, default = [])
    guild_id = StringField(max_length = 20)
    last_action_date = DateTimeField()
    faction = IntField(default = 0)
    pve_player_limit = IntField(default = 1)
    pve_join_password = StringField() 
    
    def getCharacter(self):
        return self.characters_list[self.active_character]
    
    def updateCurrentCharacter(self, c):
        self.characters_list[self.active_character] = c
        return
    
    def getCharacterByName(self, name):
        for ch in self.characters_list:
            if ch.name == name:
                return ch
        return None
    
    def updateCharacterByName(self, c):
        counter = 0
        for ch in self.characters_list:
            if ch.name == c.name:
                self.characters_list[counter] = c
                return 
            counter +=1
    def getCharacterInNode(self, node_id):
        for c in self.characters_list:
            if c.getInstance().node_id == node_id:
                return c
        return None
    
    def getCurrentNode(self):
        return self.getCharacter().getInstance()
    
    def maxCharacters(self):
        return 6

class Monster(Battler):
    character_stats = EmbeddedDocumentField(character)
    behaviour = IntField() #Monster Behaviors will be figured out later.
    faction = IntField(default = 1)
    def getCharacter(self):
        return self.character_stats
    
    def getCharacterInNode(self, node):
        return self.character_stats

class GhostBattler(Battler):
    previous_id = StringField()
    
    def getCharacter(self):
        return None

class MonsterEntry(Document):
    name = StringField()
    character_stats = EmbeddedDocumentField(character)


class Spell(Document):
    name = StringField(max_length = 50)
    sanity_cost = IntField(default = 0)
    spell_success_rate = IntField(default = 100)            #The success rate of the spell taking effect on a target.
    instance_type = IntField()                              #The instance this spell can be activated Free Roam: 0, Dungeon: 1, Battle: 2
    targets = IntField(default = 1)                         # Special Values: Self -> 0 , ONE_SIDE -> -1 , ALL -> -2
    damage = IntField(default = 0)                          #Negative for Healing.
    on_success_buff_chance = ListField(IntField(), default = array_zero_24)
    on_success_buff_duration = ListField (IntField(), default = array_zero_24)
    on_success_condition_inflict_chance = ListField(IntField(), default = array_zero_15)
    on_success_condition_duration = ListField(IntField(), default = array_zero_15)
    on_success_force_exhaustion_damage = IntField(default = 0)              #Deals damage directly to someone's actions left. (PvP-Only)
    actions_required = IntField(default = 1)                     #The number of actions required to use this spell.
    ingredients = ListField(ListField(IntField()), default = []) #List of Resources required in format List([resource_id, quantity])


    
class Armor(Item):
    armor_set = ReferenceField(ArmorSet)
    evasion_chance_reduction = IntField(default = 0)        #Armor Stat  | Decrease evasion by X%
    physical_damage_reduction_f = IntField (default = 0)    #Armor Stat  | Flat damage reduction from Physical Sources
    magic_damage_reduction_f = IntField(default = 0)        #Armor Stat  | Flat damage reduction from Magical Sources
    physical_damage_reduction_p = IntField(default = 0)     #Armor Stat  | Percentage damage reduction from Physical Sources
    magic_damage_reduction_p = IntField(default = 0)        #Armor Stat  | Percentage damage reduction from Magical Sources
    
    thorn_condition_inflict_chance = ListField(IntField(), default = array_zero_15)     #Upon getting hit, chance of inflicting conditions to attacker.
    thorn_condition_duration = ListField(IntField(), default = array_zero_15)           #Upon getting hit, duration of any condition that gets inflicted to attacker from Thorn effect.
    thorn_force_exhaustion_damage = IntField(default = 0)                                          #Upon getting hit, deals damage to the Attacker's Actions (Exhaustion Damage) (vs Players only)


class Weapon(Item):
    precision_scale = IntField(default = 0)                 #Weapon Stat | For each point in agility this is added to the Precision%
    damage_amp_scale = IntField(default = 0)                #Weapon Stat | For each point in strength this is added to damage_amplification%
    damage_per_amp = IntField(default = 0)                  #Weapon Stat | Amount of Bonus Damage, for each time that the damage is amplified.
    damage_base = IntField(default = 0)                     #Weapon Stat | Base damage that is dealt per Hit. 
    
    on_hit_condition_inflict_chance = ListField(IntField(), default = array_zero_15)    #Upon hitting someone. chance of inflicting conditions to attacker.
    on_hit_condition_duration = ListField(IntField(), default = array_zero_15)          #Upon hitting someone, duration of any inflicting conditions.
    on_hit_force_exhaustion_damage = IntField()                                         #Deals damage directly to someone's actions left. (vs Player only)

class Spellbook(Item):
    spells = ListField(ReferenceField(Spell), default = [])     #Spellbook   | Includes the available spells.   

class Artifact(Item):
    study_requirement = IntField()
    consumable = BooleanField()
    spell = ReferenceField(Spell)
    key_item = BooleanField()

class battlelog(EmbeddedDocument):
    battler = ReferenceField(Battler)
    action_description = StringField()
    timestamp = DateTimeField()

class Battle(Node):
    loot = ListField(ReferenceField(Item))
    money_loot = IntField(default = 0)
    actions_log = EmbeddedDocumentListField(battlelog)
    player_limit = IntField(default = 1)
    join_password = StringField()
    meta = {'allow_inheritance': True}

    def getMember_not_in_faction(self, mid, faction):
        counter = 0
        for member in self.members:
            if member.faction != faction:
                if counter == mid:
                    return member
                counter += 1
        return None
    
    def getEnemies_of_faction(self,faction):
        enemies = []
        for member in self.members:
            if member.faction != faction:
                enemies.append(member)
        return enemies
    

class lock(EmbeddedDocument):
    is_active = BooleanField(default = False)
    key_tag = StringField() #Starts with "SWITCH_" if it's a switch. 
    hack_difficulty = IntField(default = 100)
    demolish_difficulty = IntField(default = 100) 
    inspection_description = StringField()
    tag = StringField()

class trap(EmbeddedDocument):
    is_active = BooleanField(default = False)
    trap_obscurity = IntField(default = 100)
    trap_lethality = IntField(default = 10) #Damage taken when triggered
    hack_difficulty = IntField(default = 100)
    inspection_description = StringField()

class path(EmbeddedDocument):
    lock = EmbeddedDocumentField(lock)
    trap = EmbeddedDocumentField(trap)
    obscurity = IntField(default = 0)
    inspection_description = StringField()
    tag = StringField()

class interactable(EmbeddedDocument):
    lock = EmbeddedDocumentField(lock)
    trap = EmbeddedDocumentField(trap)
    obscurity = IntField(default = 0)
    is_dial = BooleanField(default = False) #When True, the dial can take more than 1 value
    correct_dial_value = IntField(default = 1)
    current_dial_value = IntField(default = 0)
    inspection_description = StringField()
    this_location_string = StringField()
    tag = StringField()
    location_of_lock = StringField()

class Dungeon(Node):
    name = StringField()
    d_name = StringField()
    dungeon_instance = IntField()
    treasure = ListField(ReferenceField(Item), default = [])
    gold_loot = IntField()
    entrance_side = StringField()
    north = EmbeddedDocumentField(path)
    east = EmbeddedDocumentField(path)
    south = EmbeddedDocumentField(path)
    west = EmbeddedDocumentField(path)
    interactables = EmbeddedDocumentListField(interactable, default = [])

class DungeonEntry(Document):
    name = StringField()
    max_monsters = IntField(default = 1)
    current_monsters = IntField(default = 0)
    monsters_list = ListField(StringField(), default = [])
    average_number_of_rooms = IntField(default = 1)
    id_prefix = StringField()
    descriptor_tags = ListField(StringField(),default =[])
    deadends_tags = ListField(StringField(), default = [])
    pathways_tags = ListField(StringField(), default =[])
    existing_instances = IntField(default = 0)
    max_instances_of_dungeon = IntField(default = 1)

class PackageNames(Document):
    name = StringField()

class Tags(Document):
    name = StringField()
    collection = ListField(StringField(), default =[])