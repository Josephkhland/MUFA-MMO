import time, threading
import math 
import datetime
import mufadb as db
import mufabattle as mb

StartTime=time.time()

def action() :
    print('action ! -> time : {:.1f}s'.format(time.time()-StartTime))

def solve_conditions(hourly= False, tworly = False):
    battlers = db.Battler.objects.no_dereference()
    for b in battlers:
        if isinstance(b, db.Player):
            for pCharac in b.characters_list:
                to_remove = []
                for con in pCharac.conditions:
                    if con.duration == -1:
                        continue
                    else :
                        end_time = condition.date_added + timedelta(hours =condition.duration)
                        if (datetime.now() >= end_time):
                            to_remove.append(con)
                for i in to_remove:
                    pCharac.conditions.remove(i)
                if hourly:
                    if mb.has_condition(pCharac,"CURSED") or mb.has_condition(pCharac,"DEAD") or mb.has_condition(pCharac, "BLEEDING"):
                        pass
                    else: 
                        pCharac.current_health = min(pCharac.vitality*10, math.ceil(pCharac.current_health+ (pCharac.vitality*0.1)))
                        pCharac.actions_left = pCharac.max_actions
                if tworly:
                    pCharac.current_sanity = min(pCharac.willpower*10, math.ceil(pCharac.current_sanity+ (pCharac.willpower*0.1)))
            
                b.updateCharacterByName(pCharac)
                b.save()
        elif isinstance (b, db.Monster):
            pCharac = b.getCharacter()
            to_remove = []
            for con in pCharac.conditions:
                if con.duration == -1:
                    continue
                else :
                    end_time = condition.date_added + timedelta(hours =condition.duration)
                    if (datetime.now() >= end_time):
                        to_remove.append(con)
            for i in to_remove:
                pCharac.conditions.remove(i)
            if hourly:
                if mb.has_condition(pCharac,"CURSED") or mb.has_condition(pCharac,"DEAD") or mb.has_condition(pCharac, "BLEEDING"):
                    pass
                else: 
                    pCharac.current_health = min(pCharac.vitality*10, math.ceil(pCharac.current_health+ (pCharac.vitality*0.1)))
                    pCharac.actions_left = pCharac.max_actions
            if tworly:
                pCharac.current_sanity = min(pCharac.willpower*10, math.ceil(pCharac.current_sanity+ (pCharac.willpower*0.1)))
            b.character_stats = pCharac
            b.save()
    log_message = datetime.datetime.now().ctime() + " : Completed Interval Update"
    if hourly: 
        log_message += " | hourly == TRUE"
    if tworly: 
        log_message += " | tworly == TRUE"
    print(log_message)
            
class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        self.seconds_passed = datetime.datetime.now().minute*60
        if datetime.datetime.now().hour % 2 == 0:
            self.seconds_passed += 0
        else:
            self.seconds_passed += 3600
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            self.seconds_passed = (self.seconds_passed+self.interval)%7200
            if self.seconds_passed == 3600:
                nextTime+=self.interval
                self.action(True,False)
            elif self.seconds_passed == 0:
                nextTime+=self.interval
                self.action(False,True)
            else: 
                nextTime+=self.interval
                self.action(False,False)
                
            

    def cancel(self) :
        self.stopEvent.set()


def update():
    inter = setInterval(30,solve_conditions)
    
# start action every 60s
#inter=setInterval(30,solve_conditions)
#print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))
# will stop interval in 5s
#t=threading.Timer(5,inter.cancel)
#t.start()

