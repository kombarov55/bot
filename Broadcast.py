#coding: utf-8

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from random import randint
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
    for userId, isSubscribed in db.items(): 
        if isSubscribed:
            stage = Stage.makePredictionStage(userId)
            stage["text"] = getGoodMorningText() + "А вот твоё предсказание на сегодня!\n" + stage["text"]
            print("send prediction to " + str(userId) + ": " + str(stage))
            ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])

def start():
    print("send loop")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = broadcast,
        trigger = IntervalTrigger(seconds = 5),
        id = "sendLoop",
        name = "send broadcast",
        replace_existing = True
    )
    atexit.register(lambda: scheduler.shutdown())

goodMorning = ["С добрым утром! &#128521;", "Доброе утро! &#128572;", "Доброе утро, друг! &#128524;", "Приветствую! &#128521;", "Доброе утро! &#128520;"]
def getGoodMorningText():
    i = randint(0, len(goodMorning - 1))
    return goodMorning[i]
