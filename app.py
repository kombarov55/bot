#coding: utf-8
from flask import Flask, request, json, Response
from datetime import datetime as dt
from random import randint
import sys
from collections import OrderedDict

import Predictions
import ApiGate
import Stage

app = Flask(__name__)

import sys
print(sys.getdefaultencoding())

def displayStage(userId, stage):
    message = stage["text"]
    options = list(map(lambda x: x["text"], stage["options"]))
    ApiGate.sendKeyboardMessage(userId, message, options)

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
        nextStage = Stage.getNextStage(currentStage, text) 
        #Stage.updateUserToStage(userId, currentStage)
        msg = {"userid": "asdf фыва", "msg": "1123"}
        msg = json.dumps(msg)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(msg)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        ApiGate.sendTextMessage(userId, msg)
        
        return Response(status=200)
