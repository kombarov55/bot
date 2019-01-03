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
    return date.year * 365 + date.month * 30 + date.day

userIdToPredictionIndex = {}
userIdToUpdateTime = {}

predictions = [ 
"День пройдет легко, вдохновенной, возможно вы получите подарок, удачное стечение обстоятельств, что заставит вас улыбнуться, но в силу своего характера вы его можете пропустить и попросту не увидев из-за своей гордости и предубеждений. Будьте открыты миру и он найдет чем вас порадовать!", 
"Дела тяжелым грузом будут тяготить ваше сердце, в конечном итоге вы со всем разберетесь, но чувствовать при этом себя как выжатый лимон. День сулит мелкие приобретения, что-то незначительное но приятное. Покупка или вдруг найденная дома вещь, которую долго искали вам поднимет настроение.", 
"Вы будете чувствовать себя скованно и зажато под грузом обязательств. Окружающая суматоха и мандраж будут выбивать вас из равновесия и рассеивать внимание на несущественные вещи, отвлекая от главного. Будьте бдительны, ваши недоброжелатели не дремлют!", 
"День пройдет уверенно и качественно. Вы чувствуете себя человеком – свергающим наповал горы и раздвигающим облака. Одним словом, вы на коне и у вас все получится. День так же предвещает небольшие плотские искушения, которые принесут удовольствие и добавят пикантности в ваше настроение.", 
"Вы будете заняты работой, планами, усердно трудясь на благо себя или компании. Результат будет удовлетворительным, не ждите от себя и других чего-то сверх меры. Вы получите ровно столько – сколько заслужили и наработали.", 
"Вы рискуете увязнуть в своих иллюзиях и сомнениях. Вас со всех сторон будут одолевать не самые приятные события, пытающиеся сбить с толку и ослабить. Держитесь. Совет дня: не терять боевой настрой и сконцентрироваться на том, что для вас действительно важно. Можно даже выписать на бумажку по пунктам, для наглядности.", 
"В этот день велика вероятность встретить нового или давно забытого человека. Встреча предвещает беду, потери и глубокое сожаление. Вас предадут и самым некрасивым образом кинут. Не делите судьбу старухи с разбитым корытом, меньше трясите языком и больше анализируйте поведение ваших собеседников, что бы не поддаться на провокации.", 
"День будет легким, воздушным, но вы при этом твердо держитесь и без трудностей исполняете все задуманное. Оно конечно идет не очень стабильно, но в любом случае возымеет благополучный исход. Помните о родственниках, они могут вас поддержать и подсказать дельный совет.", 
"День пройдет довольно пресно. Давнее дело с договорами, сделками и административной сферой наконец закончится раз и навсегда. Проблема решена, какой бы она не была, но ее исход может быть несколько скоропалительным и невыгодным лично для вас. Имейте уважение к себе не прогибаться под обстоятельства и людей, которые не стоят вашего времени.", 
" Вы будете в унынии и некой апатии из-за прошедших событий. Да, они сделали вам больно и ослабили, но черт побери, нужно собраться и утереть сопли. У вас есть все силы на это, а ближе к вечеру вам поднимут настроение приятным бонусом.", 
" День пройдет, как на иглах. Вы в обороне и ваша паранойя окажется неплохой интуицией, а именно – вы окажетесь готовы к негативным факторам и уверен им сможете противостоять, невзирая на их действие. День предвещает оборону и уверенность.", 
" Вас навестит семья! Возможно не физически, а по какой либо связи, это доставит вам хлопот и вынудит скорректировать планы, но при этом убережет от некоторых негативных факторов. Вспомните свои истинные корни и не забывайте место, где были рождены.", 
" День пройдет нестабильно. Вас буквально свяжут по рукам и ногам материальные заботы связанные с финансовой сферой, но в первую очередь стоит открыть глаза и думать шире. Деньги – это конечно хорошо, но не бойтесь с ними расстаться. То, что вы потеряете, вернется потом и умножится.", 
" В этот день вы наконец придете к некоторому заключению по прошедшим событиям и вынесете вердикт, который скажется позитивно и даст больше уверенности в будущем. Вы вновь на позиции ведущего, которая потребует от вас ответственности и глубокого сосредоточения на действиях, иначе вы рискуете подвести тех, кто будет под вашим началом.", 
" День начнется с хорошего настроения, всепонимания, всепрощения и вхождения в положение других людей, но….  Увы, это скажется негативно на вашем положении и состоянии. Вы плюнете на ваши добрые и бескорыстные порывы и обрежете контакт с теми, кто вас пытался использовать. К слову, не стоит изначально завышать планку, меньше разочарований в людях и их намерениях.", 
" День предвещает освобождение от некой коварной ситуации и приход к более-менее стабильному положению. Вы будете чувствовать прилив сил и уверенность в себе, но не слишком злоупотребляйте мнимым проблеском радуги в вашей жизни. Примените всю приобретенную энергию с пользой и результат окажется гораздо лучше, чем изначально ожидали.", 
" День – праздник, вы получите массу удовольствия и веселья + небольшой подарок, который растрогает сердце и порадует. Ваш день будет очень удачным и вы испытаете довольство. День так же повлияет на следующее утро, но вы испытаете нечто «похмельное», после разгульного кутежа.", 
" У вас будет множество дел и планов, которые потребуют хорошего терпения, усидчивости и сил, вложенных в качественную работу. Вы будете стараться доделать все «хвосты» и одновременно продолжать работать над уже имеющимся стабильным делом, которое вам приносит доход.", 
" Вы в боевом настрое и будете переть на проблемы, как таран, что не очень благотворно скажется на ваших делах. Как говорится – за двумя зайцами погонишься …    Сконцентрируйте внимание на более важных вещах и выполняете их в первую очередь, иначе рискуете под вечер остаться с носом по каждому пункту.", 
" Этот день предоставит вам выбор между борьбой, делами важными лично для вас и семьей, которая попытается забрать у вас все время, которое вы рассчитывали уделить делам. Перед тем, как принять решение, спросите у самого себя – что вам важнее.", 
" Обязанности и дела будут наваливаться на вас кучей и все надо решить, сделать, реализовать. Под конец дня вы рискуете свалиться и тяжело дыша пыхтеть, восстанавливая силы, которые на протяжении дня их вас активно пили.", 
" Ваши дела будут идти легко, но непредсказуемо и все исключительно из-за халатности, лени и желания сделать все быстро. Не думайте, что за это останетесь безнаказанным, волшебный пинок прилетит из самого необычного места.", 
" Множество дел, которыми вы будете окружены со всех сторон принесут вам удовольствие от процесса выполнения и удовлетворение результатами. Вы так же будете довольны собой, за то, что такой молодец и все решили быстро.", 
" День будет удачным и плодотворным, многое как всегда поймете и заранее будете готовы. Вам придется столкнуться с некими семейными моментами (не факт, что дело касается конкретно семьи в обычном понимании этого слова, потому как семьей может быть группа близких по духу людей). Доверяйте своей интуиции.", 
" День пройдет замечательно, вы получите некую плюшку, которая очень пригодится в будущем. Полнота, радость, довольство и гармония с самим собой – вот, что вас ждет, а еще возможность выделиться, стать полезным важным для вас людям.", 
" В этот День вы крепко держитесь за протянутую руку помощи, которую вам несомненно кто-то окажет, но будьте крайне осторожны, ибо оказавший помощь имеет корыстные мотивы и с вас потом 3 шкуры сдерет, требуя вернуть долг. Не злоупотребляете помощью со стороны, даже если кажется, что  сами не справитесь. Доверяйте только проверенным друзьям.", 
" Вам окажут существенную помощь им поддержку, выступят в роли благодеятеля, желающего добра. Не бойтесь довериться человеку и разделить ваши чувства и проблемы с ним. Он (или она) поможет вам преодолеть трудности и скрасит день своим присутствием.", 
" День пройдет уверенно и стабильно. Вы будете несколько увлечены заинтересовавшим вас вопросом, что позволит несколько отвлечься от дел, но это не возымеет негативного действа, а просто позволит переключиться. Не отказывайте себе в удовольствии узнать что-то новое и выйти из привычных рамок.", 
" Боль, обида и грусть не длятся вечность, помните о том, что все когда ни будь заканчивается и негатив в вашей жизни так же пройдет. Будьте более пламными, гибкими, как вода и спокойно относитесь к сложившейся ситуации. Если кажется, что очень тяжело – обратитесь за помощью к психологу или доверенному человеку.", 
" В этот день кардинально поменяется ваша жизнь и скорей всего это изменение необратимо. Относитесь более позитивно к тому, что с  вами случиться и помните – Душа бессмертна и требует духовного развития.", 
" Вас ждет активное сражение и неоднозначная победа. Атака и оборона заберет много сил, но помните – в любом бою нужно прежде всего думать головой, а не действовать с позиции грубой силы.", 
" Вы поменяете свое мышление и будете пытаться насиловать сознание ненужными догмами, иллюзиями и правилами, что скажется негативно на вас самих. Попытки «выйти за грань» обернуться утратой и потерей энергии, которая могла преобразоваться во что-то полезное. Не стоит увлекаться тем, что ты не понимаешь, иногда в мутной реке попадаются битые стекла и ржавые гвозди. Ваши ресурсы информации не проверенны.", 
"  День вы активно потратите на борьбу со своими иллюзиями. Противостоите так же обману и накручиванию ложной информации, одним словом – день пройдет в поиске истины. Ваша удача зависит от потраченных усилий, не бойтесь нестандартных подходов и избирательности в методах.", 
" День пройдет хорошо, но сперва вы будете держаться особняком с подростковыми замашками максимализма, при этом не заметите, что делают для вас близкие люди, предпочитая все мерить одной палкой и поспешно делать выводы. Ничего опасного или плохого не случится, кроме малых каверз, которые вы сперва примите за что-то серьезное.", 
" День будет проведен в расслаблении, дела завершатся естественно и без натуги. Вы займетесь отдыхом и восполнением сил, отлынивая от работы. Но за это вас скорей всего осудят и вынесут вердикт о вашей пригодности (не очень хороший). Если отношения с начальством нормальные, то вам нечего бояться, кроме небольшой выволочки.", 
" Ваши приобретения и вложения принесут разочарование и потери. Желание быстро получить выгоду обернется неоправданными ожиданиями и придется приложить все силы, что бы вернуть хотя бы часть из того, что утратили. Больше позитива и уверенности, жизнь длинная и при должном старании вы сумеете наверстать упущенное.", 
" День пойдет на артистичной ноте, доля игривого настроении и легкости при этом будет сопровождать внутренняя уверенность в себе. Ваши решения окажутся верными, принесут выгоду и довольство собой. Не смейте в себе сомневаться, блистайте и покажите всю многогранность вашей сути.", 
" День принесет вам небольшую прибыль за малым усилием. Какие-то мелкие дела и проекты разродятся прибылью, которая не заставит себя ждать.", 
"Вы наплюете на мнение абсолютно всех людей, кроме одного из вашего окружения. Перестанете слышать даже голос собственного разума, а тот человек, которому безоговорочно принадлежит ваше внимание – пленит вас своими песнями и полностью ведет, как ему заблагорассудится.", 
" День будет связан с судебными разбирательствами или чем-то связанным с договорами, сделками, бумагами. Вы наконец освободитесь от этой волокиты и сможете вздохнуть свободней, когда последняя страничка подпишется и печать проставится. НО –– читайте мелкий шрифт, а то рискуете вляпаться в авантюру.", 
" День предвещает приятную встречу, с последующим времяпровождением вместе. Вы будете довольны, удовлетворены и счастливы от компании. Вас жизненный тонус поднимется и фонтанчик радости проснется в груди.", 
" День будет нести обучение и познание. Вы углубитесь в нечто духовное и это заставит вас задуматься над собственной жизнью. Но старайтесь избегать непроверенной информации и сектанских течений.", 
" Будет много дел, которые нужно успеть решить до конечного срока, который уже поджимает, но в итоге вы все успеете вовремя (впритык) и получите удовольствие от результата + хороший стимул продолжать дальше.", 
" На вас лежит ответственность и обязанности, но будет искушение профилонить и свалить часть дел на других. Вы либо сделаете все сами, под «руководством» со стороны, либо специально будете ошибаться и это «руководство» будет вынуждено за вас делать работу. Эта скажется на отношениях.", 
" День будет посвящен построению планов и схем для дальнейшего пути. Вы будете уверенны в себе, дальновидны и прагматичны, но при всем при этом, не мешает больше определенности и точности в действиях. Вам нужно заложить крепкий фундамент, иметь опору для дальнейшего движения.", 
" Нежность, мягкость, женственность – сегодня это не про вас. Уверенность конечно будет преобладать, но больше по части силовых методов и «горячих» решений. Вы рветесь в бой, поступки продуманы, но без ложной нежности или пощады. Не расслабляйтесь, вы на верном пути.", 
" Ваш день – это борьба с обстоятельствами, которые мешаю на пути к достижению цели и усилия будут оправданы (риск тоже). Вам будут вставлять палки в колеса, мешать, сбивать с цели и всячески препятствовать, но если будете упорно двигаться вперед – то обязательно преодолеете все трудности.", 
" День – когда вы уйдете от материальных благ и жажды наживы, к более духовному, осознанному и прекрасному. Поиск самого себя, раскрытие и познание вот, как вы проведете день, но не увлекайтесь и помните, что во всем нужна мера.", 
" День пойдет в обучении и стремлении саморазвиваться. Обучение и отшлифовка навыков дадут вам надежный толчок для будущего пути. Не думайте о материальной выгоде, вкладывайте время, деньги, силы в самого себя и не прогадаете.", 
" Результат затраченных действий принесет свои плоды. Вы крепко держитесь за свои убеждения, но помните, что гибкость и широта мыслей прекрасно дополнят ваш нынешний образ жизни, да и к тому же принесут куда больше, чем заскорузлые догмы из прошлого.", 
" Если вы измените самому себе, то это приведет к неоправданному риску, потерям и душевной боли. Помните и ставьте на первое место себя, чутко относитесь к своим чувствам и не за какие коврижки не соглашайтесь ломать себя в угоду других. Они этого не стоят.", 
" Болезнь, ослабленное состояние наконец будут вас покидать. Силы вернуться и энтузиазм возрастет, подталкиваемый работой.   Уделите больше внимания домашнему труду и приведите в порядок ваше жилище.", 
" Вы откажетесь от некоторых полюшек, предложений и работы, которую будут предлагать вам люди. Они будут пытаться давить на вас, склонять на свою сторону не чураясь любых методов, но вы останетесь непоколебимы и твердолобы.", 
" Разбитое сердце, одиночество, страдание.. вы серьезно?  Забудьте о том, что вас кто-то там обидел, не оправдал надежд, жизнь на этом не заканчивается, нужно двигаться вперед. Проблемы, которые на вас навалятся только сейчас кажутся очень плохими, а на самом деле они такие же, как у остальных и легко решаются путем вытирания своих соплей и уверенного подхода.", 
" Вы будете тунеядствовать и пространно смотреть на вещи. Легкая апатия и тоска попытаются забрать вас в свои глубины, но в конце дня вы взбодритесь и мысли станут более упорядоченными.", 
" Погоня за материальными благами окажется хлопотной, заставит потратить много сил на поиски решений, где бы добыть больше ресурсов. Это заставит вас побегать и весь день напряженно работать.", 
" Вы слишком прямолинейны и многое будет улет из под вашего языка. Поток невысказанного, чувств и ощущений. Вы упиваетесь тем, что вроде бы сильный человек и не нужно вам никакой близости, единения душ, но на самом деле очень хотите такого человека, которому можно целиком и полностью довериться. Расслабиться с ним и быть полностью открытым.", 
" День будет особенным. Вы щедры, поможете другим и окажете поддержку. Возможно выступите в роли жилетки или столба, на который можно опереться. Получите удовольствие от того, что кому-то пригодились, но пользы не поимеете.", 
" Вас ждет путешествие, которое принесет много новых открытий, уверенное движение окажется удачным и нагонит ностальгию  по приятному прошлому. Будьте внимательны на дорогах.", 
" Силы Тьмы благоволят вам, помогут в делах и планах, поддержат и обезопасят от неприятных событий, но так же помните – нужно и самому постараться, что бы добиться наилучшего результата. " ]



