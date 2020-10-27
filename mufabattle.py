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

def copy_loot_to_node(chara):
    node = chara.getInstance()
    node.money_loot += chara.money
    counter = 0
    for item in node.loot:
        node.loot[counter] = item.to_dbref()
        counter +=1
    for item in chara.armor_equiped:
        if itemDrops(item.drop_chance):
            node.loot.append(item)
    for item in chara.weapons_equiped:
        if itemDrops(item.drop_chance):
            node.loot.append(item)
    for item in chara.inventory:
        if itemDrops(item.drop_chance):
            node.loot.append(item)
    node.save()

def monster_dead_share_exp(monster):
    #Calculate exp
    information_message = []
    members_seen = []
    member_to_update = []
    characters_to_give_exp = []
    for m in node.members:
        if m in members_seen: continue
        members_seen.append(m)
        if m.faction == 0 :
            for c in m.characters_list:
                if c.is_dead == False and c.getInstance() == node:
                    characters_to_give_exp.append(c)
                    member_to_update.append(m)
    expBonus = monster.experience/len(characters_to_give_exp)
    ctge_counter = 0
    for c in characters_to_give_exp:
        exLevel = c.level
        c.experience += expBonus
        c.checkLevel()
        if c.level > exLevel:
            information_message.append(c.name + " received **"+ str(expBonus) +"** XP and gained **"+ str(c.level - exLevel)+"** Levels!")
            information_message.append(":confetti_ball:CONGRATULATIONS!!!:confetti_ball:")
        else:
            information_message.append(c.name + " received **"+ str(expBonus) +"** XP.")
        member_to_update[ctge_counter].updateCharacterByName(c)
        member_to_update[ctge_counter].save()
    return information_message

def getBuff(character, buff_name):
    summ = 0
    fivePercent = ["EVASION_UP","PRECISION_UP"]
    onePercent = ["DAMAGE_UP","KARMA_UP"]
    for b in character.buffs:
        if b.name == buff_name:
            summ +=1
    if buff_name in onePercent:
        return summ
    elif buff_name in fivePercent:
        return 5*summ
    else:
        return 10*summ

def add_character_condition(character, condition):
    for c in character.conditions:
        if c.name == condition.name:
            if c.duration == -1:
                return
            elif c.duration >=0 and c.duration < condition.duration:
                c.duration = condition.duration
                c.date_added = condition.date_added
                return
    character.conditions.append(condition)
    return character
def has_condition(character, con_name):
    for c in character.conditions:
        if c.name == con_name:
            return True
    return False

def remove_condition(character, con_name):
    for c in character.conditions:
        if c.name == con_name:
            character.conditions.remove(c)
            break
    return character
    
def check_halting_conditions(pCharac):
    d_con_names = ["PETRIFIED", "DEAD", "ASLEEP", "FROZEN"]
    disabling_conditions = []
    for con in pCharac.conditions:
        if con.name in d_con_names:
            disabling_conditions.append(con.name)
    if len(disabling_conditions) == 0:
        return False
    else:
        return True

def calculate_total_AECR(charac):
    """ Calculates the total Armor Evasion Chance Reduction from all pieces of armor in a character"""
    value = 0
    for armor in charac.armor_equiped:
        if not isinstance(armor.name, db.Armor):
            value += 0
        else:
            value += armor.evasion_chance_reduction
    return value

def itemDrops(number):
    diceroll = random.randint(0,1000000)
    if number > diceroll:
        return True
    else:
        return False
def calculate_number_of_successes(number):
    successes = number // 100
    additional_success_chance = number % 100
    diceroll = random.randint(1,100)
    if additional_success_chance >= diceroll:
        successes += 1
    return successes

def deal_exhaustion(charac, exhaustion):
    charac.actions_left -= exhaustion
    con0 = charac.actions_left + charac.willpower <= 0
    con1 = charac.actions_left + charac.vitality <= 0
    con2 = charac.actions_left + charac.strength <= 0
    con3 = charac.actions_left + charac.agility <= 0
    if con0 or con1 or con2 or con3 :
        charac.kill()
    return charac
    

