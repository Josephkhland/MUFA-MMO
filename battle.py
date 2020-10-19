import random
import mufadb as db 
import mongoengine
import mufadisplay as puru
import discord

def create():
    stored_var = db.Instance().save()
    print(type(stored_var.id))
    return stored_var.id
    
def join(instance_id, applicant: db.Battler , side: int = 0):
    instance_obj = db.Instance.objects(id=instance_id, participants_side_A__S__previous_id= applicant.id)
    if side == 0:
        if  instance_obj != None :
            instance_obj.update(set__participants_side_A__S = applicant)
        else :
            db.Instance.objects(id=instance_id).update(push__participants_side_A = applicant)
    else:
        if  instance_obj != None :
            instance_obj.update(set__participants_side_B__S = applicant)
        else :
            db.Instance.objects(id=instance_id).update(push__participants_side_B = applicant)

def leave(instance_id, applicant: db.Battler, side: int = 0):
    
    try:
        if side == 0:
            temp_obj = db.Instance.objects(id=instance_id, participants_side_A__S__id = applicant.id)
            temp_obj.update(participants_side_A__S = db.GhostBattler(previous_id=applicant.id))
        else:
            temp_obj = db.Instance.objects(id=instance_id, participants_side_B__S__id = applicant.id)
            temp_obj.update(participants_side_B__S = db.GhostBattler(previous_id=applicant.id))
    except ValueError:
        debug_message_to_print = "Can't find Battler object in the given Instance("+instance_id+")."
        print(debug_message_to_print)
    
def list_participants(instance_id, side: int =0):
    temp_obj = db.Instance.objects(id=instance_id)
    side_to_text = "A"
    if side == 1:
        side_to_text = "B"

    embed = discord.Embed(
        title = "Side "+side_to_text+ " -Instance("+instance_id+").",
        description = "Powered by Josephkhland",
        colour = discord.Colour.blue()
    )
    embed.set_footer(text="Instance("+instance_id+") powered by Josephkhland")
    if side == 0:
        for participant in temp_obj.participants_side_A:
            if participant.previous_id != None:
                c = participant.getCharacter()
                useful_stats =(puru.digits_panel(c.current_health, c.vitality*10, 8) + ":heart:"
                               +puru.digits_panel(c.current_sanity, c.willpower*10, 8) + ":brain:"
                               +puru.digits_panel(c.actions_left, c.max_actions, 8) + ":zap:"
                              )
                embed.add_field(name= participant.name, value = useful_stats)
    else :
        for participant in temp_obj.participants_side_B:
            if participant != None:
                c = participant.getCharacter()
                useful_stats =(puru.digits_panel(c.current_health, c.vitality*10, 8) + ":heart:"
                               +puru.digits_panel(c.current_sanity, c.willpower*10, 8) + ":brain:"
                               +puru.digits_panel(c.actions_left, c.max_actions, 8) + ":zap:"
                              )
                embed.add_field(name= participant.name, value = useful_stats)
    return embed 