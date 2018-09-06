#coding: utf-8
from flask import Flask, request, json, Response
from datetime import datetime as dt
from random import randint
import sys
from collections import OrderedDict

import Predictions
import ApiGate
import Stage

from datetime import datetime as dt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!!!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    elif data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        userId = data['object']['peer_id']
        text = data["object"]["text"]

        currentStage = Stage.getStage(userId)
        nextStage = Stage.getNextStage(userId, currentStage, text)
        Stage.updateUserToStage(userId, nextStage)
        ApiGate.sendKeyboardMessage(userId, nextStage["text"], nextStage["options"])
        
        return "OK"
    else:
        return "OK"

def log(msg):
    timeStr = dt.now().strftime("%y-%m-%d %H:%M:%S")
    print(timeStr + "  " + msg)

def logRequest(userId, text, currentStage):
        log("user info: ")
        log("  userId=" + str(userId))
        log("  text=" + text)
        log("  currentStage=" + json.dumps(currentStage, ensure_ascii=False))
