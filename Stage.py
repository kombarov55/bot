#coding: utf-8

from flask import json
from random import randint
from copy import deepcopy

import Broadcast
import Predictions

def getCurrentStage(userId):
    if userId in db: 
        stageId = db[userId]["stageId"]
        return findStageById(stageId)
    else:
        return None

def resetUser(userId):
    db[userId] = {"stageId": stages[0]["id"]}

def getNextStage(userId, stage, text):
    if containsSwear(text):
        reflectSwear(userId)
        return getSwearResponseJson(stage)

    if stage is None:
        return stages[0]

    option = findOption(stage, text)
    print("selectedOption=" + str(option))

    result = None

    if stage["id"] == "Мат":
        print('if stage["id"] == "Мат":')
        if containsExcuses(text) or option is not None: 
            swearMap[userId] = False
            nextId = stage["options"][0]["nextId"]
            result = deepcopy(findStageById(nextId))
            result["text"] = "Не делай так больше, пожалуйста) \n\n\n" + result["text"]
            return result
    
    if stage["id"] == "Мат" and option is None:
        print('if stage["id"] == "Мат" and option is None:')
        return getSwearRefusementJson(stage)
    
    if option is None and stage["id"] in ["Вопрос", "Задание вопроса"]:
        print('if option is None and stage["id"] not in ["Вопрос", "Задание вопроса"]:')
        result = deepcopy(stage)
        result["text"] = ""
    else:
        print("else:")
        nextId = option["nextId"]
        result = deepcopy(findStageById(nextId))
        if nextId == "Результат предсказания":
            result["text"] = Predictions.getPrediction(userId)
        elif nextId == "Рассылка":
            Broadcast.subscribe(userId)
        elif nextId == "Отписка":
            Broadcast.unsubscribe(userId)
        elif nextId == "Предсказание" and Broadcast.isSubscribed(userId):
            result = findStageById("Предсказание с включенной рассылкой")

        if didSwear(userId):
            result["text"] = "Не делай так больше, пожалуйста) \n\n\n" + result["text"]
    return result

def makeBroadcastPredictionStage(userId):
    result = deepcopy(findStageById("Результат предсказания"))
    result["text"] = Predictions.getPrediction(userId)
    result["options"] = findStageById("Рассылка")["options"]
    return result
    

def saveUserAndStage(userId, stage):
    db[userId]["stageId"] = stage

def findStageById(id):
    return list(filter(lambda x: x["id"] == id, stages))[0]

def findOption(stage, text):
    options = list(filter(lambda option: eqOption(text, option), stage["options"]))
    if len(options) == 0: 
        return None
    else:
        return options[0]

def eqOption(text, option): 
    return option["text"].lower() == text.lower()

def updateUserToStage(userId, stage):
    if userId in db: 
        db[userId]["stageId"] = stage["id"]
    else:
        db[userId] = {"stageId": stage["id"]}

swears = ["сука", "бля", "соси", "хер", "долбоеб", "блять", "нахуй", "хуй", "хуйня", "пизда", "пизду", "пиздуй", "пиздец", "ебать", "падла", "мразь", "пидор", "чмо", "пидорас", "жопа", "член", "мудак", "хуйло"]
def containsSwear(str):
    lowerStr = str.lower()
    for w in swears:
        if w in lowerStr:
            return True
    return False

swearResponse = ["&#128563; Нука. Не выражаться!", "Ещё раз и домой пойдешь! &#128545;", "Ну и этому тебя учили родители? &#128560;", "И этими губами целуешь свою маму? &#128541;", "Как тебе не стыдно! &#128548;"]
def getSwearResponse():
    i = randint(0, len(swearResponse) - 1)
    return swearResponse[i]

def getSwearResponseJson(stage):
    result = findStageById("Мат")
    result["text"] = getSwearResponse()

    nextId = None
    if stage["id"] == "Мат":
        nextId = stage["options"][0]["nextId"]
    else: 
        nextId = stage["id"]
    result["options"][0]["nextId"] = nextId
    
    return result

def getSwearRefusementJson(stage):
  result = getSwearResponseJson(stage)
  result["text"] = "Нет, так дело не пойдёт &#128545; Пока не извинишься, я с тобой не разговариваю!"
  return result


