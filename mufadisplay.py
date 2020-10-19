
#Function for creating a small digital display on the screen in the style `___10/100`
def digits_panel(minvalue:int, maxvalue:int, size:int) -> str:
    m_v = str(minvalue)
    M_v = str(maxvalue)
    spaces_needed = size-len(m_v)-len(M_v)
    for i in range(spaces_needed):
        m_v = " " + m_v
    return "`"+m_v+"/"+M_v+"`"