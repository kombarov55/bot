 #coding: utf-8

from flask import json
import Predictions
from random import randint
from copy import deepcopy

def getStage(userId):
    if userId in db: 
        stageId = db[userId]["stageId"]
        return findStageById(stageId)
    else:
        return None

    

def getNextStage(userId, stage, text):
    if containsSwear(text):
        result = deepcopy(stage)
        result["text"] = getSwearResponse()
        return result

    if stage is None:
        return stages[0]

    option = findOption(stage, text)
    print("selectedOption=" + json.dumps(option, ensure_ascii=False))
    if option is None:
        print("ERROR: could not find option with " + text + " in " + json.dumps(stage, ensure_ascii = False))
        return stage
    else:
        nextId = option["nextId"]
        nextStage = findStageById(nextId)
        if nextId == "Результат предсказания":
            nextStage["text"] = Predictions.getPrediction(userId)
        return nextStage

def saveUserAndStage(userId, stage):
    db[userId]["stageId"] = stage

def findStageById(id):
    return list(filter(lambda x: x["id"] == id, stages))[0]

def findOption(stage, text): 
    options = list(filter(lambda option: option["text"] == text, stage["options"]))
    if len(options) == 0: 
        return None
    else:
        return options[0]

def updateUserToStage(userId, stage):
    if userId in db: 
        db[userId]["stageId"] = stage["id"]
    else:
        db[userId] = {"stageId": stage["id"]}

swears = ["сука", "блять", "нахуй", "хуй", "хуйня", "пизда", "пиздуй", "пиздец", "ебать"]
def containsSwear(str):
    lowerStr = str.lower()
    for w in swears:
        if w in lowerStr:
            return True
    return False

swearResponse = ["Нука. Не выражаться!", "Ещё раз и домой пойдешь!", "Ну и этому тебя учили родители?", "Ты этими губами целуешь свою маму?", "Как тебе не стыдно!"]
def getSwearResponse():
    i = randint(0, len(swearResponse))
    return swearResponse[i]
    
stages = [
    {
        "id": "Первое сообщение",
        "text": "Здравствуй, путник! Зачем ты пришёл к нам?",
        "options": [
            { "text": "Получить предсказание", "nextId": "Подтверждение предсказания"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Прощание" }
        ]
    },
    {
        "id": "Подтверждение предсказания",
        "text": "Отлично. Ты готов к тому чтобы узнать о завтрашнем дне?",
        "options": [
            { "text": "Глаголь ;)", "nextId": "Предсказание" },
            { "text": "Нет, спасибо.", "nextId": "Прощание" },
            { "text": "Ещё чего. Я сам творю свою судьбу.", "nextId": "Прощание" }
        ]
        
    },
    {
        "id": "Предсказание",
        "text": "Отлично! А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "скажи как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": " каждый день в 9 утра", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Результат предсказания",
        "text": "placeholder",
        "options": [
            { "text": "скажи как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу получать презсказания по утрам ;)", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Рассылка",
        "text": "Отлично, теперь тебе будут приходить предсказания каждый день в 9 утра. Не проспи ;)",
        "options": [
            { "text": "скажи как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу получать презсказания по утрам ;)", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Прощание",
        "text": "Чтож, это твой выбор. Удачи на твоём пути!",
        "options": [
            { "text": "Прости, я поспешил.", "nextId": "Предсказание" }
        ]
    } 
]

db = {}
