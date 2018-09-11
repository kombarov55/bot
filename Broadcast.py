#coding: utf-8

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

import ApiGate
import Stage

#userId -> Boolean
db = {}

def subscribe(userId):
    print("Broadcast: subscribed user with userId=" + str(userId))
    db[userId] = True

def unsubscribe(userId):
    print("Broadcast: unsubscribed user with userId=" + str(userId))
    db[userId] = False
    
def broadcast():
    print("brodcast")
    for userId, isSubscribed in db.items(): 
        if isSubscribed:
            stage = Stage.makePredictionStage(userId)
            print("send prediction to " + str(userId) + ": " + str(stage))
            ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])

def start():
    print("send loop")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = broadcast,
        trigger = IntervalTrigger(seconds = 1),
        id = "sendLoop",
        name = "send broadcast",
        replace_existing = True
    )
    atexit.register(lambda: scheduler.shutdown())