# predictions = [
#     "Сегодня вы испытаете ожидаемое удивление и вспомните старых знакомых. Помимо этого, возможно впадение в легкую ностальгию, но не увлекайтесь, так как у вас найдутся более важные и интересные дела.",
#     "Ваш день будет насыщенным, но зависит это только от того, решитесь ли вы преодолеть свой страх и узнать что-то новое. Не отчаивайтесь, если что-то не получится с первого раза.",
#     "Сегодняшний день будет благополучен в творческой сфере, если вы уделите больше внимания себе и своим эмоциям, не будете их зажимать, то почувствуете очень приятное облегчение. У вас будет шанс решить, либо дать себе свободу, либо продолжить корчить приличного и спокойного человека.",
#     "День будет спокойным и вы будете удовлетворены результатами. Но пожалуй, завышенные ожидания окажутся несколько неприятными, потому что будет ощущения легкого разочарования, если вы будете слишком требовательны.",
#     "Сегодня вы должны блистать, поверьте в свою силу и много добьетесь. Не советую слушать других людей, их претензии могут быть либо из зависти, либо от личного настроения.",
#     "Сегодня уделите больше времени работе и завершению дел. В конце вечера возможен приятный бонус и конечно же удовлетворение от оконченной работы. В случае лентяйства, вас будет ожидать досада.",
#     "Сегодняшний день благоприятен для более магического образа жизни, позвольте себе немного помедитировать на воду, успокоить нервы. Вы будете гораздо лучше себя чувствовать после этого.",
#     "Сегодняшний день пройдет сумбурно, многое может выходить из под контроля и очень советую вам держать себя в руках. Следите за тем, что говорите, многих вы можете неосознанно обидеть неосторожным словом.",
#     "Сегодняшний день может оказаться сложным, так что с самого начала дня настройтесь на позитивное настроение и что бы не случилось, держитесь. Вы сильный человек, поверьте в это и сможете преодолеть практически все!",
#     "Бот предсказатель настоятельно рекомендует, чтобы вы выбирали для себя дорогу, работу или отношения, только следуя велениям сердца и непременно добровольно. От этого сегодня зависит ваше будущее счастье.",
#     "Сегодняшний день  ознаменует для вас выбор. Советую вам больше не колебаться и не медлить, ожидая доступа к дополнительной информации, а вместо этого, не теряя времени, начинать действовать и претворять в жизнь свои планы.",
#     "Ожидайте позитивный перелом в судьбе, потому как успех с вами. Вас ждут прекрасные новости, но нужно уметь их принимать и оценивать все плюсы от полученного.",
#     "Впереди ситуация, которая покажет кто есть кто. Кто Ваш истинный друг, кто Ваш враг. Учитесь прислушиваться к сердцу, сегодня именно оно укажет вам верный путь. ",
#     "Труд даст результат, но вознаграждение за него будет маленьким. Посему, Вам стоит поискать дополнительные источники прибыли или удовлетворения в ваших делах.",
#     "Сегодня день будет более радужным. Скорей всего вас ожидают позитивные события и встреча со старыми друзьями или приятными людьми. Прислушивайтесь к их словам и постарайтесь увидеть между строк. Возможно ситуация намного глубже, чем кажется на первый взгляд.",
#     "Ссора (или неприятность) произошедшая недавно скоро будет позабыта. Старайтесь больше энергии вкладывать в позитив и уделять больше времени себе.",
#     "Только кошки знают, как получить пищу без труда, жилище без замка и любовь без треволнений. Последнее – особенно актуально. Будьте гибче и мягче, обходите острые углы. И не заметите, как всё наладится. Сегодняшний день будет несколько тревожным, но только благодаря вашему подходу вы сможете его сгладить.",
#     "Какое это огромное счастье любить и быть любимым, и какой ужас чувствовать, что начинаешь сваливаться с этой высокой башни! Береги то, что имеете, иначе Вам придётся очень горько сожалеть о потерянных отношениях. В этот день велика опасность в отношениях(не только со второй половинкой, так же это касается хорошего друга, родственника, знакомого). Будьте аккуратны и не допускайте пренебрежения к ним. Если любите – скажите сразу, а нет, то не скрывайте своего безразличия за милой улыбочкой. Это лицемерие.",
#     "Кто-то из великих мира сего заметил: «Чем разводиться, лучше пошли жене дюжину роз. Потрясение ее убьет, а розы ты положишь на гроб». Сделайте то же самое со своими врагами и жалеть Вам не придётся. Сегодня может быть так, что вы получите нежь в спину, но не стоит воспринимать это так остро, знайте себе цену, не устраивайте скандалы и просто примите тот факт, что если один раз предал, велика вероятность, предаст и дважды.",
#     "Время проститься со своими страхами, время забыть обиды прошлого, время отпустить всех людей, что давно канули в лету. День для вас ознаменует выбор, вы либо решитесь на что-то важное, либо оставите все как есть, но будет ощущение, что снова пошли по кругу.",
#     "Сегодня вы возможно что-то потеряете. Бот предсказатель предостерегает от кражи или потери. Далеко - что пропало, не найдется. Но это повод приобрести новое и порадовать себя.",
#     "Сегодняшний день ознаменует победу в делах. Приобретение почестей по заслугам, неожиданная встреча с  человеком, который возвратится из далекого путешествия. ",
#     "Задуманное Вами обязательно исполнится. Вам не стоит доверять мнению окружающих Вас людей. Вместо этого – научитесь доверять себе. для того чтобы довериться себе, нужно научиться уважать себя. В некотором смысле, эти прописные истины известны всем и каждому, да только толку от этого мало. Кто-то просто это знает, а кто-то не только знает, но и делает. Слово «делает» - ключевое. Если Вы не уважаете себя, не верите себе, это все очень быстро считается. В результате Вы имеете то, что имеете.",
#     "Вам не стоит пренебрегать помощью близких людей, ведь предлагая её, они действуют от чистого сердца. В какой-то момент времени Вам срочно понадобится совет человека мудрого и незаинтересованного, человека, не погружённого в эмоции. Прислушайтесь к тому, что Вам скажет этот человек. ",
#     "Сегодняшний день  обещает новые возможности: финансовую стабильность и деловые поездки. Сейчас лучшее время для укрепления имеющихся связей, а также развития новых. Важно трезво оценивать всё новое, входящее в жизнь.",
#     "Дела сердечные суеты не терпят, как впрочем, не терпят и «третьих лиц». Данный Сегодняшний день предоставит вам, как начало новых отношений (начало бурного романа), так и «второе рождение» отношений, которые казались исчерпанными. Возможно возвращение старого знакомого, который будет пытаться наладить контакт  и очень сожалеть о том, как он в Вас ошибался. Не стоит верить этим словам. Они лживы.",
#     "Впереди травмоопасный период. Сейчас нельзя рисковать. Более того, это касается не только физического здоровья, но и здоровья психического. Нужно исключить возможность перенапряжения, стрессовых ситуаций, диет, больших физических и психоэмоциональных нагрузок. Если таковой возможности нет, то постарайтесь хотя бы высыпаться и медитировать. В противном случае, Вы рискуете расхвораться.",
#     "Старая тайна вырвется наружу. Станет известна всем. Данная тайна поможет Вам в решении Ваших дел. Так же, может означать открытый путь, отсутствие препятствий, дорогу, которая будет Вами осилена. Кроме этого, вы получите новые знания, приобретение опыта.",
#     "День будет сложным и вы взвалите на себя слишком многое, но как говориться: Не стоит заваривать той каши, которую потом не расхлебаешь. Оценивайте свои силы здраво.",
#     "Можно послать и сто стрел, но ни разу ни попасть, а можно пусть всего одну стрелу, которая попадёт в цель. Поменьше суеты. Побольше твёрдости духа. Дела сегодняшнего дня потребуют от вас хорошей самоотдачи.",
#     "Много суеты, мало толку. Сейчас не тот период, чтобы тратить время понапрасну. Проанализируйте, что для вас сейчас наиболее важно и правильно расставьте приоритеты.",
#     "Отношения, разорванные с близкими Вам людьми, в ближайшее время смогут наладиться. Поскорее забудьте о ссорах и сделайте первый шаг.",
#     "Медитируйте, очищайте собственное сознание от всего лишнего, наносного. Духовные практики помогут справиться не только с навалившимися проблемами, но и с недугами, проявляющимися в физическом теле. Бот намекает на более духовный день, если вы пойдете на поводу материальных хотелок, то можете потерпеть неудачу в некоторых делах.",
#     "Сегодняшний день будет приятным. Вы углубитесь в свои мечты, но из-за этого можете пропустить что то очень важное. Будьте внимательны и прислушивайтесь к словам ваших близких друзей.",
#     "Бот предсказатель советует делать все с полной ответственностью, быть разумно критичным по отношению к себе и своим поступкам и принимать только обдуманные и взвешенные решения. Не забывайте народную мудрость: что посеешь, то и пожнешь. День потребует от вас много сил, но результат будет соответствующим.",
#     "Сегодня, вы переживаете переломный момент: проблема, мучившая вас, вот-вот разрешится к вашему облегчению. У  вас есть повод улыбнуться, потому вы по настоящему счастливый человек, просто примите это и начните проецировать на себя чувство радости. Выф богаты, но возможно не осознаете этого. ",
#     "Скоро вы получите хорошее известие. Речь может идти о благополучном разрешении давнего спора, портившего ваши отношения с близким человеком, о неожиданном поступлении денежных средств, об исцелении болезни, об открывшейся возможности сделать рывок в карьере или о предложении руки и сердца.",
#     "Не ломайте голову над тем, каким образом будет достигнуто желаемое или в какой форме оно проявится. Ответ прост: удача сегодня вам благоволит, будьте проще и больше улыбайтесь, потому что вы прекрасны.",
#     """Ожидайте прибыли, прибавления финансов, возможно не очень большое, но приятное событие. 
# Будьте благодарны самому себе и не держите обиды в сердце. День благоприятен для новых начинаний, может быть хобби?) """,
#     "Марионетки боятся не виселицы, а ножниц. Когда «нити» обрываются, становится страшно: ведь зло может выйти на свободу. Избегайте тех людей, что подходят под данное описание. От них Вы доброго ждать не приходится. Сегодня вы встретитесь с опасностью, и каков итог – будет зависит от вас. Если вы окажетесь достаточно сильны, то для вас опасность будет не страшна."
# ]
