import random
import re
import mufadb as db 
import mufa_world as mw

def monster(noderef):
    all_monsters_list = db.MonsterEntry.objects.no_dereference()
    selection = random.randint(0,len(all_monsters_list)-1)
    n_char = all_monsters_list[selection].character_stats
    n_char.enterInstance(noderef)
    mon_id = mw.generateMonsterID()
    db.Monster(battler_id = mon_id, name = n_char.name , character_stats = n_char).save()
    return db.Monster.objects.no_dereference.get(battler_id = mon_id).to_dbref()

def spawn_monster_in_dungeon(noderef, name_of_monster_to_spawn):
    monster = db.MonsterEntry.objects.no_dereference().get(name = name_of_monster_to_spawn)
    n_char = monster.character_stats
    n_char.enterInstance(noderef)
    mon_id = mw.generateMonsterID()
    db.Monster(battler_id = mon_id, name = n_char.name , character_stats = n_char).save()
    return db.Monster.objects.no_dereference.get(battler_id = mon_id).to_dbref()

def global_monsters_generate():
    all_world_nodes = db.WorldNode.objects.no_dereference()
    world_size = len(all_world_nodes)
    MAX_MONSTERS = 10000
    this_size = len(db.Monster.objects.no_dereference())
    monsters_to_add = max(MAX_MONSTERS - this_size,0)
    for i in range(monsters_to_add):
        location = random.randint(0,len(world_size)-1)
        node_val = all_world_nodes[location] 
        noderef = all_world_nodes[location].to_dbref()
        battler_added = monster(noderef)
        node_val.members.append(battler_added)
        node_val.save()
        
def dungeon_monsters_generate():
    all_dungeon_entries = db.DungeonEntry.objects
    for dungeon in all_dungeon_entries:
        if dungeon.max_monsters <= dungeon.current_monsters:
            continue
        else:
            monsters_to_spawn = dungeon.max_monsters - dungeon.current_monsters
            dungeon_rooms = db.Dungeon.objects(d_name= dungeon.name).no_dereference()
            total_rooms = len(dungeon_rooms)
            for i in range(monsters_to_spawn):
                room =  random.randint(0, total_rooms -1)
                monster_selection = random.randint(0,len(dungeon.monsters_list)-1)
                node_val = dungeon_rooms[room] 
                noderef = dungeon_rooms[room].to_dbref()
                battler_added = spawn_monster_in_dungeon(noderef, dungeon.monsters_list[monster_selection])
                node_val.members.append(battler_added)
                node_val.save()
            dungeon.current_monsters = dungeon.max_monsters
            dungeon.save()


def gen_dungeon_id(dungeon_tag, x,y):
    x_value = str(abs(x)).zfill(3)
    y_value = str(abs(y)).zfill(3)
    if x < 0:
        x_value = "N" + x_value[1:]
    if y < 0:
        y_value = "N" + y_value[1:]
    final = dungeon_tag +":X"+ x_value +"Y"+ y_value + "E"
    return final



def getRoomCoords(room_id):

    def denegafy(match):
        value : int 
        if match[0] == "N":
            value = - int(match[1:2])
        else:
            value = int(match)
        return value

    regexFilter_x = r"(?!\:[X])\w\w\w(?=[E])"
    regexFilter_y = r"(?!\:[Y])\w\w\w(?=[E])"
    x_match = re.search(regexFilter_x, room_id).string
    y_match = re.search(regexFilter_y, room_id).string
    x = denegafy(x_match)
    y = denegafy(y_match)
    return x, y

def generate_trap(level):
    trap_lethality_calc = 0
    pukoucoo = random.randint(0,100)
    active = False
    if pukoucoo > 70:
        active = True
    for i in range(level):
        trap_lethality_calc += random.randint(1,10) 
    trap_obj = db.trap(is_active = active,
                       trap_obscurity = random.randint(0,100),
                       trap_lethality = trap_lethality_calc,
                       hack_difficulty = random.randint(10,100),
                       inspection_description = "A dangerous trap")
    return trap_obj

def generate_lock(key_id):
    active = True
    if key_id == "NONE":
        active = False   
    lock_obj = db.lock( is_active = active,
                        key_tag = key_id,
                        hack_difficulty = random.randint(0,100),
                        inspection_description = "There is a lock here")
    return lock_obj
    
def generate_interactable(dungeon_entry, level, node_id, index):
    key_tag = node_id + "::" + str(index)
    tag = random.choice(dungeon_entry.descriptor_tags)
    ## Come up with what to do about dials and generating the puzzle part
    inter_obj = db.interactable( lock = generate_lock("NONE"),
                                 trap = generate_trap(level),
                                 obscurity = random.randint(0,100),
                                 inspection_description = "Beep Boop Rapati Papapa",
                                 key_tag = key_tag)
                                 

def room_exists(dungeon_tag, x, y):
    gid = gen_dungeon_id(dungeon_tag,x,y)
    if len(db.Dungeon.objects(node_id = gid)) == 0:
        return False
    else:
        return True

def generate_dungeon(dungeon_name):
    d_entry = db.DungeonEntry.objects.get(name = dungeon_name)
    rooms_to_create = d_entry.average_number_of_rooms + random.randint(-5, 5) 
    rooms_to_create = max(rooms_to_create, 1)
    keys_in_place = []
    blank_paths = 4
    generate_room(d_entry, 0,rooms_to_create,blank_paths,0,0, keys_in_place)   


