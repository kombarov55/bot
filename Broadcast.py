#coding: utf-8

from threading import Timer

import ApiGate
import Predictions

#userId -> Boolean
db = {}

def subscribe(userId):
    print("Broadcast: subscribed user with userId=" + userId)
    db[userId] = True

def unsubscribe(userId):
    print("Broadcast: unsubscribed user with userId=" + userId)
    db[userId] = False

def sendLoop():
    Timer(5.0, sendLoop).start()
    print("send loop")    
    #for userId, isSubscribed in db.items(): 
        #if isSubscribed:
            #msg = Predictions.getPrediction(userId)
            #print("send prediction to " + userId ": " + msg)
            #ApiGate.sendTextMessage(userId, msg)
