#coding: utf-8

import vk
import json

session = vk.Session()
api = vk.API(session, v=5.80)
myId=33167934

def sendTextMessage(userId, text): 
    api.messages.send(access_token=token, user_id=userId, message=text)

def optionsToKeyboard(options):
    buttons = list(map(lambda option: [{"color": "default", "action": {"type": "text", "label": option["text"]}}], options))
    keyboard = {"one_time": True, "buttons": buttons}
    keyboard = json.dumps(keyboard).encode("utf-8")
    return keyboard

def sendKeyboardMessage(userId, text, options):
    keyboard = optionsToKeyboard(options)
    api.messages.send(access_token = token, user_id = userId, message = text, keyboard = keyboard)

def optionsToButtons(options):
    textList = list(map(lambda option: option[0]["text"], options))
    buttons = list(map(lambda text: [{
        "color": "default",
        "action": {"type": "text", "label": text}
    }], textList))
    return buttons

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
confirmationToken = "be8af98b"
