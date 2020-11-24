import random
import descriptions
import re
import math
import mufadb as db 
import mufa_world as mw
import mufa_constants as mc

def monster(noderef):
    all_monsters_list = db.MonsterEntry.objects.no_dereference()
    selection = random.choice(all_monsters_list)
    n_char = selection.character_stats
    n_char.enterInstance(noderef)
    mon_id = mw.generateMonsterID()
    db.Monster(battler_id = mon_id, name = n_char.name , character_stats = n_char).save()
    return db.Monster.objects.no_dereference().get(battler_id = mon_id).to_dbref()

def spawn_monster_in_dungeon(noderef, name_of_monster_to_spawn):
    monster = db.MonsterEntry.objects.no_dereference().get(name = name_of_monster_to_spawn)
    n_char = monster.character_stats
    n_char.enterInstance(noderef)
    mon_id = mw.generateMonsterID()
    db.Monster(battler_id = mon_id, name = n_char.name , character_stats = n_char).save()
    return db.Monster.objects.no_dereference().get(battler_id = mon_id).to_dbref()

def global_monsters_generate():
    print("DEBUG - 0")
    all_world_nodes = db.WorldNode.objects.no_dereference()
    print("DEBUG - 1")
    world_size = len(all_world_nodes)
    MAX_MONSTERS = mc.MAX_MONSTERS
    this_size = len(db.Monster.objects.no_dereference())
    monsters_to_add = min(max(MAX_MONSTERS - this_size,0),10*len(db.Player.objects.no_dereference()))
    for i in range(monsters_to_add):
        location = random.randint(0,world_size-1)
        node_val = all_world_nodes[location] 
        noderef = all_world_nodes[location].to_dbref()
        battler_added = monster(noderef)
        node_val.members.append(battler_added)
        node_val.save()
    print(str(monsters_to_add) +" MONSTERS WERE GENERATED IN THE WORLD!")
    return
        
def dungeon_monsters_generate():
    all_dungeon_entries = db.DungeonEntry.objects
    gens_counter = 0
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
            gens_counter += monsters_to_spawn
    print(str(gens_counter) + " MONSTERS WERE GENERATED IN DUNGEONS")
    return


def gen_dungeon_id(dungeon, x,y):
    dungeon_tag = dungeon.id_prefix + str(dungeon.existing_instances)
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
                                 

def room_exists(dungeon, x, y):
    gid = gen_dungeon_id(dungeon,x,y)
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
    d_entry.existing_instances += 1   
    d_entry.save()
    return d_entry.existing_instances - 1 


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
    n_id = gen_dungeon_id(d_entry, x, y)
    room_obj = db.Dungeon( name = "Room",
                           d_name = d_entry.name,
                           node_id = n_id,
                           dungeon_instance = d_entry.existing_instances
                        ).save()
                               
    for r_direction in paths_chosen:
        print("\n"+n_id)
        print("Rooms to create: " + str(rooms_to_create))
        print("Paths to Fill: " + str(blank_paths))
        if r_direction == 1:
            room_obj.north_exit = gen_dungeon_id(d_entry,x, y +1)
            if room_exists(d_entry, x, y+1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x, y+1, [], n_id)
        elif r_direction == 2:
            room_obj.east_exit = gen_dungeon_id(d_entry,x+1, y)
            if room_exists(d_entry, x+1, y):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x+1, y, [], n_id)
        elif r_direction == 3:
            room_obj.south_exit = gen_dungeon_id(d_entry,x, y -1)
            if room_exists(d_entry, x, y-1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x, y-1,[], n_id)
        elif r_direction == 4:
            room_obj.west_exit = gen_dungeon_id(d_entry,x-1, y )
            if room_exists(d_entry, x, y-1):
                blank_paths -= 3 
                rooms_to_create += 1
            else:
                rooms_to_create, blank_paths = generate_room(d_entry, r_direction, rooms_to_create, blank_paths, x-1, y, [], n_id)
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
    
    room_obj.save()
    return rooms_to_create, blank_paths

def flood_with_monsters():
    dungeon_monsters_generate()
    global_monsters_generate()


