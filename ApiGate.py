#coding: utf-8

import vk
import json

import Stage

session = vk.Session()
api = vk.API(session, v=5.80)
myId=33167934
asyaId=226223557

def sendTextMessage(userId, text): 
    api.messages.send(access_token=token, user_id=userId, message=text)

def optionsToKeyboard(options):
    buttons = list(map(lambda option: [{"color": "default", "action": {"type": "text", "label": option["text"]}}], options))
    keyboard = {"one_time": True, "buttons": buttons}
    keyboard = json.dumps(keyboard, ensure_ascii = False)
    return keyboard

def sendKeyboardMessage(userId, text, options):
    keyboard = optionsToKeyboard(options)
    api.messages.send(access_token = token, user_id = userId, message = text, keyboard = keyboard)

def getUser(userId): 
    return api.users.get(user_id=userId, access_token=token)[0]

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
            api.messages.send(access_token = token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId], keyboard = keyboard)
        else: 
            api.messages.send(access_token = token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId])
    

# token = "d035b4ff7ff57a162c22eae2a4c036150fdb681dcbe7c406eaef510842aefe5a6b8155a6d751c972a6fd7"
#токен для тестовой группы
token = "bf0caf1fb36202a7489084a98ff6bf484f71120a44e952349f4c97c6b42b153ce7425cfde6f0d80220acc"
confirmation_token = "c40f8570"
