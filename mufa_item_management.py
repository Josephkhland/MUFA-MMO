import mufa_constants as mc
import mufadisplay as mdisplay
import mufadb as db
import discord
import math

def copyItem(item_list, id_of_item_to_grab, character_to_give):
    character_to_give.inventory.append(db.Item.objects.get(item_id =item_list[id_of_item_to_grab].item_id))
    return character_to_give

def storeItem(list_to_grab, id_of_item_to_move, player):
    if len(list_to_grab) <= id_of_item_to_move:
        return "Not a valid index for the given inventory"
    player.items_stored.append(list_to_grab[id_of_item_to_move])
    player.save()
    return "Successfully stored "+ list_to_grab[id_of_item_to_move].name + " to player storage."

def turnListToDBREF(listname):
    new_list = []
    for i in listname:
        new_list.append(i.to_dbref())
    return new_list
    
def pickupItem(node_with_treasure, id_of_item_to_grab, battler):
    character_to_give = battler.getCharacter()
    item_list = node_with_treasure.treasure
    if len(item_list) < id_of_item_to_grab:
        return "ERROR: Index out of bounds. This Instance doesn't have such an item in its treasure"
    if len(character_to_give.inventory) >= character_to_give.strength*6 :
        return character_to_give.name +" has a full inventory("+str(len(character_to_give.inventory))+"/"+str(character_to_give.strength*6)+"."
    character_to_give = copyItem(item_list, id_of_item_to_grab, character_to_give)
    name_of_item = item_list[id_of_item_to_grab].name
    del item_list[id_of_item_to_grab]
    item_list = turnListToDBREF(item_list)
    node_with_treasure.treasure = item_list
    node_with_treasure.save()
    character_to_give.inventory = turnListToDBREF(character_to_give.inventory)
    battler.updateCurrentCharacter(character_to_give)
    battler.save()
    return character_to_give.name +" picked up " + name_of_item +"."

    
def buyItem(buyer, guild, id_of_item_to_grab):
    bCharacter = buyer.getCharacter()
    shop_list = guild.shop
    try:
        price = shop_list[id_of_item_to_grab].value
    except:
        return "ERROR: Index out of bounds. The shop doesn't have such an item"
    if price <= bCharacter.money_carried:
        if len(bCharacter.inventory) >= bCharacter.strength*6 :
            if guild.guild_id != buyer.guild_id:
                return bCharacter.name +" has a full inventory("+str(len(bCharacter.inventory))+"/"+str(bCharacter.strength*6)+". Your storage is too far to deposit the purchased item.\nTransaction is cancelled."
            else:
                bCharacter.money_carried -= shop_list[id_of_item_to_grab].value
                buyer.updateCurrentCharacter(bCharacter)
                storeItem(shop_list, id_of_item_to_grab, buyer)
                return bCharacter.name + " has purchased `" + shop_list[id_of_item_to_grab].name + "` for a price of "+ str(shop_list[id_of_item_to_grab].value) + mc.currency +"\nYour character's inventory is full, so the item was deposited in storage."
                
        bCharacter.money_carried -= shop_list[id_of_item_to_grab].value
        bCharacter = copyItem(shop_list, id_of_item_to_grab, bCharacter)
        bCharacter.inventory = turnListToDBREF(bCharacter.inventory)
        bCharacter.instance_stack = turnListToDBREF(bCharacter.instance_stack)
        buyer.updateCurrentCharacter(bCharacter)
        buyer.save()
        return bCharacter.name + " has purchased `" + shop_list[id_of_item_to_grab].name + "` for a price of "+ str(shop_list[id_of_item_to_grab].value) + mc.currency
    else:
        missing = shop_list[id_of_item_to_grab].value - bCharacter.money_carried
        return bCharacter.name + " doesn't carry enough money to make this purchase. Missing `" +missing + "` " + mc.currency

def sellItem(seller, id_of_item_to_sell):
    sCharacter = seller.getCharacter()
    inventory = sCharacter.inventory
    try: 
        money = math.ceil(inventory[id_of_item_to_sell].value / 2)
    except:
        return "ERROR: You don't have an item in that inventory slot"
    name_of_item = inventory[id_of_item_to_sell].name 
    del inventory[id_of_item_to_sell]
    sCharacter.inventory = turnListToDBREF(inventory)
    sCharacter.money_carried += money
    sCharacter.instance_stack = turnListToDBREF(sCharacter.instance_stack)
    seller.updateCurrentCharacter(sCharacter)
    seller.save()
    return sCharacter.name +" sold " + name_of_item + " for `" +str(money) +"`."

