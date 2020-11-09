import mufa_world as mw
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
    
    db.Armor(item_id = generateItemID(),
            name = "Cultist's Hood",
            armor_set = db.ArmorSet.objects.get(name = "Cultist").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
            name = "Cultist's Robes",
            armor_set = db.ArmorSet.objects.get(name = "Cultist").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
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
    
    db.Armor(item_id = generateItemID(),
            name = "Rook's Helmet",
            armor_set = db.ArmorSet.objects.get(name = "Rook").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
            name = "Rook's Hide",
            armor_set = db.ArmorSet.objects.get(name = "Rook").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
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
    
    db.Armor(item_id = generateItemID(),
            name = "Acrobat's Cap",
            armor_set = db.ArmorSet.objects.get(name = "Acrobat").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
            name = "Acrobat's Shirt",
            armor_set = db.ArmorSet.objects.get(name = "Acrobat").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
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
    
    db.Armor(item_id = generateItemID(),
            name = "Brute's Helmet",
            armor_set = db.ArmorSet.objects.get(name = "Brute").to_dbref(),
            item_type = 0,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
            name = "Brute's Armour",
            armor_set = db.ArmorSet.objects.get(name = "Brute").to_dbref(),
            item_type = 1,
            evasion_chance_reduction = 5,
            physical_damage_reduction_f = 0,
            physical_damage_reduction_p = 2,
            drop_chance = 10).save()
    
    db.Armor(item_id = generateItemID(),
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
    new_id = mw.generateMonsterID()
    db.Monster(battler_id = new_id, name =n_char.name ,character_stats=n_char).save()
    
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
    new_id = mw.generateMonsterID()
    db.Monster(battler_id = new_id, name =n_char.name ,character_stats=n_char).save()
    
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
    new_id = mw.generateMonsterID()
    db.Monster(battler_id = new_id, name =n_char.name ,character_stats=n_char).save()
    
    print("Basic Monsters Pack Installed Successfully")

def basic_dungeon():
    db.Dungeon(node_id = "BDGL0000",
               entrance_message = "You are standing at the entrance of a dark cavern, it's overall pretty dark, making it hard to see. The wind blowing from the north, carries a stinking smell of goblin waste."
               name = "Goblin Lair",
               gold_loot = 50,
               north_exit = "BDGL0100).save()
    db.Room(node_id = "BDGL0100",
            name = "Goblin Lair - Room 1",
            entrance_message = "It's so dark that it's hard to see",
            gold_loot = 50,
            south_exit = "BDGL0000").save()
    
    print("Basic Dungeon Pack Installed Successfully")
 
def install_pack():
    basic_weapons()
    basic_armor()
    basic_monsters()
    db.PackageNames(name = "basic").save()