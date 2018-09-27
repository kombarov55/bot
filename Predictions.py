#coding: utf-8

from random import randint
from datetime import datetime as dt
import FileUtils

userIdToUpdateTimePath = "data/userIdToUpdateTime"
userIdToPredictionIndexPath = "data/userIdToPredictionIndex"

def getPrediction(userId):
    if notInDb(userId) or hasOutdatedPrediction(userId):
        predictionIndex = getRandomPredictionIndex()
        updateTime = dt.now()
        
        userIdToPredictionIndex[userId] = predictionIndex
        userIdToUpdateTime[userId] = updateTime

        FileUtils.saveDict(userIdToUpdateTime, userIdToUpdateTimePath)
        FileUtils.saveDict(userIdToPredictionIndex, userIdToPredictionIndexPath)

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

userIdToPredictionIndex = FileUtils.readDict(userIdToPredictionIndexPath)
userIdToUpdateTime = FileUtils.readDict(userIdToUpdateTimePath)

predictions = [
    "Сегодня вы испытаете ожидаемое удивление и вспомните старых знакомых. Помимо этого, возможно впадение в легкую ностальгию, но не увлекайтесь, так как у вас найдутся более важные и интересные дела.",
    "Ваш день будет насыщенным, но зависит это только от того, решитесь ли вы преодолеть свой страх и узнать что-то новое. Не отчаивайтесь, если что-то не получится с первого раза.",
    "Сегодняшний день будет благополучен в творческой сфере, если вы уделите больше внимания себе и своим эмоциям, не будете их зажимать, то почувствуете очень приятное облегчение. У вас будет шанс решить, либо дать себе свободу, либо продолжить корчить приличного и спокойного человека.",
    "День будет спокойным и вы будете удовлетворены результатами. Но пожалуй, завышенные ожидания окажутся несколько неприятными, потому что будет ощущения легкого разочарования, если вы будете слишком требовательны.",
    "Сегодня вы должны блистать, поверьте в свою силу и много добьетесь. Не советую слушать других людей, их претензии могут быть либо из зависти, либо от личного настроения.",
    "Сегодня уделите больше времени работе и завершению дел. В конце вечера возможен приятный бонус и конечно же удовлетворение от оконченной работы. В случае лентяйства, вас будет ожидать досада.",
    "Сегодняшний день благоприятен для более магического образа жизни, позвольте себе немного помедитировать на воду, успокоить нервы. Вы будете гораздо лучше себя чувствовать после этого.",
    "Сегодняшний день пройдет сумбурно, многое может выходить из под контроля и очень советую вам держать себя в руках. Следите за тем, что говорите, многих вы можете неосознанно обидеть неосторожным словом.",
    "Сегодняшний день может оказаться сложным, так что с самого начала дня настройтесь на позитивное настроение и что бы не случилось, держитесь. Вы сильный человек, поверьте в это и сможете преодолеть практически все!",
    "Бот предсказатель настоятельно рекомендует, чтобы вы выбирали для себя дорогу, работу или отношения, только следуя велениям сердца и непременно добровольно. От этого сегодня зависит ваше будущее счастье.",
    "Сегодняшний день  ознаменует для вас выбор. Советую вам больше не колебаться и не медлить, ожидая доступа к дополнительной информации, а вместо этого, не теряя времени, начинать действовать и претворять в жизнь свои планы.",
    "Ожидайте позитивный перелом в судьбе, потому как успех с вами. Вас ждут прекрасные новости, но нужно уметь их принимать и оценивать все плюсы от полученного.",
    "Впереди ситуация, которая покажет кто есть кто. Кто Ваш истинный друг, кто Ваш враг. Учитесь прислушиваться к сердцу, сегодня именно оно укажет вам верный путь. ",
    "Труд даст результат, но вознаграждение за него будет маленьким. Посему, Вам стоит поискать дополнительные источники прибыли или удовлетворения в ваших делах.",
    "Сегодня день будет более радужным. Скорей всего вас ожидают позитивные события и встреча со старыми друзьями или приятными людьми. Прислушивайтесь к их словам и постарайтесь увидеть между строк. Возможно ситуация намного глубже, чем кажется на первый взгляд.",
    "Ссора (или неприятность) произошедшая недавно скоро будет позабыта. Старайтесь больше энергии вкладывать в позитив и уделять больше времени себе.",
    "Только кошки знают, как получить пищу без труда, жилище без замка и любовь без треволнений. Последнее – особенно актуально. Будьте гибче и мягче, обходите острые углы. И не заметите, как всё наладится. Сегодняшний день будет несколько тревожным, но только благодаря вашему подходу вы сможете его сгладить.",
    "Какое это огромное счастье любить и быть любимым, и какой ужас чувствовать, что начинаешь сваливаться с этой высокой башни! Береги то, что имеете, иначе Вам придётся очень горько сожалеть о потерянных отношениях. В этот день велика опасность в отношениях(не только со второй половинкой, так же это касается хорошего друга, родственника, знакомого). Будьте аккуратны и не допускайте пренебрежения к ним. Если любите – скажите сразу, а нет, то не скрывайте своего безразличия за милой улыбочкой. Это лицемерие.",
    "Кто-то из великих мира сего заметил: «Чем разводиться, лучше пошли жене дюжину роз. Потрясение ее убьет, а розы ты положишь на гроб». Сделайте то же самое со своими врагами и жалеть Вам не придётся. Сегодня может быть так, что вы получите нежь в спину, но не стоит воспринимать это так остро, знайте себе цену, не устраивайте скандалы и просто примите тот факт, что если один раз предал, велика вероятность, предаст и дважды.",
    "Время проститься со своими страхами, время забыть обиды прошлого, время отпустить всех людей, что давно канули в лету. День для вас ознаменует выбор, вы либо решитесь на что-то важное, либо оставите все как есть, но будет ощущение, что снова пошли по кругу.",
    "Сегодня вы возможно что-то потеряете. Бот предсказатель предостерегает от кражи или потери. Далеко - что пропало, не найдется. Но это повод приобрести новое и порадовать себя.",
    "Сегодняшний день ознаменует победу в делах. Приобретение почестей по заслугам, неожиданная встреча с  человеком, который возвратится из далекого путешествия. ",
    "Задуманное Вами обязательно исполнится. Вам не стоит доверять мнению окружающих Вас людей. Вместо этого – научитесь доверять себе. для того чтобы довериться себе, нужно научиться уважать себя. В некотором смысле, эти прописные истины известны всем и каждому, да только толку от этого мало. Кто-то просто это знает, а кто-то не только знает, но и делает. Слово «делает» - ключевое. Если Вы не уважаете себя, не верите себе, это все очень быстро считается. В результате Вы имеете то, что имеете.",
    "Вам не стоит пренебрегать помощью близких людей, ведь предлагая её, они действуют от чистого сердца. В какой-то момент времени Вам срочно понадобится совет человека мудрого и незаинтересованного, человека, не погружённого в эмоции. Прислушайтесь к тому, что Вам скажет этот человек. ",
    "Сегодняшний день  обещает новые возможности: финансовую стабильность и деловые поездки. Сейчас лучшее время для укрепления имеющихся связей, а также развития новых. Важно трезво оценивать всё новое, входящее в жизнь.",
    "Дела сердечные суеты не терпят, как впрочем, не терпят и «третьих лиц». Данный Сегодняшний день предоставит вам, как начало новых отношений (начало бурного романа), так и «второе рождение» отношений, которые казались исчерпанными. Возможно возвращение старого знакомого, который будет пытаться наладить контакт  и очень сожалеть о том, как он в Вас ошибался. Не стоит верить этим словам. Они лживы.",
    "Впереди травмоопасный период. Сейчас нельзя рисковать. Более того, это касается не только физического здоровья, но и здоровья психического. Нужно исключить возможность перенапряжения, стрессовых ситуаций, диет, больших физических и психоэмоциональных нагрузок. Если таковой возможности нет, то постарайтесь хотя бы высыпаться и медитировать. В противном случае, Вы рискуете расхвораться.",
    "Старая тайна вырвется наружу. Станет известна всем. Данная тайна поможет Вам в решении Ваших дел. Так же, может означать открытый путь, отсутствие препятствий, дорогу, которая будет Вами осилена. Кроме этого, вы получите новые знания, приобретение опыта.",
    "День будет сложным и вы взвалите на себя слишком многое, но как говориться: Не стоит заваривать той каши, которую потом не расхлебаешь. Оценивайте свои силы здраво.",
    "Можно послать и сто стрел, но ни разу ни попасть, а можно пусть всего одну стрелу, которая попадёт в цель. Поменьше суеты. Побольше твёрдости духа. Дела сегодняшнего дня потребуют от вас хорошей самоотдачи.",
    "Много суеты, мало толку. Сейчас не тот период, чтобы тратить время понапрасну. Проанализируйте, что для вас сейчас наиболее важно и правильно расставьте приоритеты.",
    "Отношения, разорванные с близкими Вам людьми, в ближайшее время смогут наладиться. Поскорее забудьте о ссорах и сделайте первый шаг.",
    "Медитируйте, очищайте собственное сознание от всего лишнего, наносного. Духовные практики помогут справиться не только с навалившимися проблемами, но и с недугами, проявляющимися в физическом теле. Бот намекает на более духовный день, если вы пойдете на поводу материальных хотелок, то можете потерпеть неудачу в некоторых делах.",
    "Сегодняшний день будет приятным. Вы углубитесь в свои мечты, но из-за этого можете пропустить что то очень важное. Будьте внимательны и прислушивайтесь к словам ваших близких друзей.",
    "Бот предсказатель советует делать все с полной ответственностью, быть разумно критичным по отношению к себе и своим поступкам и принимать только обдуманные и взвешенные решения. Не забывайте народную мудрость: что посеешь, то и пожнешь. День потребует от вас много сил, но результат будет соответствующим.",
    "Сегодня, вы переживаете переломный момент: проблема, мучившая вас, вот-вот разрешится к вашему облегчению. У  вас есть повод улыбнуться, потому вы по настоящему счастливый человек, просто примите это и начните проецировать на себя чувство радости. Выф богаты, но возможно не осознаете этого. ",
    "Скоро вы получите хорошее известие. Речь может идти о благополучном разрешении давнего спора, портившего ваши отношения с близким человеком, о неожиданном поступлении денежных средств, об исцелении болезни, об открывшейся возможности сделать рывок в карьере или о предложении руки и сердца.",
    "Не ломайте голову над тем, каким образом будет достигнуто желаемое или в какой форме оно проявится. Ответ прост: удача сегодня вам благоволит, будьте проще и больше улыбайтесь, потому что вы прекрасны.",
    """Ожидайте прибыли, прибавления финансов, возможно не очень большое, но приятное событие. 
Будьте благодарны самому себе и не держите обиды в сердце. День благоприятен для новых начинаний, может быть хобби?) """,
    "Марионетки боятся не виселицы, а ножниц. Когда «нити» обрываются, становится страшно: ведь зло может выйти на свободу. Избегайте тех людей, что подходят под данное описание. От них Вы доброго ждать не приходится. Сегодня вы встретитесь с опасностью, и каков итог – будет зависит от вас. Если вы окажетесь достаточно сильны, то для вас опасность будет не страшна."
]