def compare_item(id_in_list, player, storage = False):
    sCharacter = player.getCharacter()
    locationStr = "(INVENTORY)"
    equipedStr = "(EQUIPED)"
    item_list = []
    if storage == False:
        item_list = sCharacter.inventory
        locationStr = "(INVENTORY)"
    else: 
        item_list = player.items_stored
        locationStr = "(STORAGE)"
    if len(item_list) <= id_in_list:
        return
    i_type = item_list[id_in_list].item_type
    
    if i_type ==0:
        item_to_compare = sCharacter.armor_equiped[0]
        equipedStr = "(EQUIPED HELMET)"
    elif i_type == 1:
        item_to_compare = sCharacter.armor_equiped[1]
        equipedStr = "(EQUIPED CHESTPIECE)"
    elif i_type ==2:
        item_to_compare = sCharacter.armor_equiped[2]
        equipedStr = "(EQUIPED BOOTS)"
    elif i_type ==3:
        item_to_compare = sCharacter.weapons_equiped[0]
        equipedStr = "(EQUIPED SLASH WEAPON)"
    elif i_type ==4:
        item_to_compare = sCharacter.weapons_equiped[1]
        equipedStr = "(EQUIPED PIERCE WEAPON)"
    elif i_type ==5:
        item_to_compare = sCharacter.weapons_equiped[2]
        equipedStr = "(EQUIPED CRASH WEAPON)"
    elif i_type ==6:
        item_to_compare = sCharacter.weapons_equiped[3]
        equipedStr = "(EQUIPED RANGED WEAPON)"
    elif i_type == 7: 
        item_to_compare = db.Item.objects.get(name = "null_object")
        equipedStr = "(ARTIFACT)"
    elif i_type == 8:
        item_to_compare = db.Item.objects.get(name = "null_object")
        equipedStr = "(SPELLBOOK)"
    embed = discord.Embed(
                title = "Compare Items",
                description = "Comparing "+item_list[id_in_list].name + " with the equipped "+item_to_compare.name,
                colour = discord.Colour.red()
                )
    name_string = str(id_in_list)+": "+item_list[id_in_list].name + " "+locationStr
    item_1_str = mdisplay.itemDetails(item_list[id_in_list], True)
    embed.add_field(name = name_string, value = item_1_str , inline = False)

    if item_to_compare.name != "null_object":
        name_string = str(id_in_list)+": "+item_to_compare.name + " "+equipedStr
        item_2_str = mdisplay.itemDetails(item_to_compare, True)
        embed.add_field(name = name_string , value = item_2_str, inline = False)
    else:
        if i_type < 7:
            embed.add_field(name = equipedStr, value = "No item equipped in this slot", inline = False)
        else:
            embed.add_field(name = equipedStr, value = "Items of this type can't be compared.", inline = False)
    
    return embed

def removeArmorSet(character):
    if character.armor_set == None: 
        return character
    if character.set_bonus_specification == 2:
        character.willpower -= character.armor_set.full_set_bonus[0]
        character.vitality -=character.armor_set.full_set_bonus[1]
        character.agility -=character.armor_set.full_set_bonus[2]
        character.strength -=character.armor_set.full_set_bonus[3]
    elif character.set_bonus_specification == 1:
        character.willpower -= character.armor_set.two_items_set_bonus[0]
        character.vitality -=character.armor_set.two_items_set_bonus[1]
        character.agility -=character.armor_set.two_items_set_bonus[2]
        character.strength -=character.armor_set.two_items_set_bonus[3]
    return character

def equipArmorSet(character):
    if character.set_bonus_specification == 2:
        character.willpower += character.armor_set.full_set_bonus[0]
        character.vitality +=character.armor_set.full_set_bonus[1]
        character.agility +=character.armor_set.full_set_bonus[2]
        character.strength +=character.armor_set.full_set_bonus[3]
    elif character.set_bonus_specification == 1:
        character.willpower += character.armor_set.two_items_set_bonus[0]
        character.vitality +=character.armor_set.two_items_set_bonus[1]
        character.agility +=character.armor_set.two_items_set_bonus[2]
        character.strength +=character.armor_set.two_items_set_bonus[3]
    return character

def checkArmorSet(character: db.character):
    set_names = []
    counter = 0
    armors_equipped = character.armor_equiped
    print(armors_equipped)
    for armor in armors_equipped:
        if armor.name != "null_object" and armor.item_type != 8:
            set_names.append(armor.armor_set.name)
        else :
            set_names.append(str(counter))
        counter += 1
    if character.armor_set != None:
        character = removeArmorSet(character)
    if set_names[0] == set_names[1]:
        if set_names[1] == set_names[2]:
            character.armor_set = character.armor_equiped[0].armor_set
            character.set_bonus_specification = 2
        else:
            character.armor_set = character.armor_equiped[0].armor_set
            character.set_bonus_specification = 1
    else:
        if set_names[1] == set_names[2]:
            character.armor_set = character.armor_equiped[1].armor_set
            character.set_bonus_specification = 2
        elif set_names[0] == set_names[2]:
            character.armor_set = character.armor_equiped[0].armor_set
            character.set_bonus_specification = 2
        else:
            character.armor_set = None
            character.set_bonus_specification = 0
    character = equipArmorSet(character)
    if character.armor_set != None:
        arm_set = character.armor_set
        character.armor_set = arm_set.to_dbref()
    return character

