#coding: utf-8
from flask import Flask, request, json, Response
from datetime import datetime as dt
from random import randint
from collections import OrderedDict
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime as dt

import Predictions
import ApiGate
import Stage
import Broadcast





app = Flask(__name__)

import sys
print(sys.getdefaultencoding())

import platform
print(platform.python_version())

@app.route('/')
def hello_world():
    return 'Hello, World!!!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    print("app: " + str(data))
    if 'type' not in data.keys():
        return 'not vk'
    elif data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        userId = data['object']['peer_id']
        text = data["object"]["text"]
        msg_id = data["object"]["id"]

        print("app: incoming message: userId=" + str(userId) + " text=" + text)

        currentStage = Stage.getCurrentStage(userId)
        if currentStage is not None: 
            print("app: currentStage for userId=" + str(userId) + " is " + currentStage["id"])

        if currentStage is not None and currentStage["id"] == "Вопрос" or currentStage["id"] == "Задание вопроса" and Stage.findOption(currentStage, text) is None:
            forwardMessage(msg_id)
        
        nextStage = Stage.getNextStage(userId, currentStage, text)
        print("app: nextStage for userId=" + str(userId) + " is " + nextStage["id"])

        Stage.updateUserToStage(userId, nextStage)
        ApiGate.sendKeyboardMessage(userId, nextStage["text"], nextStage["options"])
        
        return "OK"
    else:
        return "OK"

app.wsgi_app = ProxyFix(app.wsgi_app)

Broadcast.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
