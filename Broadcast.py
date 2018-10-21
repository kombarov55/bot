#coding: utf-8

import atexit
from datetime import datetime as dt
from random import randint

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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

def start():
    print("send loop")
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func = _broadcast,
        trigger = IntervalTrigger(seconds = 59),
        id = "sendLoop",
        name = "send broadcast",
        replace_existing = True
    )
    atexit.register(lambda: scheduler.shutdown())

def _broadcast():
    print("Broadcast: sending broadcast")
    print("Broadcast: isCorrectTiming? " + str(_isCorrectTiming()))
    print("Broadcast: db=" + str(db))
    if _isCorrectTiming():
        for userId, isSubscribed in db.items(): 
            if isSubscribed:
                stage = Stage.makeBroadcastPredictionStage(userId)
                print("send prediction to " + str(userId) + ": " + str(stage))
                ApiGate.sendTextMessage(userId, _getGoodMorningText() + " А вот твоё предсказание на сегодня!")
                ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])

def _isCorrectTiming():
    now = dt.now()
    return now.hour == 9 and now.minute == 0

_goodMorning = ["С добрым утром! &#128521;", "Доброе утро! &#128572;", "Доброе утро, друг! &#128524;", "Приветствую! &#128521;", "Доброе утро! &#128520;"]
def _getGoodMorningText():
    i = randint(0, len(_goodMorning) - 1)
    return _goodMorning[i]
