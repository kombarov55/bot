#coding: utf-8

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from random import randint
from datetime import datetime as dt
import atexit


import ApiGate
import Stage

#userId -> Boolean
db = {}

def subscribe(userId):
    db[userId] = True
    print("Broadcast: subscribed user with userId=" + str(userId))
    print("Broadcast: db=" + str(db))

def unsubscribe(userId):
    db[userId] = False    
    print("Broadcast: unsubscribed user with userId=" + str(userId))
    print("Broadcast: db=" + str(db))

def isSubscribed(userId):
    return userId in db

    
def broadcast():
    print("Broadcast: sending broadcast")
    print("Broadcast: isCorrectTiming? " + str(isCorrectTiming()))
    print("Broadcast: db=" + str(db))
    if isCorrectTiming():
        for userId, isSubscribed in db.items(): 
            if isSubscribed:
                stage = Stage.makePredictionStage(userId)
                print("send prediction to " + str(userId) + ": " + str(stage))
                
                ApiGate.sendTextMessage(userId, getGoodMorningText() + " А вот твоё предсказание на сегодня!")
                ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])

def isCorrectTiming():
    return dt.now().hour == 3
        
                
def start():
    print("send loop")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = broadcast,
        trigger = IntervalTrigger(seconds = 60),
        id = "sendLoop",
        name = "send broadcast",
        replace_existing = True
    )
    atexit.register(lambda: scheduler.shutdown())

goodMorning = ["С добрым утром! &#128521;", "Доброе утро! &#128572;", "Доброе утро, друг! &#128524;", "Приветствую! &#128521;", "Доброе утро! &#128520;"]
def getGoodMorningText():
    i = randint(0, len(goodMorning) - 1)
    return goodMorning[i]
