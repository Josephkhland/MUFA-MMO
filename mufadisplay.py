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