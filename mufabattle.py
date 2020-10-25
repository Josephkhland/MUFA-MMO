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

def add_character_condition(character, condition):
    for c in character.conditions
        if c.name == condition.name:
            if c.duration = -1:
                return
            elif c.duration >=0 and c.duration < condition.duration:
                c.duration = condition.duration
                c.date_added = condition.date_added
                return
    character.conditions.append(condition)
    return character

def calculate_total_AECR(charac):
    """ Calculates the total Armor Evasion Chance Reduction from all pieces of armor in a character"""
    value = 0
    for armor in charac.armor_equiped:
        value += armor.evasion_chance_reduction
    return value

def calculate_number_of_successes(number):
    successes = number // 100
    additional_success_chance = number % 100
    diceroll = random.randint(1,100)
    if additional_success_chance >= diceroll:
        successes += 1
    return successes
    
def slash(battler_attacker, target):
    attacker = battler_attacker.getCharacter()
    weapon = attacker.weapons_equiped[0]
    total_AECR = calculate_total_AECR(attacker)
    
    #Calculate Number of Hits 
    attacker_precision = attacker.precision_base + attacker.agility*weapon.precision_scale
    target_evasion = max(target.evasion_base + target.agility - total_AECR, 10)
    hit_chance = max(attacker_precision - target_evasion,10)
    number_of_hits = calculate_number_of_successes(hit_chance)
    
    #Calculate Hit Damage and on Hit effects 
    total_damage = 0
    total_exhaustion_damage = 0
    total_thorn_exhaustion_damage = 0
    
    amp_chance = attacker.strength*weapon.damage_amp_scale
    condition_chances = []
    thorn_condition_chances = []
    thorn_condition_durations = []
    thorn_exhaustion = 0 
    for armor in target.armor_equiped:
        thorn_exhaustion += armor.thorn_force_exhaustion_danage
    for condition in range(15):
        condition_chances[condition] = weapon.on_hit_condition_inflict_chance[condition]
        condition_chances[condition] -= target.condition_resistances[condition]
        condition_chances[condition] = max(0,condition_chances[condition])
        thorn_condition_chances[condition] = 0
        thorn_condition_durations[condition] = 0
        for target_armor in target.armor_equiped:
            thorn_condition_chances[condition] += target_armor.thorn_condition_inflict_chance[condition]
            thorn_condition_durations[condition] += target_armor.thorn_condition_duration[condition]
        thorn_condition_chances[condition] -= attacker.condition_resistances[condition]
        thorn_condition_chances[condition] = max (0, thorn_condition_chances[condition]) 
    for hit in range(number_of_hits):
        damage += weapon.damage_base + calculate_number_of_successes(amp_chance)*damage_per_amp
        for i in range(15):
            if calculate_number_of_successes(condition_chances[i]) >= 1 :
                condition_to_give = db.activeCondition(name = db.Conditions(i).name,
                                                        date_added = datetime.datetime.now(),
                                                        duration = weapon.on_hit_condition_duration[i]
                                                       )
                target = add_character_condition(target,condition_to_give)
            if calculate_number_of_successes(thorn_condition_chances[i]) >=1:
                condition_to_give = db.activeCondition(name = db.Conditions(i).name,
                                                        date_added = datetime.datetime.now(),
                                                        duration = thorn_condition_durations[i]
                                                       )
                attacker = add_character_condition(attacker,condition_to_give)
        if weapon.on_hit_force_exhaustion_damage > 0 :
            if calculate_number_of_successes(target.forced_exhaustion_resistance) == 0:
                total_exhaustion_damage += weapon.on_hit_force_exhaustion_damage
        if thorn_exhaustion >0 :
            if calculate_number_of_successes(attacker.forced_exhaustion_resistance) == 0:
                total_thorn_exhaustion_damage+= thorn_exhaustion