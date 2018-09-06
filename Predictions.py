#coding: utf-8

from random import randint
from datetime import datetime as dt

def getPrediction(userId):
    if notInDb(userId) or hasOutdatedPrediction(userId):
        predictionIndex = getRandomPredictionIndex()
        updateTime = dt.now()
        
        userIdToPredictionIndex[userId] = predictionIndex
        userIdToUpdateTime[userId] = updateTime

        return predictions[predictionIndex]
        
    else:
        predictionIndex = userIdToPredictionIndex[userId]
        return predictions[predictionIndex]

def getRandomPredictionIndex():
    return randint(0, len(predictions) - 1)

def notInDb(userId):
    return userId not in userIdToPredictionIndex

def hasOutdatedPrediction(userId):
    now = dt.now()
    summedNow = sumDays(now) 

    updateTime = userIdToUpdateTime[userId]
    summedUpdateTime = sumDays(updateTime)

    return summedNow > summedUpdateTime

def sumDays(date):
    return date.year * 365 + date.month + 30 + date.day

userIdToPredictionIndex = {}
userIdToUpdateTime = {}

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
