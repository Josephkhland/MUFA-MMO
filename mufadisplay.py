import mufadb as db
#Function for creating a small digital display on the screen in the style `___10/100`
def digits_panel(minvalue:int, maxvalue:int, size:int) -> str:
    m_v = str(minvalue)
    M_v = str(maxvalue)
    spaces_needed = size-len(m_v)-len(M_v)
    for i in range(spaces_needed):
        m_v = " " + m_v
    return "`"+m_v+"/"+M_v+"`"

def line(label: str, value:int):
    return label +": `"+ str(value)+"`\n"

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
