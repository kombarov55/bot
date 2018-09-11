#coding: utf-8

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

import ApiGate
import Predictions

#userId -> Boolean
db = {}

def subscribe(userId):
    print("Broadcast: subscribed user with userId=" + str(userId))
    db[userId] = True

def unsubscribe(userId):
    print("Broadcast: unsubscribed user with userId=" + str(userId))
    db[userId] = False

def start():
    print("send loop")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = p,
        trigger = IntervalTrigger(seconds = 1),
        id = "sendLoop",
        name = "send broadcast",
        replace_existing = True
    )
    atexit.register(lambda: scheduler.shutdown())

def broadcast():
    for userId, isSubscribed in db.items(): 
        if isSubscribed:
            msg = Predictions.getPrediction(userId)
            print("send prediction to " + userId ": " + msg)
            ApiGate.sendTextMessage(userId, msg)
            
