#coding: utf-8
from flask import Flask, request, json, Response
from datetime import datetime as dt
from random import randint
import vk
import sys
from collections import OrderedDict

'''
зашёл в чат:
Спрашиваем, хочет ли предсказание

Написал в 1 раз: 
  зависит от ответа. Далее либо прощание, либо "отлично, начнём". и клавиатура

Далее будет приходить только ответы с клавиатуры. 
Выбор: 
  1. Получить предсказание сейчас
  2. Подписаться на рассылку (?можно потом добавить выбор времени) / отписаться от рассылки
? 3. Задать вопрос (Возможно, тогда может какая нибудь пересылка)

Что связано с юзером?
  На какой стадии
  Когда обновлялось ему предсказание

Что есть у стадии: 
  id
  текст
  Варианты ответа

Хранится база, в которой лежат userId -> UserData
Хранятся стейджи в массиве. 

====================

Получить userid
Есть в userdata? 
  Завести запись на 0 stage
получить стейдж 
обработать ввод: 
  поменять при необходимости
  если ошибка - создать отдельный стейдж с текстом ошибки и ответами из предыдущего
отобразить его 

'''

app = Flask(__name__)

session = vk.Session()
api = vk.API(session, v=5.80)

userId_to_lastUpdateTime = {}
userId_to_prediction = {}

