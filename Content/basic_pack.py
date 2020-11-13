import mufa_world as mw
import mufadb as db
def basic_weapons():
    db.Weapon(item_id = mw.generateItemID(),
            name = "Basic Sword", 
            item_type = 3,
            precision_scale = 90,
            damage_amp_scale = 5,
            damage_per_amp = 2,
            damage_base = 3,
            drop_chance = 10).save()
    db.Weapon(item_id = mw.generateItemID(),
            name = "Basic Spear", 
            item_type = 4,
            precision_scale = 70,
            damage_amp_scale = 5,
            damage_per_amp = 2,
            damage_base = 3,
            drop_chance = 10).save()
    db.Weapon(item_id = mw.generateItemID(),
            name = "Basic Club", 
            item_type = 5,
            precision_scale = 50,
            damage_amp_scale = 50,
            damage_per_amp = 5,
            damage_base = 3,
            drop_chance = 10).save()
    db.Weapon(item_id = mw.generateItemID(),
            name = "Basic Bow", 
            item_type = 6,
            precision_scale = 70,
            damage_amp_scale = 50,
            damage_per_amp = 2,
            damage_base = 3,
            drop_chance = 10).save()
    
    db.Weapon(item_id = mw.generateItemID(),
            name = "Goblin Claws", 
            item_type = 3,
            precision_scale = 90,
            damage_amp_scale = 10,
            damage_per_amp = 1,
            damage_base = 3).save()
    
    print("Basic Weapons Pack Installed Successfully")

def basic_armor():

    #Cultist Armor Set
    db.ArmorSet(name = "Cultist",
                two_items_set_bonus = [1,0,0,0],
                full_set_bonus = [2,0,0,0]).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Cultist's Hood",
            armor_set = db.ArmorSet.objects.get(name = "Cultist").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Cultist's Robes",
            armor_set = db.ArmorSet.objects.get(name = "Cultist").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Cultist's Boots",
            armor_set = db.ArmorSet.objects.get(name = "Cultist").to_dbref(),
            item_type = 2,
            evasion_chance_reduction = 0,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    #Rook Armor Set
    db.ArmorSet(name = "Rook",
                two_items_set_bonus = [0,1,0,0],
                full_set_bonus = [0,2,0,0]).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Rook's Helmet",
            armor_set = db.ArmorSet.objects.get(name = "Rook").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Rook's Hide",
            armor_set = db.ArmorSet.objects.get(name = "Rook").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Rook's Boots",
            armor_set = db.ArmorSet.objects.get(name = "Rook").to_dbref(),
            item_type = 2,
            evasion_chance_reduction = 0,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    
    #Acrobat Armor Set
    db.ArmorSet(name = "Acrobat",
                two_items_set_bonus = [0,0,1,0],
                full_set_bonus = [0,0,2,0]).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Acrobat's Cap",
            armor_set = db.ArmorSet.objects.get(name = "Acrobat").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Acrobat's Shirt",
            armor_set = db.ArmorSet.objects.get(name = "Acrobat").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Acrobat's Shoes",
            armor_set = db.ArmorSet.objects.get(name = "Acrobat").to_dbref(),
            item_type = 2,
            evasion_chance_reduction = 0,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    #Brute Armor Set
    db.ArmorSet(name = "Brute",
                two_items_set_bonus = [0,0,0,1],
                full_set_bonus = [0,0,0,2]).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Brute's Helmet",
            armor_set = db.ArmorSet.objects.get(name = "Brute").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Brute's Armour",
            armor_set = db.ArmorSet.objects.get(name = "Brute").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = mw.generateItemID(),
            name = "Brute's Boots",
            armor_set = db.ArmorSet.objects.get(name = "Brute").to_dbref(),
            item_type = 2,
            evasion_chance_reduction = 0,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    print("Basic Armour Pack Installed Successfully")