class Puzzle:
    def __init__(self, number_of_keys=1):
        self.array = list(range(0,number_of_keys))
    
    def find_legal(self, value, arr):
        outcome = set()
        for slot in arr:
            if type(slot) is tuple:
                if slot[1] == value:
                    continue
                else: 
                    outcome = outcome.union(self.find_legal(value, slot[0]))
            else:
                if slot == value:
                    continue
                outcome.add(slot)
        return outcome

    def get_deepest(self, target):
        if type(target) is tuple:
            return self.get_deepest(target[0])
        elif type(target) is list:
            return target[0]
        else:
            return target

    def set_deepest(self, target, key_to_save):
        if type(target) is tuple:
            return ([self.set_deepest(target[0], key_to_save)],target[1])
        elif type(target) is list:
            return ([target[0]], key_to_save)
        else:
            return ([target] , key_to_save)

    def key_gen(self, value):
        all_legal = self.find_legal(value, self.array)
        return random.choice(tuple(all_legal))

    def create_lock(self, arr, index, key):
        value = self.set_deepest(arr[index], key)
        return value

    def randomize(self):
        locks = len(self.array)
        new_array = self.array
        for i in range(locks):
            selection = random.randint(0,locks-1)
            key = self.key_gen(self.array[selection])
            new_array[selection] = self.create_lock(new_array, selection, key)
        return new_array
    
def test_random_puzzle(size):
    p = Puzzle(size).randomize()
    print (p)
    return p

def do_nothing(arg):
    if isinstance(arg, db.Dungeon):
        print("\n"+arg.node_id)
        north =arg.north_exit
        if arg.north_exit == None:
            north = "None"
        print("north_exit: " + north)

        east =arg.east_exit
        if arg.east_exit == None:
            east = "None"
        print("east_exit: " + east)

        south =arg.south_exit
        if arg.south_exit == None:
            south = "None"
        print("south_exit: " + south)

        west =arg.west_exit
        if arg.west_exit == None:
            west = "None"
        print("west_exit: " + west)
    else:
        print("function argument has no attribute name") 

def print_room(room, fake_variable):
    print("\n")
    print(room.name)
    north =room.north_exit
    if room.north_exit == None:
        north = "None"
    print("North Path: " + north)
    print("#### Lock Key_Tag: "+ room.north.lock.key_tag)
    east =room.east_exit
    if room.east_exit == None:
        east = "None"
    print("East Path: " + east)
    print("#### Lock Key_Tag: "+ room.east.lock.key_tag)
    south =room.south_exit
    if room.south_exit == None:
        south = "None"
    print("South Path: "+ south)
    print("#### Lock Key_Tag: "+ room.south.lock.key_tag)
    west =room.west_exit
    if room.west_exit == None:
        west = "None"
    print("West Path: "+ west)
    print("#### Lock Key_Tag: "+ room.west.lock.key_tag)
    print("\n")
    print("===Interactables===")
    for i in room.interactables:
        print("ID: "+ i.this_location_string)
        print("Unlocks: " + i.location_of_lock)
        print("#### Lock Key_Tag: "+ i.lock.key_tag)
        print("#### Description: "+ i.inspection_description)
        print("-------------------\n")
    print("###########################")
    pass