keyboard = {
    'one_time': True,
    'buttons':
    [
        [{
            'action': {
                'type': 'text',
                'label': "prediction",
            },
            'color': 'default'
        }],
        [{
            'action': {
                'type': 'text',
                'label': 'Подписаться на предсказания',
            },
            'color': 'primary'
        }]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False)

def getRandomPrediction():
    randIndex = randint(0, len(predictions))
    return predictions[randIndex]
    
def getPrediction(userId):
    now = dt.now()

    isFirstMessage = userId in userId_to_lastUpdateTime
    
    if isFirstMessage:
        userId_to_lastUpdateTime[userId] = now
        userId_to_prediction[userId] = getRandomPrediction()
        return 

    didNotUpdatePredictionToday = userId_to_lastUpdateTime[userId].day != now.day
    if didNotUpdatePredictionToday:
        prediction = getRandomPrediction()
        userId_to_lastUpdateTime[userId] = now
        userId_to_prediction[userId] = prediction
        return prediction
    else:
        return userId_to_prediction[userId]
    
#{userid -> {stageId: String, lastUpdateTime: Date}}
db = {}

def getStage(userId):
    if userId in db: 
        stageId = db[userId][stage]
        return findStageById(stageId)
    else:
        stageId = "Первое сообщение"
        db[userId] = {"stageId": stageId}
        return findStageById(stageId)

def updateStage(userId, stage):
    db[userId]["stageId"] = stage

def displayStage(userId, stage):
    message = stage["text"]
    options = list(map(lambda x: x["text"], stage["options"]))
    sendKeyboardMessage(userId, message, options)


stages = [
    {
        "id": "Первое сообщение",
        "text": "Здравствуй, путник! Зачем ты пришёл к нам?",
        "options": [
            { "text": "Получить предсказание", "nextId": "Подтверждение предсказания"},
            { "text": "Хочу задать вопрос", "nextId": "Вопрос" },
            { "text": "Ничего, просто смотрю", "nextId": "Прощание" }
        ]
    },
    {
        "id": "Подтверждение предсказания",
        "text": "Отлично. Ты готов к тому чтобы узнать о завтрашнем дне?",
        "options": [
            { "text": "Глаголь ;)", "nextId": "Предсказание" },
            { "text": "Нет, спасибо.", "nextId": "Прощание" },
            { "text": "Ещё чего. Я сам творю свою судьбу.", "nextId": "Прощание" }
        ]
        
    },
    {
        "id": "Предсказание",
        "text": "Отлично. Это твой выбор. А теперь скажи, чего тебе хочется!",
        "options": [
            { "text": "Пожалуйста, скажи как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу чтобы ты отсылал мне предсказания каждый день в 9 утра", "nextId": "Рассылка" }
        ]
    },
    {
        "id": "Результат предсказания"
    },
    {
        "id": "Рассылка"
    },
    {
        "id": "Прощание",
        "text": "Чтож, это твой выбор. Удачи на твоём пути! Если передумаешь - скажи ;)",
        "options": [
            { "text": "Прости, я поспешил. Впрочем, предсказание на сегодня мне бы не помешало. ", "nextId": "Предсказание" }
        ]
    } 
]

def findStageById(id):
    return list(filter(lambda x: x["id"] == id, stages))[0]

def sendTextMessage(userId, text): 
    api.messages.send(access_token=token, user_id=userId, message=text)

def sendKeyboardMessage(userId, text, options):

    buttons = []
    for option in options:
        action = OrderedDict()
        action["type"] = "text"
        action["label"] = option["text"]

        button = OrderedDict()
        button["action"] = action
        button["color"] = "default"

        buttons.append(button)

    keyboard = OrderedDict()
    keyboard["one_time"] = True
    keyboard["buttons"] = [buttons]
    keyboard = json.dumps(keyboard)
    api.messages.send(access_token = token, user_id = userId, message = text, keyboard = keyboard)
    
myId=33167934

@app.route('/')
def hello_world():
    return 'Hello, World!!!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        userId = data['object']['peer_id']
        text = data["object"]["text"]

        #currentStage = getStage(userId)
        #nextStage = processInput(currentStage, text)
        #updateStage(userId, currentStage)
        #displayStage(userId, currentStage)

        options = [
            { "text": "Пожалуйста, скажи как пройдёт сегодняшний день", "nextId": "Результат предсказания" },
            { "text": "Хочу чтобы ты отсылал мне предсказания каждый день в 9 утра", "nextId": "Рассылка" }
        ]

        sendKeyboardMessage(userId, "Выбор", options)
        return Response(status=200)

    predictions = [
    "Романтика создаст для вас новое направление",
    "С этого момента ваша ответственность принесет вам удачу"
    "Сегодня у вас будет эмоциональный день",
    "Обратите внимание на знаки, они вам укажут путь!",
    "Уделите больше времени отдыху и развлечениям",
    "Все, что вы искали прямо у вас под носом.",
    "Настало время попробовать что-то новое.",
    "Пришла пора выйти из зоны комфорта",
    "Терпение! Вы почти у цели",
    "Кто-то будет очень сильно волновать ваши чувства и эмоции",
    "Впереди поездка или путешествие",
    "Сегодня звезды советуют отказаться от алкоголя",
    'Погодка так и шепчет:"займи, но выпей',
    "Ты получишь необычный подарок",
    "Вы разочаруетесь в человеке которому доверяли",
    "Ваше будущее зависит от ваших поступков",
    "Поздравляем! Вы находитесь на верном пути.",
    "Покорив одну гору, начинай штурмовать другую...",
    "Прилив энергии поможет Вам справиться с большим объемом незапланированных работ.",
    "Примите то, что вы не можете изменить, и вы будете чувствовать себя лучше.",
    "Природа, время и терпение - три великих врача.",
    "Пришло время действовать!",
    "Пришло время закончить старое и начать новое.",
    "Пусть мир наполнится спокойствием и доброжелательностью.",
    "Работа с новыми партнерами будет очень выгодным.",
    "Работайте над дипломатическими способностями - они очень пригодятся для реализации идей.",
    "Размышляйте и не спешите с действиями.",
    "Разрешите состраданию направлять ваши решения.",
    "Результат Ваших действий может оказаться неожиданным.",
    "Сегодня у вас будет красивый день.",
    "Семь раз отмерьте, один раз отрежьте!",
    "Слушайте каждого. Идеи приходят отовсюду.",
    "Сосредоточьтесь на семье и гармонии с окружающим миром.",
    "Счастливая жизнь прямо перед вами.",
    "Теперь настало время попробовать что-то новое.",
    "Терпение! Вы почти у цели.",
    "Тот, кто знает, достаточно богат.",
    "Тот, кто не ждет благодарности, никогда не будет разочарован.",
    "Удача проводит Вас через все трудные времена.",
    "Уделите особое внимание старой дружбе.",
    "Физическая активность значительно улучшит ваши взгляды на жизнь сегодня.",
    "Хорошее время, чтобы закончить старые начинания.",
    "Хорошие новости придут к вам по почте.",
    "Хорошо сделанное лучше, чем хорошо сказанное.",
    "Хоть некоторые и пытаются вам помешать, вы все равно достигнете поставленных целей.",
    "Человек никогда не стар, чтобы учиться. Новые знания принесут Вам успех.",
    "Что ни делается - все к лучшему.",
    "Это время, чтобы двигаться. Ваше настроение улучшится.",
    "Вам предстоит рассмотреть неожиданное предложение",
    "Делайте то, чего просит душа и тело",
    "Не оставляйте усилий и получите желаемое",
    "Кто-то нуждается в вашей поддержке"
]


token = "bf0caf1fb36202a7489084a98ff6bf484f71120a44e952349f4c97c6b42b153ce7425cfde6f0d80220acc"
confirmationToken = "be8af98b"
