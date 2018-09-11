#coding: utf-8

from threading import Timer

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

def sendLoop():
    print("send loop")    
    #Timer(5.0, sendLoop).start() 
    
    #for userId, isSubscribed in db.items(): 
        #if isSubscribed:
            #msg = Predictions.getPrediction(userId)
            #print("send prediction to " + userId ": " + msg)
            #ApiGate.sendTextMessage(userId, msg)