def equipItem(id_in_list, player, slot_for_spellbook = 0):
    sCharacter = player.getCharacter()
    inventory = sCharacter.inventory
    try:
        item_to_equip = inventory[id_in_list]
    except:
        return "ERROR: Index out of bounds. You don't have an item with such an index"
    i_type = item_to_equip.item_type
    if i_type ==0: #HELMET
        item_to_compare = sCharacter.armor_equiped[0]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.armor_equiped[0] = item_to_equip
    elif i_type == 1: #CHESTPIECE
        item_to_compare = sCharacter.armor_equiped[1]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.armor_equiped[1] = item_to_equip
    elif i_type ==2: # BOOTS
        item_to_compare = sCharacter.armor_equiped[2]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.armor_equiped[2] = item_to_equip
    elif i_type ==3: # SLASH
        item_to_compare = sCharacter.weapons_equiped[0]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.weapons_equiped[0] = item_to_equip
    elif i_type ==4: # PIERCE
        item_to_compare = sCharacter.weapons_equiped[1]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.weapons_equiped[1] = item_to_equip
    elif i_type ==5: # CRASH
        item_to_compare = sCharacter.weapons_equiped[2]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.weapons_equiped[2] = item_to_equip
    elif i_type ==6: # RANGED
        item_to_compare = sCharacter.weapons_equiped[3]
        if item_to_compare.name != "null_object":
            inventory.append(item_to_compare)
        sCharacter.weapons_equiped[3] = item_to_equip
    elif i_type == 7: #ARTIFACT
        return "ERROR: ARTIFACT items cannot be equiped."
    elif i_type == 8: #SPELLBOOK
        if slot_for_spellbook <0 or slot_for_spellbook >= 8:
            return "ERROR: SPELLBOOK cannot be equipped in this slot!"
        if slot_for_spellbook <=2:
            item_to_compare = sCharacter.armor_equiped[slot_for_spellbook]
            if item_to_compare.name != "null_object":
                inventory.append(item_to_compare)
            sCharacter.armor_equiped[slot_for_spellbook] = item_to_equip
        else:
            slot_for_spellbook -= 3
            item_to_compare = sCharacter.weapons_equiped[slot_for_spellbook]
            if item_to_compare.name != "null_object":
                inventory.append(item_to_compare)
            sCharacter.weapons_equiped[slot_for_spellbook] = item_to_equip
    sCharacter = checkArmorSet(sCharacter)
    del inventory[id_in_list]
    sCharacter.armor_equiped = turnListToDBREF(sCharacter.armor_equiped)
    sCharacter.weapons_equiped = turnListToDBREF(sCharacter.weapons_equiped)
    sCharacter.inventory = turnListToDBREF(inventory)
    sCharacter.instance_stack = turnListToDBREF(sCharacter.instance_stack)
    player.updateCurrentCharacter(sCharacter)
    player.save()
    return "Successfully equipped " +item_to_equip.name + " to "+ sCharacter.name + "\n"

def unequipItem(player, slot_id):
    sCharacter = player.getCharacter()
    inventory = sCharacter.inventory
    if len(inventory) >= sCharacter.strength*6:
        return "Inventory is full. Can't unequip item."
    item_to_equip = db.Item.objects.get(name = "null_object")
    item_to_remove = db.Item.objects.get(name = "null_object")
    if slot_id <0 or slot_id >= 8:
        return "ERROR: Not a Valid Slot!"
    if slot_id <=2:
        item_to_remove = sCharacter.armor_equiped[slot_id]
        if item_to_remove.name != "null_object":
            inventory.append(item_to_remove)
        else:
            return "You already have no item equipped at the selected slot."
        sCharacter.armor_equiped[slot_id] = item_to_equip.to_dbref()
    else:
        slot_id -= 3
        item_to_remove = sCharacter.weapons_equiped[slot_id]
        if item_to_remove.name != "null_object":
            inventory.append(item_to_remove)
        else:
            return "You already have no item equipped at the selected slot."
        sCharacter.weapons_equiped[slot_id] = item_to_equip.to_dbref()
    sCharacter = checkArmorSet(sCharacter)
    sCharacter.inventory = turnListToDBREF(inventory)
    sCharacter.instance_stack = turnListToDBREF(sCharacter.instance_stack)
    player.updateCurrentCharacter(sCharacter)
    player.save()
    return "Successfully unequipped " +item_to_remove.name + " from "+ sCharacter.name + "\n"