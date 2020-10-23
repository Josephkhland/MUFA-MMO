import mufadb as db
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
    for m in node.members:
        if m.faction == 0 :
            for c in m.characters_list:
                if c.is_dead == False and c.getInstance() == node:
                    if len(playerBattlers[tab_count_players]) >500:
                        tab_count_players += 1
                        playerBattlers.append("")
                    playerBattlers[tab_count_players] += c.name +"("+m.battler_id+"), "
        elif m.faction == 1:
            if len(playerBattlers[tab_count_monsters]) >500:
                    tab_count_monsters += 1
                    monsterBattlers.append("")
            monsterBattlers[tab_count_monsters] += m.getCharacter().name + ", "
    for i in range(len(playerBattlers)):
        playerBattlers[i] = playerBattlers[i][:-2]
    for i in range(len(monsterBattlers)):
        monsterBattlers[i] = monsterBattlers[i][:-2]
    return (playerBattlers,monsterBattlers)