import mufadb as db
import datetime
import discord
#Function for creating a small digital display on the screen in the style `___10/100`
def digits_panel(minvalue:int, maxvalue:int, size:int) -> str:
    m_v = str(minvalue)
    M_v = str(maxvalue)
    spaces_needed = size-len(m_v)-len(M_v)
    for i in range(spaces_needed):
        m_v = " " + m_v
    return "`"+m_v+"/"+M_v+"`"

def line(label: str, value:int, size:int):
    val_str = str(value)
    characters_occupy = len(label) + len(val_str)
    num_of_space = size - characters_occupy
    if num_of_space < 0 : num_of_space = 0
    string_to_return = label +":"
    for i in range(num_of_space):
        string_to_return += ' '
    string_to_return +="`"+ val_str+"`\n"
    return string_to_return

def null_item_display_help(item):
    if item.name == "null_object":
        return "-"
    else:
        return item.name
    
def equipment(slot,item):
    name = null_item_display_help(item)
    if slot == 0:
        return "Helmet: `" + name +"`\n"
    if slot == 1:
        return "Chestpiece: `" + name +"`\n"
    if slot == 2:
        return "Boots: `" + name +"`\n"
    if slot == 3:
        return "Slash: `" + name + "`\n"
    if slot == 4:
        return "Pierce: `" + name +"`\n"
    if slot == 5:
        return "Crash: `" + name +"`\n"
    if slot == 6:
        return "Ranged: `" + name +"`\n"


def node_members(node):
    playerBattlers = [""]
    tab_count_players = 0
    monsterBattlers = [""]
    tab_count_monsters = 0
    members_seen = []
    for m in node.members:
        if m in members_seen: continue
        members_seen.append(m)
        if m.faction == 0 :
            for c in m.characters_list:
                if c.is_dead == False and c.getInstance() == node:
                    if len(playerBattlers[tab_count_players]) >500:
                        tab_count_players += 1
                        playerBattlers.append("")
                    playerBattlers[tab_count_players] += c.name +"("+m.battler_id+"), "
        elif m.faction == 1:
            if len(monsterBattlers[tab_count_monsters]) >500:
                    tab_count_monsters += 1
                    monsterBattlers.append("")
            monsterBattlers[tab_count_monsters] += m.getCharacter().name + ", "
    members_seen = None
    for i in range(len(playerBattlers)):
        playerBattlers[i] = playerBattlers[i][:-2]
    for i in range(len(monsterBattlers)):
        monsterBattlers[i] = monsterBattlers[i][:-2]
    return (playerBattlers,monsterBattlers)

def node_monsters(node):
    monsterBattlers = []
    for m in node.members:
        if m.faction == 1:
            monsterBattlers.append(m)
    return monsterBattlers

def display_battle_members(list_of_members, node_id):
   
    embedList = []
    counter = 0
    tab_size = 10
    current_tab =00
    total_tabs = 1+ len(list_of_members)/tab_size 
    for enemy in list_of_members:
        if counter >= current_tab*tab_size:
            if counter != 0: embedList.append(embed)
            current_tab += 1
            embed = discord.Embed(
                title = "BATTLE",
                description = "Use the indexes below to choose your targets when attacking.",
                colour = discord.Colour.red()
                )
            embed.set_footer(text="Battle("+node_id+") - Last Active : " + datetime.datetime.now().ctime() + " - Tab "+str(current_tab)+"/"+str(total_tabs))
        #ADD ENEMY TO EMBED
        enemy_char = enemy.getCharacterInNode(node_id)
        name_to_add = str(counter) + ": " + enemy_char.name + "("+enemy.battler_id+")"
        healthString = digits_panel(enemy_char.current_health,enemy_char.vitality*10, 8) + ":heart: "
        sanityString = digits_panel(enemy_char.current_sanity,enemy_char.willpower*10, 8) + ":brain: "
        disabling_conditions = [False,False,False]
        this_value = "Conditions:  "
        buff_value = "Buffs:  "
        for con in enemy_char.conditions:
            if con.name == 'DEAD':
                disabling_conditions[0] = True
            if con.name == 'PETRIFIED':
                disabling_conditions[1] = True
            if con.name == 'ASLEEP':
                disabling_conditions[2] = True
            this_value += "`"+con.name+"`, "
        this_value = this_value[:-2]
        for buf in enemy_char.buffs:
            this_value += "`"+con.name+"`, "
        buff_value = buff_value[:-2]
        name_plugin = " "
        if disabling_conditions[2]:
            name_plugin += ":zzz: "
        if disabling_conditions[1]:
            name_plugin += ":rock: "
        if disabling_conditions[0]:
            name_plugin += ":skull: "
        embed.add_field(name = name_to_add+name_plugin, value = healthString + sanityString + "\n" + this_value + "\n" + buff_value, inline = False)
        counter += 1
        if counter == len(list_of_members):
            embedList.append(embed)
    return embedList
    