excuses = ["прости", "извини", "сожалею", "извиняюсь"]
def containsExcuses(str): 
  lowerStr = str.lower()
  for excuse in excuses: 
    if excuse in lowerStr: 
      return True
  return False


# userId -> Boolean
swearMap = {}
def didSwear(userId):
    didSwear = userId in swearMap and swearMap[userId] is True
    swearMap[userId] = False
    return didSwear

def reflectSwear(userId):
    swearMap[userId] = True

stages = [
    {
        "id": "Первое сообщение",
        "text": "Здравствуй, путник! Зачем ты пришёл к нам?",
        "options": [
            { "text": "Хочу предсказание)", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Ну смотри" }
        ]
    },
    {
        "id": "Ну смотри",
        "text": "Ну, смотри &#128516;",
        "options": [
            { "text": "Хотя знаешь, я надумал)", "nextId": "Что же" }
        ]
    },
    {
        "id": "Что же",
        "text": "Что же?)",
        "options": [
            { "text": "Хочу предсказание)", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Ну смотри" }
        ]
    },    
    {
        "id": "Как хочешь",
        "text": "Как хочешь &#128520;",
        "options": [
            { "text": "Кажется я передумал)", "nextId": "Замечательно" }
        ]
    },
    {
        "id": "Замечательно",
        "text": "Замечательно! Скажи чего же тебе хочется)",
        "options": [
            { "text": "Хочу предсказание)", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Ну смотри" }
        ]
    },    
    {
        "id": "Твой выбор",
        "text": "Тоже верно. Ну, как знаешь. Если всё же захочешь предсказания - пиши &#128524;",
        "options": [
            { "text": "Впрочем, пара предсказаний не помешают)", "nextId": "Предсказания не помешают" }
        ]
    },
        {
        "id": "Предсказания не помешают",
        "text": "Отлично! ",
        "options": [
            { "text": "Хочу предсказание)", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Ну смотри" }
        ]
    },     
    {
        "id": "Предсказание",
        "text": "Отлично! А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу получать предсказания по утрам ;)", "nextId": "Рассылка" },
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" }
        ]
    },
    {
        "id": "Предсказание с включенной рассылкой",
        "text": "Отлично! А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Я хочу прервать подписку", "nextId": "Отписка"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" }
        ]
    },
    {
        "id": "Результат предсказания",
        "text": "placeholder",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу получать презсказания по утрам ;)", "nextId": "Рассылка" },
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" }
        ]
    },
    {
        "id": "Рассылка",
        "text": "Отлично, теперь тебе будут приходить предсказания каждый день в 9 утра. Не проспи ;)",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Я хочу прервать подписку", "nextId": "Отписка"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" }
        ]
    },
    {
        "id": "Отписка",
        "text": "Чтож, твоё право &#127770; Отныне прекращаю высылать тебе предсказания по утрам",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу получать предсказания по утрам ;)", "nextId": "Рассылка" },
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" }
        ]
    },    
    {
        "id": "Назад",
        "text": "Конечно! &#128523; Я к твоим услугам!",
        "options": [
            { "text": "Получить предсказание", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Прощание" }
        ]
    },
    {
        "id": "Прощание",
        "text": "Чтож, это твой выбор. Удачи на твоём пути!",
        "options": [
            { "text": "Прости, я поспешил.", "nextId": "Предсказание" }
        ]
    },
    {
        "id": "Вопрос",
        "text": "Отлично. Ты можешь задать любой вопрос! Наши админы через какое то время ответят тебе. Если хочешь вновь получать предсказания - нажми или напиши 'Назад')",
        "options": [
            { "text": "Назад", "nextId": "Назад" }
        ]
    },
    {
        "id": "Задание вопроса",
        "text": "Вопрос отослан админам. В ближайшее время вам на него ответят",
        "options": [
            { "text": "Назад", "nextId": "Назад" }
        ]
    },    
    {
        "id": "Мат",
        "text": "placeholder",
        "options": [
            { "text": "Извини. Больше так не буду.", "nextId": "placeholder" }
        ]
    }
]

db = {}