def generate_room(d_entry, entering_from, rooms_to_create, blank_paths, x, y, lock_keys, previous_room_id="NONE"):
    all_paths = [1,2,3,4]
    try: 
        all_paths.remove(entering_from)
    except:
        pass
    paths_chosen = []
    max_rooms_to_create = min(rooms_to_create, 3)
    if entering_from == 0:
        max_rooms_to_create = min(rooms_to_create, 4)
    paths_this_node = random.randint(0,max_rooms_to_create)
    blank_paths -= paths_this_node
    blank_paths += 3*paths_this_node
    rooms_to_create -= paths_this_node
    if blank_paths == 0 and rooms_to_create>0:
        paths_this_node += 1
        blank_paths += 3
        rooms_to_create -= 1
    for a in range(paths_this_node):
        index = random.randint(0,len(all_paths)-1)
        paths_chosen.append(all_paths.pop(index))
    n_id = gen_dungeon_id(d_entry.id_prefix, x, y)
    room_obj = db.Dungeon( name = "Room ",
                           d_name = d_entry.name,
                           node_id = n_id).save()
                               
    for r_direction in paths_chosen:
        if r_direction == 1:
            room_obj.north_exit = gen_dungeon_id(d_entry.id_prefix,x, y +1)
            if room_exists(d_entry.id_prefix, x, y+1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x, y+1, n_id)
        elif r_direction == 2:
            room_obj.east_exit = gen_dungeon_id(d_entry.id_prefix,x+1, y)
            if room_exists(d_entry.id_prefix, x+1, y):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x+1, y, n_id)
        elif r_direction == 3:
            room_obj.south_exit = gen_dungeon_id(d_entry.id_prefix,x, y -1)
            if room_exists(d_entry.id_prefix, x, y-1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x, y-1, n_id)
        elif r_direction == 4:
            room_obj.west_exit = gen_dungeon_id(d_entry.id_prefix,x-1, y )
            if room_exists(d_entry.id_prefix, x, y-1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x-1, y, n_id)
    if entering_from == 1:
        #Entering from South ↑
        room_obj.south_exit = previous_room_id
    elif entering_from == 2:
        #Entering from West: →
        room_obj.west_exit = previous_room_id
    elif entering_from == 3:
        #Entering from North:↓
        room_obj.north_exit = previous_room_id
    elif entering_from == 4:
        #Entering from East: ←
        room_obj.east_exit = previous_room_id
    
    return rooms_to_create, blank_paths

def flood_with_monsters():
    dungeon_monsters_generate()
    global_monsters_generate()

class DescriptionGen:
    def __init__(self):
        self.fluff = ["sketchily-drawn", "rough", "minimalistic", "simple", "carefully-drawn, hastily-drawn, elaborate"]
        self.verbs = ["painted","engraved", "carved", "drawn", "glued", "scorched","stiched"] 
        self.position = ["floor, adjacent to the", "wall, adjacent to the", "surface of the"]
        self.position_prefix = ["on the", "upon the", "over the", "over a segment of the"]
        self.adverb = ["hastily", "carefully", "roughly", "poorly", "artistically", "elaborately"]
        self.afterv = ["presented","expressed","delivered","demonstrated", "pictured", "illustrated"]
        pass

    def starts_with_vowel(self,s):
        try:
            vowels = ['a','e','i','o','u','y']
            return s[0] in vowels
        except:
            return None

    def insert_a_article(self,s):
        if self.starts_with_vowel(s):
            return "an "+ s

    def express_shape(self,s):
        synonyms = ["shape", "symbol"]
        shape_syn = random.choice(synonyms)
        return shape_syn+ " of " + self.insert_a_article(s)

    def enrich_shape(self,s):
        adj = random.choice(self.fluff)
        return adj + " " + self.express_shape(s)

    def diverse_action(self):
        adv = random.choice(self.adverb)
        v = random.choice(self.verbs)
        return adv + " " + v

    def express_position(self, t, suffix = ", "):
        p = random.choice(self.position)
        pre = random.choice(self.position_prefix)
        return pre + " " + p + " " + t + suffix
    
    def interactable_description(self,tag,symbol):
        result : str
        b,c = " "
        choice = random.randint(0,5)

        if choice == 0:
            #String there is a + self.enrich_shape(s)
            result = random.choice(self.verbs) + b + self.express_position(tag)+"there is the " + self.enrich_shape(symbol) + "."
        elif choice ==1: 
            #String pre_enriched + ", there is the " + self.express_shape(s)
            result = self.diverse_action() + b + self.express_position(tag)+ "there is the " + self.express_shape(symbol) + "."
        elif choice ==2:
            #String pre_enriched + ", the " + self.express_shape(s) + " is expressed."
            result = self.diverse_action() + b + self.express_position(tag)+ "the " + self.express_shape(symbol) + " is" +random.choice(self.afterv) +"."
        elif choice ==3:
            #The surface of the {}, is occupied by the + self.enrich_shape(s)
            result = "The" + self.express_position(tag) + "is occupied by the " + self.enrich_shape(symbol) +"."
        elif choice ==4:
            #On the wall adjacent to the {}, the {symbol} is {enrich_action} painted
            result = self.express_position(tag)+"the " +self.express_shape(symbol) + " is " + self.diverse_action() +"."
        elif choice ==5:
            #The symbol of a sun is {diverse action} over the surface of the {}.
            result = "The "+ self.enrich_shape(symbol) + " is " + self.diverse_action() + b + self.express_position(tag, ".") 
        return result


def generateDescription():
    all_symbols = db.Tags.objects.get(name = "Symbols").collection
    all_decorators = db.Tags.objects.get(name = "Decorators").collection
    symbol = random.choice(all_symbols)
    decorator = random.choice(all_decorators)
    result = DescriptionGen().interactable_description(decorator,symbol)
    print(result)
    return result