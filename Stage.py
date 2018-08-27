 #coding: utf-8

def getStage(userId):
    if userId in db: 
        stageId = db[userId]["stageId"]
        return findStageById(stageId)
    else:
        return stages[0]

def getNextStage(stage, text):
    option = findOption(stage, text)
    if option is None: 
        return stage
    else:
        return findStageById(option["nextId"])

def saveUserAndStage(userId, stage):
    db[userId]["stageId"] = stage
    
def findStageById(id):
    return list(filter(lambda x: x["id"] == id, stages))[0]

def findOption(stage, text): 
    options = list(filter(lambda option: option["text"] == text, stage["options"]))
    if len(options) == 0: 
        return None
    else:
        return options[0]

def updateUserToStage(userId, stage):
    db[userId]["stageId"] = stage
    
        

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

db = {}
