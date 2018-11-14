#coding: utf-8
from flask import Flask, request, json
from werkzeug.contrib.fixers import ProxyFix

import ApiGate
import Broadcast
import Stage
import Tracer

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
    if 'type' not in data.keys():
        return 'ok'
    elif data['type'] == 'confirmation':
        return ApiGate.confirmation_token
    elif data['type'] == 'message_new':
        userId = data['object']['peer_id']
        text = data["object"]["text"]
        msg_id = data["object"]["id"]

        if text == "RESET!":
            Stage.resetUser(userId)
            stage = Stage.stages[0]
            ApiGate.sendKeyboardMessage(userId, stage["text"], stage["options"])
            return "ok"
            
        currentStage = Stage.getCurrentStage(userId)

        isQuestionStage = currentStage is not None and (currentStage["id"] == "Вопрос" or currentStage["id"] == "Задание вопроса") or currentStage["id"] == "Вопрос тарологу"
        if isQuestionStage:
            option = Stage.findOption(currentStage, text)
            asked = option is None
            if asked:
                ApiGate.forwardMessage(msg_id)
                return "ok"

        nextStage = Stage.getNextStage(userId, currentStage, text)

        Stage.updateUserToStage(userId, nextStage)
        ApiGate.sendKeyboardMessage(userId, nextStage["text"], nextStage["options"])
        Tracer.logUser(userId)
        return "ok"
    else:
        return "ok"

app.wsgi_app = ProxyFix(app.wsgi_app)

Broadcast.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

