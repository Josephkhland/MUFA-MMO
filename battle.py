import random
import mufadb as db 
import mongoengine

def create():
    stored_var = db.Instance().save()
    print(type(stored_var.id))
    return stored_var.id
    
def join(instance_id, applicant: db.Battler , side: int = 0):
    if side == 0:
        db.Instance().objects(id=instance_id).update(push__participants_side_A = applicant)
    else:
        db.Instance().objects(id=instance_id).update(push__participants_side_B = applicant)

def leave(instance_id, applicant: db.Battler, side: int = 0):
    temp_obj = db.Instance().objects(id=instance_id)
    try:
        if side == 0:
            db.Instance().objects(id=instance_id).update(participants_side_A = temp_obj.remove(temp_obj.applicant))
        else:
            db.Instance().objects(id=instance_id).update(participants_side_B = temp_obj.remove(temp_obj.applicant))
    except ValueError:
        debug_message_to_print = "Can't find Battler object in the given Instance("+instance_id+")."
        print(debug_message_to_print)

def clean():
    #Deletes instances with no Participants
    pass