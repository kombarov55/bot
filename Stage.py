#coding: utf-8

def updateUserToStage(userId, stage):
    db[userId]["stageId"] = stage

def findStageById(id):
    return list(filter(lambda x: x["id"] == id, stages))[0]

def getStage(userId):
    if userId in db: 
        stageId = db[userId]["stageId"]
        return findStageById(stageId)
    else:
        stageId = "Первое сообщение"
        db[userId] = {"stageId": stageId}
        return findStageById(stageId)

def processInput(currentStage, text):
    '''
    - по тексту найти stageId
    - найден?
      - найти следующий вариант по option.nextId=stage.id
      - найден? 
        - вернуть его 
        - вернуть что не понял и тд
    - вернуть что не понял и тд
    '''
    selectedOption = list(filter(lambda option: option["text"] == text, currentStage["options"]))
    optionFound = len(selectedOption) == 1
    if not optionFound:
        errorStage = createErrorStage(currentStage, "хмм.... не понял. Можно ещё раз?")
        
        return errorStage
    else:
        option = selectedOption[0]
        nextId = option["nextId"]
        selectedStage = list(filter(lambda stage: stage["id"] == nextId, stages))
        stageFound = len(selectedStage) == 1
        if not stageFound:
            errorStage = createErrorStage(currentStage, "не найден stage с id=" + nextId)

            return errorStage
        else:
            selectedStage = selectedStage[0]

            return selectedStage

def createErrorStage(currentStage, errorText): 
        stageWithErrorText = currentStage.copy()
        stageWithErrorText["text"] = errorText
        return stageWithErrorText

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
