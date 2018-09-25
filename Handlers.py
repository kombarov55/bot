#coding: utf-8

import Stage
import ApiGate

def handle(userId, text, stage):
    if stage is None:
        nextStage = Stages.getDefaultStage()
        defaultRender(userId, stage)
    else:
        defaultHandle(userId, text, stage)


def defaultHandle(userId, text, stage):
    selectedOption = Stage.findOption(stage, text)
    invalidText = selectedOption is None

    if not invalidText: 
        nextId = option["nextId"]
        nextStage = Stage.findStageById(nextId)
        defaultRender(userId, nextStage)
    else:
        stage["text"] = "Я тебя не понял. Лучше выбери ответ!"
        defaultRender(userId, stage)

def defaultRender(userId, stage):
    ApiGate.sendKeyboardMessage(userId, stage)
