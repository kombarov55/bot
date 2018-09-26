#coding: utf-8

import vk
import json

import Stage

session = vk.Session()
api = vk.API(session, v=5.80)
myId=33167934

def sendTextMessage(userId, text): 
    api.messages.send(access_token=token, user_id=userId, message=text)

def optionsToKeyboard(options):
    buttons = list(map(lambda option: [{"color": "default", "action": {"type": "text", "label": option["text"]}}], options))
    keyboard = {"one_time": True, "buttons": buttons}
    keyboard = json.dumps(keyboard, ensure_ascii = False)
    return keyboard

def sendKeyboardMessage(userId, text, options):
    keyboard = optionsToKeyboard(options)
    print("ApiGate: sendKeyboardMesssge")
    print("\t\t\t user_id=" + str(userId) + " message=" + text + " keyboard=" + str(keyboard))
    api.messages.send(access_token = token, user_id = userId, message = text, keyboard = keyboard)

def optionsToButtons(options):
    textList = list(map(lambda option: option[0]["text"], options))
    buttons = list(map(lambda text: [{
        "color": "default",
        "action": {"type": "text", "label": text}
    }], textList))
    return buttons

recipients = [myId]
def forwardMessage(msgId):
    for userId in recipients:
        currentStage = Stage.getCurrentStage(userId)
        if currentStage is not None:
            keyboard = optionsToKeyboard(currentStage["options"])
            api.messages.send(access_token = token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId], keyboard = keyboard)
        else: 
            api.messages.send(access_token = token, user_id = userId, message = "Нам в группе задали вопрос:", forward_messages = [msgId])
    

keyboard_json = {
    "one_time": True,
    "buttons":
    [
        [
            {
                "action":{
                    "type": "text",
                    "label": "blue"
                },
                "color": "default"
            }
        ],
        [
            {
                "action":{
                    "type": "text",
                    "label": "red"
                },
                "color": "default"
            }
        ]
    ]
}

keyboard_json = json.dumps(keyboard_json)

token = "bf0caf1fb36202a7489084a98ff6bf484f71120a44e952349f4c97c6b42b153ce7425cfde6f0d80220acc"
confirmation_token = "c40f8570"