def displayInventoryList(character):
    embedList = []
    counter = 0
    tab_size = 3
    current_tab =0
    total_tabs = 1+ len(character.inventory)/tab_size 
    for item in character.inventory:
        if counter >= current_tab*tab_size:
            if counter != 0: embedList.append(embed)
            current_tab += 1
            embed = discord.Embed(
                title = "Inventory",
                description = "Use the indexes below to choose your targets when attacking.",
                colour = discord.Colour.red()
                )
            embed.set_footer(text=character.name+" inventory - Last Active : " + datetime.datetime.now().ctime() + " - Tab "+str(current_tab)+"/"+str(total_tabs))
        
        name_string = str(counter)+item.name +" ("+db.ItemType(item.item_type).name+")"
        conditions_string = "*Condition Resistances:*  "
        for con_counter in range(15):
            if item.condition_resistances[con_counter] != 0 :
                condition_string += "**"+db.Conditions(con_counter).name +"** `"+str(item.condition_resistances[con_counter]) + "%`, "
        conditions_string = condition_string[:-2]
        forced_exhaustion_resistance = ""
        spell_resistance_string =""
        if item.spell_resistance != 0: 
            spell_resistance_string = "**Spell Resistance:** `" +str(item.spell_resistance)+"%`"
        if item.forced_exhaustion_resistance != 0: 
            forced_exhaustion_resistance = "**Forced Exhaustion Resistance:** `"+ str(item.forced_exhaustion_resistance)+"%`"
        
        str_so_far = conditions_string + "\n" + forced_exhaustion_resistance + "\n" + spell_resistance_string +"\n"
        if isinstance(item, db.Weapon):
            str_dmg_amp_stat = "STR"
            if item.item_type == 6:
                str_dmg_amp_stat = "AGI"
            precision_string = "**Precision:** `"+ str(item.precision_scale) + "%` per AGI."  
            dmg_amp_string = "**Amplification DMG:** `" +str(item.damage_per_amp) + "` per AMPLIFICATION" 
            dmg_amp_chance_string = "**Amplification Chance:** `" +str(item.damage_amp_scale)+ "%` per " + str_dmg_amp_stat
            base_dmg_string = "**Base DMG:** `" + str(item.damage_base)
            str_so_far += precision_string +"\n" + dmg_amp_string +"\n" + dmg_amp_chance_string +"\n" +base_dmg_string + "\n"
        
        if isinstance(item, db.Armor):
            evasion_reduction_str = ""
            if item.evasion_chance_reduction !=0:
                evasion_reduction_str = "**Evasion reduction:** `-"+ str(item.evasion_chance_reduction) +"%` "
            str_physical_DR= "**Physical Damage Reduction:** `" + str(item.physical_damage_reduction_f)+ "` FLAT, `"+ str(item.physical_damage_reduction_p) + "`% "
            str_magic_DR = "**Magic Damage Reduction:** `" + str(item.magic_damage_reduction_f)+ "` FLAT, `"+ str(item.magic_damage_reduction_p) + "`% "
            armor_set_str = "**Armor set: ** `" + item.armor_set.name +"`"
            set_bonuses_str = "" 
            for i in range(4):
                if item.armor_set.full_set_bonus[i] != 0:
                    set_bonuses_str +=  "["+ str(item.armor_set.two_items_set_bonus[i]) +"|"+ str(item.armor_set.full_set_bonus[i]) +"] "+db.PrimaryStat(i).name +"\n"
            str_so_far = str_physical_DR + "\n" + str_magic_DR + "\n" + evasion_chance_reduction + "\n" + armor_set_str + "\n" + set_bonuses_str
        embed.add_field(name = name_string , value = str_so_far , inline = False)
        counter += 1
        if counter == len(list_of_members):
            embedList.append(embed)
    return embedList