def deal_damage(charac, damage, information_message):
    charac.current_health -= damage
    if damage > 0 : 
        charac = remove_condition(charac,"ASLEEP")
        information_message.append(charac.name + " is no longer ASLEEP!")
    if charac.current_health <= 0:
        charac.kill()
        information_message.append(charac.name + " is now DEAD!")
    return charac
    
def attack(battler_attacker, battler_target, target_name, attack_type=0,reaction= False, reaction_to=0):
    should_react = not reaction
    information_message = []
    target = db.character()
    if isinstance(battler_target, db.Monster):
        target = battler_target.getCharacter()
    elif isinstance(battler_target, db.Player):
        target = battler_target.getCharacterByName(target_name)
    if target == None :
        information_message.append("ERROR: Can't find attack target!")
        return information_message
    attacker = battler_attacker.getCharacter()
    weapon = attacker.weapons_equiped[attack_type]
    if not isinstance(weapon, db.Weapon):
        information_message.append("ERROR: Can't perform this attack without equipping a weapon")
        return information_message
    total_AECR = calculate_total_AECR(target)
    
    ASCM = 1                # Attacker Strength Condition Modifier (ASCM)
    AACM = 1                #Attacker Agility Condition Modifier (AACM)
    TACM= 1                 #Target Agility Condition Modifier (TACM)
    if has_condition(attacker, "WEAKENED"):
        ASCM = 0.5
    if has_condition(attacker, "SLOWED"):
        AACM = 0.5
    if has_condition(attacker, "PARALYZED"):
        AACM = 0
    if has_condition(target, "SLOWED"):
        TACM = 0.5
    if has_condition(target, "PARALYZED"):
        TACM = 0
    
    #Calculate Number of Hits 
    attacker_precision = attacker.precision_base + attacker.agility*weapon.precision_scale*AACM +getBuff(attacker,"PRECISION_UP")
    if attack_type == 1 or attack_type ==3:
        attacker_precision = math.ceil(attacker_precision/2)
    if attack_type == 2:
        attack_precision = math.ceil(attacker_precision/4)
    if has_condition(attacker,"BLINDED"): 
        attacker_precision = 10
    target_evasion = max(target.evasion_base + target.agility*TACM - total_AECR +getBuff(target,"EVASION_UP") , 10)
    if reaction_to == 3:
        target_evasion += 100
    if has_condition(target,"DEAFENED"):
        target_evasion = 0
    hit_chance = max(attacker_precision - target_evasion,10)
    number_of_hits = calculate_number_of_successes(hit_chance)
    information_message.append(attacker.name+ " hit "+target.name+" **"+str(number_of_hits)+"** times.")
    
    #Calculate Hit Damage and on Hit effects 
    total_damage = 0
    total_exhaustion_damage = 0
    total_thorn_exhaustion_damage = 0
    
    
    amp_chance = attacker.strength*weapon.damage_amp_scale*ASCM
    if attack_type == 3:
        amp_chance = attacker.agility*weapon.damage_amp_scale*AACM
    
    condition_chances = []
    thorn_condition_chances = []
    thorn_condition_durations = []
    thorn_exhaustion = 0 
    target_armor_buffs = getBuff(target,"ARMOR_UP")
    damage_reduction_f = target_armor_buffs
    damage_reduction_p = target_armor_buffs
    for armor in target.armor_equiped:
        if isinstance(armor, db.Armor):
            thorn_exhaustion += armor.thorn_force_exhaustion_danage
            damage_reduction_f += armor.physical_damage_reduction_f
            damage_reduction_p += armor.physical_damage_reduction_p
    for condition in range(15):
        condition_chances[condition] = weapon.on_hit_condition_inflict_chance[condition]
        condition_chances[condition] -= target.condition_resistances[condition] +getBuff(target,db.Buffs(condition-9).name)
        condition_chances[condition] = max(0,condition_chances[condition])
        thorn_condition_chances[condition] = 0
        thorn_condition_durations[condition] = 0
        for target_armor in target.armor_equiped:
            if isinstance(target_armor, db.Armor):
                thorn_condition_chances[condition] += target_armor.thorn_condition_inflict_chance[condition]
                thorn_condition_durations[condition] += target_armor.thorn_condition_duration[condition]
        thorn_condition_chances[condition] -= attacker.condition_resistances[condition] +getBuff(attacker,db.Buffs(condition-9).name)
        thorn_condition_chances[condition] = max (0, thorn_condition_chances[condition]) 
    for hit in range(number_of_hits):
        damage += weapon.damage_base + calculate_number_of_successes(amp_chance)*damage_per_amp
        damage = math.ceil(damage(100 + getBuff(attacker,"DAMAGE_UP"))/100)
        for i in range(15):
            if calculate_number_of_successes(condition_chances[i]) >= 1 :
                condition_to_give = db.activeCondition(name = db.Conditions(i).name,
                                                        date_added = datetime.datetime.now(),
                                                        duration = weapon.on_hit_condition_duration[i]
                                                       )
                target = add_character_condition(target,condition_to_give)
                information_message.append(target.name + " is now `"+ condition_to_give.name+"`.")
            if calculate_number_of_successes(thorn_condition_chances[i]) >=1:
                condition_to_give = db.activeCondition(name = db.Conditions(i).name,
                                                        date_added = datetime.datetime.now(),
                                                        duration = thorn_condition_durations[i]
                                                       )
                attacker = add_character_condition(attacker,condition_to_give)
                information_message.append(attacker.name + " is now `"+ condition_to_give.name+"` due to a Thorn effect of "+target.name+".")
        if weapon.on_hit_force_exhaustion_damage > 0 :
            if calculate_number_of_successes(target.forced_exhaustion_resistance+ getBuff(target,"F_EXHAUSTION_RES_UP")) == 0:
                total_exhaustion_damage += weapon.on_hit_force_exhaustion_damage
        if thorn_exhaustion >0 :
            if calculate_number_of_successes(attacker.forced_exhaustion_resistance + getBuff(attacker,"F_EXHAUSTION_RES_UP")) == 0:
                total_thorn_exhaustion_damage+= thorn_exhaustion
        if attack_type != 2:
            damage = max(damage - damage_reduction_f, 0 )
        else:
            damage = damage +damage_reduction_f
        if attack_type !=1:
            damage = max(math.ceil(damage*(1 - damage_reduction_p/100)), 0)
        if attack_type == 2 and (has_condition(target, "FROZEN") or has_condition(target, "PETRIFIED")):
            damage = damage*2
            attacker = remove_condition(target,"FROZEN")
        information_message.append(attacker.name + " hit "+ target.name+" for **"+ str(damage)+"** damage:knife:.")
        total_damage += damage
    target = deal_damage(target,total_damage)
    information_message.append(attacker.name + " dealt a total of **"+ str(damage)+"** damage:knife: to "+ target.name+" after *"+str(number_of_hits)+" hits* .")
    target = deal_exhaustion(target,total_exhaustion_damage)
    information_message.append(target.name + " received exhaustion bringing down his **energy**:zap: by **"+ str(total_exhaustion_damage)+"**.")
    attacker = deal_exhaustion(target, total_thorn_exhaustion_damage)
    information_message.append(attacker.name + " received exhaustion from a Thorn effect, bringing down his **energy**:zap: by **"+ str(total_thorn_exhaustion_damage)+"**.")
    
    #Promote changes to the database objects 
    battler_attacker.updateCurrentCharacter(attacker)
    battler_target.updateCurrentCharacter(target)
    battler_attacker.save()
    battler_target.save()
    
    #Proceed with reaction
    if attacker.is_dead:
        #Add Loot to the Battle instance tables
        if isinstance(battler_attacker, db.Monster):
            copy_loot_to_node(attacker)
            information_message += monster_dead_share_exp(attacker)
        should_react = False
        information_message.append(attacker.name + " died so "+ target.name + " doesn't attack him back.")
    if target.is_dead:
        #Add Loot to the Battle instance tables
        if isinstance(battler_attacker, db.Monster):
            copy_loot_to_node(target)
            information_message += monster_dead_share_exp(target)
        should_react = False
        information_message.append(target.name + " died and can't attack back.")
    elif check_halting_conditions(target):
        should_react = False
        information_message.append(target.name + " is not capable of attacking back.")
    
    
    if should_react == False:
        return information_message
    else:
        if action_type == 3:
            return information_message + slash(battler_target, battler_attacker, attacker.name ,True, 3)
        else:
            return information_message + slash(battler_target, battler_attacker, attacker.name ,True, action_type)


    