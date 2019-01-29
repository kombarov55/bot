#coding: utf-8

import vk
import json

import Stage
import Config

session = vk.Session()
api = vk.API(session, v=Config.apiVersion)

myId=33167934
asyaId=226223557


def sendTextMessage(userId, text): 
    api.messages.send(access_token=Config.token, user_id=userId, message=text)

def optionsToKeyboard(options):
    buttons = list(map(lambda option: [{"color": "positive", "action": {"type": "text", "label": option["text"]}}], options))
    keyboard = {"one_time": True, "buttons": buttons}
    keyboard = json.dumps(keyboard, ensure_ascii = False)
    return keyboard

def sendKeyboardMessage(userId, text, options):
    keyboard = optionsToKeyboard(options)
    text += "\n==================\n" + _keyboardAppendix(options)
    api.messages.send(access_token=Config.token, user_id = userId, message = text, keyboard = keyboard)

def getUser(userId): 
    return api.users.get(user_id=userId, access_token=Config.token)[0]

def optionsToButtons(options):
    textList = list(map(lambda option: option[0]["text"], options))
    buttons = list(map(lambda text: [{
        "color": "default",
        "action": {"type": "text", "label": text}
    }], textList))
    return buttons

recipients = [myId, asyaId]
def forwardMessage(msgId):
    for userId in recipients:
        currentStage = Stage.getCurrentStage(userId)
        if currentStage is not None:
            keyboard = optionsToKeyboard(currentStage["options"])
            api.messages.send(access_token = Config.token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId], keyboard = keyboard)
        else: 
            api.messages.send(access_token = Config.token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId])

def _keyboardAppendix(options):
    result = ""
    index = 1

    for option in options:
        result += str(index) + " - "
        result += option["text"]
        result += "\n"

        index += 1

    return result