def basic_monsters():
    null_obj = db.Item.objects.get(name = "null_object").to_dbref()
    weapon_slash = db.Weapon.objects.get(name = "Goblin Claws").to_dbref()
    helmet = db.Armor.objects.get(name = "Rook's Helmet").to_dbref()
    chestpiece = db.Armor.objects.get(name = "Rook's Hide").to_dbref()
    boots = db.Armor.objects.get(name = "Rook's Boots").to_dbref()
    n_char = db.character(name = "Goblin Rook",
                          willpower = 1,
                          vitality = 2,
                          agility = 1,
                          strength = 1,
                          karma = 1,
                          current_health = 10,
                          current_sanity = 10,
                          armor_equiped = [helmet,chestpiece,boots],
                          weapons_equiped = [weapon_slash,null_obj,null_obj,null_obj],
                          instance_stack = []
                          )
    db.MonsterEntry(character_stats=n_char).save()
    
    helmet = db.Armor.objects.get(name = "Acrobat's Cap").to_dbref()
    chestpiece = db.Armor.objects.get(name = "Acrobat's Shirt").to_dbref()
    boots = db.Armor.objects.get(name = "Acrobat's Shoes").to_dbref()
    n_char = db.character(name = "Goblin Scout",
                          willpower = 1,
                          vitality = 1,
                          agility = 2,
                          strength = 1,
                          karma = 1,
                          current_health = 10,
                          current_sanity = 10,
                          armor_equiped = [helmet,chestpiece,boots],
                          weapons_equiped = [weapon_slash,null_obj,null_obj,null_obj],
                          instance_stack = []
                          )
    db.MonsterEntry(character_stats=n_char).save()
    
    helmet = db.Armor.objects.get(name = "Brute's Helmet").to_dbref()
    chestpiece = db.Armor.objects.get(name = "Brute's Armour").to_dbref()
    boots = db.Armor.objects.get(name = "Brute's Boots").to_dbref()
    n_char = db.character(name = "Goblin Brute",
                          willpower = 1,
                          vitality = 1,
                          agility = 1,
                          strength = 2,
                          karma = 1,
                          current_health = 10,
                          current_sanity = 10,
                          armor_equiped = [helmet,chestpiece,boots],
                          weapons_equiped = [weapon_slash,null_obj,null_obj,null_obj],
                          instance_stack = []
                          )
    db.MonsterEntry(character_stats=n_char).save()
    
    print("Basic Monsters Pack Installed Successfully")

def basic_dungeon():
    db.Tags(
    name = "Decorators",
    collection = ["barrel", "cupboard", "waste", "pot", "corpses", "torches",
    "bones","pit","mold","graffiti","cage","kennels","debris"]
    ).save()
  
    db.Tags(
    name = "Deadends",
    collection = ["wall", "bottomless pit", "boulder" , "wooden obstacle",
    "barricade"]
    ).save()

    db.Tags(
    name = "Pathways",
    collection = ["tunnel","slope","stairs","stream","waterfall","bridge",
    "shipwreck", "door", "doorway", "curtain", "corridor"]
    ).save()

    db.Tags(
    name = "Symbols",
    collection = ["circle", "square", "triangle", "stickman", "eye", "sun",
    "moon", "hexagon", "skull", "oval", "leaf", "bear", "wolf", "eagle", 
    "fish", "sword", "bow", "flame", "star" , "deer", "arrow", "spiral",
    "0", "1", "2","3","4","5","6","7","8","9"]
    ).save()

    db.DungeonEntry(
    name = "Goblin Lair",
    max_monsters = 10,
    average_number_of_rooms = 15,
    monsters_list = ["Goblin Rook", "Goblin Scout", "Goblin Brute"],
    id_prefix = "GL",
    descriptor_tags =["barrel", "cupboard", "waste", "pot", "corpses", "torches",
    "bones","pit","mold","graffiti","cage","kennels","debris"],
    deadends_tags = ["wall", "bottomless pit", "boulder" , "wooden obstacle",
    "barricade"],
    pathways_tags = ["tunnel","slope","stairs","stream","waterfall","bridge",
    "shipwreck", "door", "doorway", "curtain", "corridor"]
    ).save()

    
    
    print("Basic Dungeon Pack Installed Successfully")
 
def install_pack():
    basic_weapons()
    basic_armor()
    basic_monsters()
    basic_dungeon()
    db.PackageNames(name = "basic").save()