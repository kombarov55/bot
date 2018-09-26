#coding: utf-8

from copy import deepcopy
from random import randint

def didSwear(str):
    lowerStr = str.lower()
    for w in swears:
        if w in lowerStr:
            return True
    return False

def getSwearStage():
    return deepcopy(swearStage)

def getSwearStage(stage):
    nextStage = deepcopy(swearStage)
    nextStage["text"] = getSwearResponse()

    nextId = None
    if stage["id"] == "Мат":
        nextId = stage["options"][0]["nextId"]
    else: 
        nextId = stage["id"]
    nextStage["options"][0]["nextId"] = nextId
    
    return nextStage

def getRandomSwearResponseText():
    i = randint(0, len(swearResponses) - 1)
    return swearResponses[i]

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

swearStage = {
        "id": "Мат",
        "text": "placeholder",
        "options": [
            { "text": "Извини. Больше так не буду.", "nextId": "placeholder" }
        ]
}

swears = ["сука", "бля", "соси", "хер", "долбоеб", "блять", "нахуй", "хуй", "хуйня", "пизда", "пизду", "пиздуй", "пиздец", "ебать", "падла", "мразь", "пидор", "чмо", "пидорас", "жопа", "член", "мудак", "хуйло"]

swearResponses = ["&#128563; Нука. Не выражаться!", "Ещё раз и домой пойдешь! &#128545;", "Ну и этому тебя учили родители? &#128560;", "И этими губами целуешь свою маму? &#128541;", "Как тебе не стыдно! &#128548;"]
