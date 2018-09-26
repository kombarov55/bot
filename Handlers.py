#coding: utf-8

import Stage
import ApiGate
import Predictions
import Swear

def handle(userId, text, stage):
    if stage is None:
        nextStage = Stage.getDefaultStage()
        defaultHandleNextStage(userId, stage)
    else:
        if Swear.didSwear(text) and stage["id"] != "Мат":
            handleOnFirstSwear(userId, text, stage)
        elif stage["id"] == "Мат"

        if stage["id"] == "Результат предсказания":
            handleOnPrediction(userId, text, stage)
        else:
            defaultHandleCurrentStage(userId, text, stage)
    # сохранить прогресс пользователя

def defaultHandleCurrentStage(userId, text, currentStage):
    textIsValid = Stage.isTextValid(currentStage, text)
    if textIsValid: 
        nextId = option["nextId"]
        nextStage = Stage.findStageById(nextId)
        defaultHandleNextStage(userId, nextStage)
    else:
        stage["text"] = "Я тебя не понял. Лучше выбери ответ!"
        defaultHandleNextStage(userId, currentStage)

def handleOnFirstSwear(userId, text, currentStage):
    nextStage = Swear.getSwearStage(stage)
    nextStage["text"] = Swear.getRandomSwearResponseText()
    nextStage["options"][0]["nextId"] = currentStage["id"]
    
    defaultHandleNextStage(nextStage)

def handleOnPrediction(userId, text, currentStage):
    textIsValid = Stage.isTextValid(currentStage, text)
    if textIsValid:
        nextId = option["nextId"]
        if nextId == "Результат предсказания":
            predictionHandleNextStage(userId, currentStage)
        else:
            nextStage = Stage.findStageById(nextId)
            defaultHandleNextStage(nextStage)

def defaultHandleNextStage(userId, stage):
    ApiGate.sendKeyboardMessage(userId, stage)

def predictionHandleNextStage(userId, stage):
    prediction = Predictions.getPrediction(userId)
    stage["text"] = prediction
    ApiGate.sendKeyboardMessage(userId, stage)

