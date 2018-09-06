 #coding: utf-8

import Predictions
import Stage 

db = {}

def entry(userId, stageId = None, lastUpdateTime = None, predictionIndex = None):
    return {"userId": userId, "stageId": stageId, "lastUpdateTime": lastUpdateTime, "predictionIndex": predictionIndex}

def add(userId):
    entry = entry(userId)
    db[userId] = entry
    return entry

def get(userId):
    if userId in db:
        return db["usreId"]
    else:
        return None


def updateUserToStage(userId, stage):
    entry = db[userId]
    entry["stageId"] = stage["id"]


     



 
     