class MapTraversal:
    def __init__(self , name, d_id):
        self.name = name 
        self.all_rooms = db.Dungeon.objects(d_name = name, dungeon_instance = d_id).no_dereference()
        self.number_of_rooms = len(self.all_rooms)
        temp = random.randint(1,5)
        variance = random.randint(-1,1)
        self.max_interactables = int(math.ceil(self.number_of_rooms/temp)) + variance
        self.num_interactables = 0
        self.used_interactables = []
        self.rooms_visited = []
        self.entrance = random.choice(self.all_rooms)
        self.rooms_dict = {} 
    
    def getNode(self, room_id):
        try: 
            return self.all_rooms.get(node_id = room_id)
        except:
            return "DoesNotExist"

    def insert_interactables(self,room,interacts_from_previous):
        left_to_add = self.max_interactables - self.num_interactables
        rooms_left = self.number_of_rooms - len(self.rooms_visited)
        attach_to_next = []
        if left_to_add == 0:
            pass
        else:
            max_inter_to_try = random.randint(1,left_to_add)
            count_added = 0
            for times in range(max_inter_to_try):
                chance = 100/max(1,rooms_left)
                determiner = random.randint(0,100)
                if chance > determiner:
                    #CREATE INTERACTABLE
                    
                    #Obscurity Calculation
                    determine_if_hidden = random.randint(0,1)
                    if determine_if_hidden == 0:
                        obs_to_give = 0
                    else:
                        obs_to_give = random.randint(1,100)
                    
                    #Dial options calculation
                    determine_if_dial = random.randint(0,1)
                    if determine_if_dial == 0:
                        is_dial_to_give = False
                        correct_dial_v= 1
                    else:
                        is_dial_to_give = True
                        correct_dial_v= random.randint(1,12)
                    
                    #Tag Selection & Description
                    dungeon = db.DungeonEntry.objects.get(name = room.d_name)
                    symbol_list = db.Tags.objects.get(name = "Symbols")
                    
                    tag_to_give = random.choice(dungeon.descriptor_tags)
                    symbol = random.choice(symbol_list.collection)
                    insp_desc_to_give = descriptions.DescriptionGen().interactable_description(tag_to_give,symbol)

                    #Calculate this Location
                    loc_string = room.node_id + "::" + str(count_added) +"::"+symbol

                    new_interact = db.interactable(
                        obscurity = obs_to_give,
                        is_dial = is_dial_to_give,
                        correct_dial_value = correct_dial_v,
                        tag = tag_to_give,
                        inspection_description = insp_desc_to_give,
                        this_location_string = loc_string,
                        location_of_lock = "UNKNOWN"
                    )
                    room.interactables.append(new_interact)
                    room.save()
                    attach_to_next.append(loc_string)
                    count_added += 1
                else:
                    break
        interactables_to_use_in_locks = interacts_from_previous[0] + attach_to_next
        self.rooms_dict[room.node_id] =interactables_to_use_in_locks 

    def analyze_string(self, s):
        return s.split("::")
    
    def get_interactable(self, s, value=0):
        temp = self.analyze_string(s)
        #value = 0 -> Get node_id
        #value = 1 -> Get index to use for node.interactables[index]
        #value = 2 -> Get symbol.
        if len(temp)> value:
            return temp[value]
        else:
            return "ERROR"
    
    def set_interactable_location(self, s, location):
        info = self.analyze_string(s)
        room = db.Dungeon.objects.no_dereference().get(node_id = info[0])
        room.interactables[int(info[1])].location_of_lock = location
        room.save()

    def createLock(self, room, string_loc):
        difficulties = [30,60,100,150,210]
        should_lock = random.randint(0,100) < 10
        hack_difficulty_tg = random.choice(difficulties)
        demolish_difficulty_tg = random.choice(difficulties)
        location_to_store = room.node_id + "::" + string_loc
        if should_lock:
            available_interactables = self.rooms_dict[room.node_id]
            if available_interactables == None or available_interactables == []: 
                pick = None 
            else:
                pick = random.choice(available_interactables)
            if pick == location_to_store or (pick in self.used_interactables) or pick == None:
                key_tag_tg = "ITEM::"
                tag_tg = "item"
                insp_desc_to_give = "Some description."
            else: 
                key_tag_tg = "SWITCH::"+ location_to_store
                tag_tg = self.get_interactable(location_to_store,2)
                #insp_desc_to_give = descriptions.DescriptionGen().lock_description(tag_to_give,symbol)
                insp_desc_to_give = "Clue: " + tag_tg
                self.used_interactables.append(pick)
                self.set_interactable_location(pick,location_to_store)

        else:
            key_tag_tg = "NONE" #There isn't actually a lock.
            tag_tg = "none"
            insp_desc_to_give = "Clear" 

        lock_object = db.lock(
            is_active = should_lock,
            hack_difficulty = hack_difficulty_tg,
            demolish_difficulty = demolish_difficulty_tg,
            key_tag = key_tag_tg,
            tag = tag_tg,
            inspection_description = insp_desc_to_give
        )
        return lock_object

    def createTrap(self):
        difficulties = [30,60,100,150,210]
        should_trap = random.randint(0,100) < 10
        hack_difficulty_tg = random.choice(difficulties)
        see_difficulty_tg = random.choice(difficulties)
        trap_lethality_tg = random.randint(1,50)
        inspection_description_tg = "INCOMPLETE FEATURE"
        trap_object = db.trap(
            is_active = should_trap,
            trap_obscurity = see_difficulty_tg,
            trap_lethality = trap_lethality_tg,
            hack_difficulty = hack_difficulty_tg,
            inspection_description = inspection_description_tg
        )
        return trap_object

    def createPath(self, room, deadend = False, string_loc = "default"):
        difficulties = [30,60,100,150,210]
        path_lock = self.createLock(room, string_loc)
        path_trap = self.createTrap()
        see_difficulty_tg = random.choice(difficulties)
        dungeon = db.DungeonEntry.objects.get(name =room.d_name)
        if deadend:
            tag_tg = random.choice(dungeon.deadends_tags)
            insp_desc_to_give = "No Path"
        else:
            tag_tg = random.choice(dungeon.pathways_tags)
            insp_desc_to_give = tag_tg 
            if path_lock.is_active == True: 
                insp_desc_to_give += " (BLOCKED)."  
        path_obj = db.path(
            lock = path_lock,
            trap = path_trap,
            obscurity = see_difficulty_tg,
            inspection_description = insp_desc_to_give,
            tag = tag_tg
        )
        return path_obj

    def insert_locks(self,room,fake_variable):
        count =0
        for interact in room.interactables:
            stringo = "inter::"+str(count)
            interact.lock = self.createLock(room, stringo)
            interact.trap = self.createTrap()
            count += 1
        
        stringo = "north"
        if room.north_exit != None and room.north_exit != "NONE":
            room.north = self.createPath(room,False,stringo)
        else:
            room.north = self.createPath(room,True,stringo)

        stringo = "east"
        if room.east_exit != None and room.east_exit != "NONE":
            room.east = self.createPath(room,False, stringo)
        else:
            room.east = self.createPath(room,True, stringo)
        
        stringo = "south"
        if room.south_exit != None and room.south_exit != "NONE":
            room.south = self.createPath(room,False, stringo)
        else:
            room.south = self.createPath(room,True, stringo)
         
        stringo = "west"
        if room.west_exit != None and room.west_exit != "NONE":
            room.west = self.createPath(room, False, stringo)
        else:
            room.west = self.createPath(room,True, stringo)
        room.save()
    

    def traverse(self, room , func = do_nothing, *args):
        if room == "DoesNotExist":
            print("DoesNotExist")
            return 
        if room.node_id in self.rooms_visited:
            return
        self.rooms_visited.append(room.node_id)
        func(room, args)
        if room.north_exit != None and room.north_exit != "NONE":
            self.traverse(self.getNode(room.north_exit), func, args)
        if room.east_exit != None and room.east_exit != "NONE":
            self.traverse(self.getNode(room.east_exit), func, args)
        if room.south_exit != None and room.south_exit != "NONE":
            self.traverse(self.getNode(room.south_exit), func, args) 
        if room.west_exit != None and room.west_exit != "NONE":
            self.traverse(self.getNode(room.west_exit), func, args)
    

    def random_traverse(self, room , func = do_nothing, *args):
        if room == "DoesNotExist":
            print("DoesNotExist")
            return 
        if room.node_id in self.rooms_visited:
            return
        self.rooms_visited.append(room.node_id)
        func(room, args)
        rooms_to_visit =[]
        if room.north_exit != None and room.north_exit != "NONE":
            rooms_to_visit.append(0)
        if room.east_exit != None and room.east_exit != "NONE":
            rooms_to_visit.append(1)  
        if room.south_exit != None and room.south_exit != "NONE":
            rooms_to_visit.append(2)
        if room.west_exit != None and room.west_exit != "NONE":
            rooms_to_visit.append(3)
        number_of_exits = len(rooms_to_visit)
        new_arg = self.rooms_dict[room.node_id]
        for door_c in range(number_of_exits):
            select = random.randint(0,len(rooms_to_visit)-1)
            selected = rooms_to_visit.pop(select)
            if selected == 0:
                self.random_traverse(self.getNode(room.north_exit), func, (new_arg))
            elif selected ==1:
                self.random_traverse(self.getNode(room.east_exit), func, (new_arg))
            elif selected ==2: 
                self.random_traverse(self.getNode(room.south_exit), func, (new_arg)) 
            elif selected ==3:
                self.random_traverse(self.getNode(room.west_exit), func, (new_arg))

    def re_init_for_traversal(self):
        self.rooms_visited = []
        self.all_rooms = db.Dungeon.objects(d_name = self.name).no_dereference()

    def populate_dungeon(self):
        self.rooms_visited = []
        self.random_traverse(self.entrance, self.insert_interactables, ([]))
        self.re_init_for_traversal()
        self.traverse(self.entrance, self.insert_locks)

    def print_dungeon(self):
        self.re_init_for_traversal()
        self.traverse(self.entrance, print_room)
    
    def launch(self):
        self.rooms_visited = []
        self.traverse(self.entrance)

def force_gen_map(name):
    d_id = generate_dungeon(name)
    map_generator = MapTraversal(name, d_id)
    map_generator.populate_dungeon()
    #map_generator.print_dungeon()
    return map_generator.entrance

def gen_map(name):
    force_gen_map(name)
    return "COMPLETED DUNGEON GENERATION"

def generate_random_dungeons():
    all_dungeons = db.DungeonEntry.objects.no_dereference()
    all_world_nodes = db.WorldNode.objects.no_dereference()
    gens_counter = 0
    for dungeon in all_dungeons:
        if dungeon.existing_instances < dungeon.max_instances_of_dungeon:
            entrance = force_gen_map(dungeon.name)
            node_to_place = random.choice(all_world_nodes)
            node_to_place.sub_nodes_ids.append(entrance.node_id)
            node_to_place.save()
            gens_counter +=1 
    print(str(gens_counter) + " DUNGEONS WERE GENERATED")
    return 
