import random
import mufadb as db 
import mongoengine
import mufa_world as mw
import mufadisplay as mdisplay
import datetime
import discord

def log_entry(battler_obj, description):
    return db.battlelog(battler = battler_obj.to_dbref(), 
                        action_description = description,
                        timestamp = datetime.datetime.now()
                        )

def create(id_to_give, players_limit, initiator):
    log_message = "Created Battle Instance("+id_to_give+")"
    log_zero = log_entry(initiator, log_message)
    db.Battle(node_id = id_to_give, player_limit = players_limit, actions_log = [log_zero]).save()
    
def battle_add_member(node_id, battler):
    log_message = battler.name + "("+ battler.battler_id+") has joined the battle!"
    log_add = log_entry(battler, log_message)
    node = db.Battle.objects.get(node_id = node_id)
    node.actions_log.append(log_add)
    node.save()
    return mw.node_go_deeper(node_id, battler.battler_id)
    
def battle_member_leaves(battler):
    log_message = battler.name + "("+ battler.battler_id+") left the battle!"
    log_add = log_entry(battler, log_message)
    node_id = battler.getCharacter().getInstance().node_id
    node = db.Battle.objects.get(node_id = node_id)
    node.actions_log.append(log_add)
    node.save()
    return mw.node_return_upper(battler.battler_id)