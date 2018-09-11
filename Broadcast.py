#coding: utf-8

from threading import Timer

import ApiGate
import Stage

#userId -> Boolean
db = {}

def subscribe(userId):
    db[userId] = True

def unsubscribe(userId):
    db[userId] = False

def sendLoop():
    Timer(5.0, sendLoop).start()
    for userId, isSubscribed in db.items():
        if isSubscribed: 
            stage = Stage.getPredictionStage(userId)
            ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])
