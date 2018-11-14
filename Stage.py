#coding: utf-8

from flask import json
from random import randint

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
    if stage is None:
        return stages[0]

    option = findOption(stage, text)
    currentId = stage["id"];

    #Фильтр мата: если сматерились, то переходим на стадию "Мат" и отражаем мат для проверки в следующем сообщении
    if containsSwear(text):
        reflectSwear(userId)
        return getSwearResponseJson(stage)

    if stage["id"] == "Мат":
        clickedExcuseButton = option is not None

        if containsExcuses(text) or clickedExcuseButton:
            return createExcuseStage(userId, stage)
        else:
            return getSwearRefusementJson(stage)

    ####################
    result = None

    if option is None and stage["id"] not in ["Вопрос", "Задание вопроса"]:
        result = stage
        result["text"] = "Я тебя не понял. Лучше выбери ответ!"
    else:
        nextId = option["nextId"]

        result = findStageById(nextId)
        result = result

        #Вставка предсказания в ответ, если нажали на предсказание
        if nextId == "Результат предсказания":
            result["text"] = Predictions.getPrediction(userId)

        #Установка статуса подписки (Хочу получать предсказания по утрам / хочу прервать подписку)
        if shouldChangeSubscriptionStatus(result):
            changeSubscriptionStatus(userId, result)

        #Подписаться, когда нажали на кнопку подписки
        if nextId == "Рассылка":
            Broadcast.subscribe(userId)

        #Отписаться, когда нажали на кнопку отписки
        if nextId == "Отписка":
            Broadcast.unsubscribe(userId)

    return result

def shouldChangeSubscriptionStatus(stage):
    currentId = stage["id"]
    requiredIds = [
        "Предсказание",
        "Предсказание с включенной рассылкой",
        "Результат предсказания",
        "Рассылка",
        "Отписка"
    ]

    return currentId in requiredIds

def changeSubscriptionStatus(userId, stage):
    currentId = stage["id"]
    optionToChange = stage["options"][1]
    finalText = None

    if Broadcast.isSubscribed(userId) is False:
        finalText = "Хочу получать предсказания по утрам ;)"
    else:
        finalText = "Я хочу прервать подписку"

    optionToChange["text"] = finalText


def makeBroadcastPredictionStage(userId):
    result = findStageById("Результат предсказания")
    result["text"] = Predictions.getPrediction(userId)
    result["options"] = findStageById("Рассылка")["options"]
    return result

def createExcuseStage(userId, currentStage):
    swearMap[userId] = False

    nextId = currentStage["options"][0]["nextId"]
    nextStage = findStageById(nextId)
    nextStage = nextStage
    nextStage["text"] = "Не делай так больше, пожалуйста) \n\n\n" + currentStage["text"]

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
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
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
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
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
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
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
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Ничего, просто смотрю", "nextId": "Ну смотри" }
        ]
    },
    {
        "id": "Предсказание",
        "text": "Отлично! А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            {"text": "Хочу задать вопрос админу группы", "nextId": "Вопрос"},
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Хочу получать предсказания по утрам ;)", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Предсказание с включенной рассылкой",
        "text": "Отлично! А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Я хочу прервать подписку", "nextId": "Отписка"}
        ]
    },
    {
        "id": "Результат предсказания",
        "text": "placeholder",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Хочу получать презсказания по утрам ;)", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Рассылка",
        "text": "Отлично, теперь тебе будут приходить предсказания каждый день в 9 утра. Не проспи ;)",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Я хочу прервать подписку", "nextId": "Отписка"}
        ]
    },
    {
        "id": "Отписка",
        "text": "Чтож, твоё право &#127770; Отныне прекращаю высылать тебе предсказания по утрам",
        "options": [
            { "text": "Скажи, как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
            { "text": "Хочу получать предсказания по утрам ;)", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Назад",
        "text": "Конечно! &#128523; Я к твоим услугам!",
        "options": [
            { "text": "Получить предсказание", "nextId": "Предсказание"},
            { "text": "Хочу задать вопрос админу группы", "nextId": "Вопрос" },
            { "text": "Хочу задать вопрос тарологу", "nextId": "Вопрос тарологу" },
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
    },
    {
        "id": "Вопрос тарологу",
        "text": "Отлично, тогда напиши вопрос, который тебя интересует. Через какое то время таролог свяжется и через группу проведёт консультацию. Учтите, что трактовку могут сказать не сразу, а в течение недели. ",
        "options": [
        { "text": "Назад", "nextId": "Назад" }
    ]
    }
]


db = {}
