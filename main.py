import os
from copy import copy

import telebot
from telebot import types
from flask import Flask, request
from runa import Runa
from random import random, choice, randint

TOKEN = ''
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


runes = [Runa("Fehu",
              "Сосредоточьте свое внимание на финансовой стороне дела. Не расслабляйтесь по отношению к работе, нельзя парить в облаках, мечтать о не возможном – постарайтесь увеличить или хотя бы сохранить то имущество, которое у Вас реально есть на данный момент. Значение руны Феху (Fehu) в плоскости деловых и партнёрских отношений – укрепляйте нынешние связи, стройте новые, взаимовыгодные взаимоотношения. Трезво смотрите на ситуацию. Преимущества в данный момент на вашей стороне.",
              "Ограничьте расход денежных средств. Берегитесь двояких ситуаций и неясных предложений, готовьтесь к образованию всё новых и новых преград на Вашем пути. Лучше отложить на какое-то время решение важных для Вас проблем. Постарайтесь найти путь из сложившейся ситуации, мысленно оградитесь от неё, отойдите в строну – наверное, на данный момент это лучшее для Вас решение.",
              "", "", "\u16A0"),
         Runa("Uruz",
              "Не упирайтесь переменам и силе, которые вошли в Вашу жизнь, не держитесь за привычное и старое. Примените свои усилия для поддержки и ускорения этих перемен. Может быть, в том числе и Ваши личные отношения станут объектом изменений. Или произойдет переорганизация Вашего дела.",
              "Не упирайтесь переменам и силе, которые вошли в Вашу жизнь, не держитесь за привычное и старое. Примените свои усилия для поддержки и ускорения этих перемен. Может быть, в том числе и Ваши личные отношения станут объектом изменений. Или произойдет переорганизация Вашего дела.",
              "", "", "\u16A2"),
         Runa("Thurusaz",
              "Спешка ни к чему. Ждите размышляя. Это время для переоценки ситуации, а не для действий. Вас ждёт новый путь, после и того и другого.",
              "Не преувеличивайте свою значимость в окружающих Вас процессах и не переусердствуйте с манией величия. Даже в том случае, если Вы обладаете острым умом и правильно разобрались в происходящем, Вы все равно не сможете каким-либо образом повлиять на происходящее. Нет смысла пытаться открыть запертую дверь. Принимая какие-либо решения, не спешите и сначала хорошо все обдумайте, в ином случае Вы создадите много новых проблем, не решив старых.",
              "", "", "\u16A6"),
         Runa("Ansuz",
              " Присмотритесь к себе, может Вы, в последнее время, находитесь в ожидании чего-то хорошего, того, что ждет своего времени, чтобы войти в Вашу жизнь.",
              "Следует перебороть уныние и с ясным разумом исследовать положение. Заметьте, многие совершенные Вами деяния не были мудрыми. И главное, отнеситесь с благодарностью к судьбе, за то, что она предоставила Вам своевременные испытания, с помощью которых Вы можете стать сильнее и что-то понять. Будьте на стороже, к Вам могут прийти советы, от людей которые не могут быть беспристрастными, находятся они возле Вас исключительно ради своей выгоды.",
              "", "", "\u16A8"),
         Runa("Raido",
              " Доверьтесь самому и ходу событий. Не мешкайте, не растрачивайте время на не нужные сомнения и рассуждения, на звуки голосов в Вашем подсознании – просто двигайтесь.",
              "Анализируйте, думайте, наблюдайте, будьте на чеку, готовьтесь приложить усилия, мобилизуйтесь – мир изменился, все завит только от Вашей сообразительности. На Вашем пути встретится что-то хорошее, но, к сожалению, оно не достанется Вам даром, без усилий с Вашей стороны. Если Вы ленитесь и слишком расслабились, то есть риск упустить свою удачу. Постарайтесь устойчиво стоять на ногах.",
              "", "", "\u16B1"),
         Runa("Kenaz",
              " Вам что-то омрачает жизнь, откажитесь от этого. Не нужно жалеть о старом и цепляться за него: оно Вам больше не понадобится в своем теперешнем виде. Покопайтесь в себе, разберитесь, откройте свои чувства и впустите в свою жизнь сияние божественной любви. Отпустите на свободу свои тайные таланты, начинайте действовать. Проникнувшись сиянием, стараясь узнать его природу, есть возможность возобновить разлаженное взаимопонимание с близкими людьми, получить некие новые знания.",
              "Будьте уверены: потерянное Вами отжило положенный ему срок и Вам это больше просто не нужно. Через какое-то время, когда боль поутихнет, Вы это поймете сами. Без сомнений откиньте прошлое и будте готовы пожить с пустотой внутри какое-то время.",
              "", "", "\u16B2"),
         Runa("Gifu", " Вы идете в правильном направлении. Творите и обретете.",
              " Вы идете в правильном направлении. Творите и обретете.", "0", "", "\u16B7"),
         Runa("Wunjo",
              " Откройте двери для радости. Сделайте хорошее дело для людей и для себя, а какое именно, вам подскажет шестое чувство.",
              "Отложите на время принятие важных решений. Старайтесь не впускать в свои мысли сомнения, не допускайте неискренности и особенно лжи в отношениях с людьми. Не переоценивайте глобально окружающих Вас людей и собственные идеалы, не делайте поспешных выводов. Постарайтесь уяснить, что отсутствие света, всего лишь данная Вам возможность видеть в темноте. На это сил у Вас хватит.",
              "", "", "\u16B9"),
         Runa("Hagalaz",
              " Не унывайте. Не важно, что повлияло на эти разрушения – ваши личные действия или внешние факторы – Вы не должны чувствовать себя беспомощным в данной ситуации. Ваша жизненная сила, Ваше упорство и стойкость, поддержит и будет управлять Вами в сложный для вас период, когда Вы будете сомневаться во всем, даже в том, что раньше считали благом. В зависимости от силы разрушения в Вашей жизни, Вам необходим своевременный и больший рост. Эти разрушения могут полностью изменить Вашу жизнь. Всё что не делается, всё к лучшему, ловите удачу за хвост, не робейте, действуйте.",
              " Не унывайте. Не важно, что повлияло на эти разрушения – ваши личные действия или внешние факторы – Вы не должны чувствовать себя беспомощным в данной ситуации. Ваша жизненная сила, Ваше упорство и стойкость, поддержит и будет управлять Вами в сложный для вас период, когда Вы будете сомневаться во всем, даже в том, что раньше считали благом. В зависимости от силы разрушения в Вашей жизни, Вам необходим своевременный и больший рост. Эти разрушения могут полностью изменить Вашу жизнь. Всё что не делается, всё к лучшему, ловите удачу за хвост, не робейте, действуйте.",
              "0", "", "\u16BA"),
         Runa("Nautiz",
              "Не падайте духом! Возьмите се себя в руки, отбросьте отчаяние. Не нойте и не ворчите, не оплакивайте свою судьбу – не всё ещё потеряно. Ждите, проявите самообладание и выдержку.",
              "Поняв, что вы есть источник всего негатива, который вас преследует, перекройте поток негативной энергии, переплюсуйте весь тот минус, который в вас рождается и проецируется в мир. Контролируйте свои эмоции, подчиняйте их спокойному и умиротворенному уму.  Тогда вы выйдете победителем из сложившихся неудач и неприятностей.",
              "0", "", "\u16BE"),
         Runa("Isa",
              " Расслабьтесь и переждите, пока поток льда сам не отступит. Нет смысла суетиться, вокруг Вас бушую силы, которые многократно сильнее Вас, переждите, и в Вашу жизнь снова придет весна. Не затевайте новых дел, отложите свою активность на полку, для осуществления своих планов дождитесь более благоприятного времени. Не добровольное бездействие может привести к депрессии. Ваши дела запутались, некоторые из них кажутся Вам бессмысленными. Не стучите в закрытую дверь, не делайте резких движений. Вам нужно только потерпеть. Нужно просто переждать.",
              " Расслабьтесь и переждите, пока поток льда сам не отступит. Нет смысла суетиться, вокруг Вас бушую силы, которые многократно сильнее Вас, переждите, и в Вашу жизнь снова придет весна. Не затевайте новых дел, отложите свою активность на полку, для осуществления своих планов дождитесь более благоприятного времени. Не добровольное бездействие может привести к депрессии. Ваши дела запутались, некоторые из них кажутся Вам бессмысленными. Не стучите в закрытую дверь, не делайте резких движений. Вам нужно только потерпеть. Нужно просто переждать.",
              "0", "", "\u16C1"),
         Runa("Jera",
              " Вы хорошо поработали, но награда не заставит себя ждать, если бы Вы еще немного поднапряглись. Не время расслабляться, иначе есть риск всё потерять. У Вас хватит сил и возможностей довести это дело до конца.",
              " Вы хорошо поработали, но награда не заставит себя ждать, если бы Вы еще немного поднапряглись. Не время расслабляться, иначе есть риск всё потерять. У Вас хватит сил и возможностей довести это дело до конца.",
              "0", "", "\u16C3"),
         Runa("Eihwaz", " Ваше дело правое, победа за Вами.", " Ваше дело правое, победа за Вами.", "0", "", "\u16C7"),
         Runa("Perthro",
              "Наступил период перемен. Временно станьте объективным и справедливым исследователем. Главное успокоиться и отпустить прошлое. Слушайте своё шесpyfxtybt hey d hfcrkfltтое чувство. И не удивляйтесь открывшимся в Вас переменам.",
              "Постарайтесь жить сегодняшним днём. Не прячьтесь в прошлое, оно Вам не поможет. С настоящим изменится и Ваш новый образ жизни. Расслабьтесь. Зарождение нового мира довольно тонкий процесс, поэтому не следует его торопить, а ещё лучше просто не мешать. Судьба каждого находиться в собственных руках.",
              "", "", "\u16C8"),
         Runa("Algiz",
              "Не забывайте, что на резких поворотах судьбы нужно быть осторожным, это и будет Вашей защитой. Главное не поддаваться чувствам и прийти к единственно правильному решению, сохраняя при этом трезвость ума и открытость взгляда.",
              "Осторожничайте и будьте на чеку, пристально следите за происходящим внутри Вас и вокруг Вас – гибкость потребуется везде. Остановитесь, отойдите в тень. Главное не идти на таран. Обстоятельства Вам не помогут. Единственный выход из положения это научится приспосабливаться к происходящим событиям.",
              "", "", "\u16C9"),
         Runa("Siegel", " Не бойтесь мечтать, мечты могут воплотиться в реальность.",
              " Не бойтесь мечтать, мечты могут воплотиться в реальность.", "0", "", "\u16CB"),
         Runa("Tyr",
              "Будьте настойчивыми и целеустремленными. Фортуна на Вашей стороне. Иногда может подействовать даже “лобовая атака”. В разных случаях используются разные тактики, когда крепость берут измором, когда штурмом. Сейчас как раз время для штурма. Но помните, терпение – один из вариантов настойчивости.",
              "Не опускайте рук и займитесь собой. Это не черная полоса в Вашей жизни, но время искать ответы внутри себя, решать внутренние проблемы. Старайтесь не время для борьбы с мифическими ветряными мельницами, то есть не время борьбы с неприятными людьми и негативными обстоятельствами, Вы просто зря потеряете энергию.",
              "", "", "\u16CF"),
         Runa("Berkana",
              "Если что-то делаете, делайте это наилучшим образом, либо не беритесь за это дело совсем. Для роста необходим глубокий и ясный взгляд на происходящее вокруг. Проявите терпение и настойчивость, старые повадки не проходят сами собой. Делите главную цель на много мелких, реально выполнимых задач, беритесь сперва за легко выполнимые дела, и постепенно переходите к выполнению все более трудных задач. Не особо расслабляйтесь и верьте, что Вы все сможете.",
              "Что-то мешает Вам поймать удачу за хвост. Препятствовать Вам могут внешние не подвластные Вам силы или же особенности Вашего характера. ",
              "", "", "\u16D2"),
         Runa("Ehwaz",
              "Меняйтесь сами. У вас все получится. Переменам должны произойти и в Ваших отношения с окружающими и с Вашим образом жизни. Только после этого у Вас могут, наступит и внешние перемены.",
              "Избегайте конфликтных ситуаций и не нужных ссор, не рискуйте понапрасну, потерпите и дождитесь созревания ситуации. Попробуйте развеяться. Не огорчайтесь, если все происходит не стой скоростью, которую Вы ожидали.",
              "", "", "\u16D6"),
         Runa("Mannaz",
              "Старайтесь познать и изменить свое внутреннее “Я”. Данный период позитивен для медленного, продуманного самосовершенствования – все это вернется Вас стократ.",
              "Постарайтесь быть непредвзятыми и честными по отношению к собственному Я", "", "", "\u16D7"),
         Runa("Laguz",
              "Представьте, что вы несетесь по течению, доверьтесь волнам, расслабьтесь, постарайтесь почувствовать себя в безопасности. В данный момент не время для обдумывания и осмысления. Не время для усомнения в своих способностях, направьте их в правильное русло. Потерпите, и Ваши опасения испарятся как роса на солнце.",
              "Похоже, Вас затянуло болото. Постарайтесь держать себя в руках: Вы на грани нервного срыва.", "", "",
              "\u16DA"),
         Runa("Ingwaz",
              "Смело расставайтесь со старыми привычками и вещами, оглянитесь, окружающий вас мир преображается. Если вы находитесь на раздорожье – попытайтесь определиться и найти свойпуть. Нужно отбросить всё былое и стремиться к новому. Руна предпологает лёгкое разрешение проблем. Совет руны. Приближается удачный для вас период, используйте его с максимальной эффективностью. Сосредоточтесь на завершении начатых ранее дел. Текущие дела обречены на успешное решение.",
              "Смело расставайтесь со старыми привычками и вещами, оглянитесь, окружающий вас мир преображается. Если вы находитесь на раздорожье – попытайтесь определиться и найти свойпуть. Нужно отбросить всё былое и стремиться к новому. Руна предпологает лёгкое разрешение проблем. Совет руны. Приближается удачный для вас период, используйте его с максимальной эффективностью. Сосредоточтесь на завершении начатых ранее дел. Текущие дела обречены на успешное решение.",
              "0", "", "\u16DD"),
         Runa("Dagaz",
              "Не надо ничего бояться, вас ждут положительные изменения. Действуя, верьте в себя и в победу, в независимости от посторонних обстоятельств. Не зацикливайтесь на своих проблемах, скорее всего вы преувеличиваете их масштабы.",
              "Не надо ничего бояться, вас ждут положительные изменения. Действуя, верьте в себя и в победу, в независимости от посторонних обстоятельств. Не зацикливайтесь на своих проблемах, скорее всего вы преувеличиваете их масштабы.",
              "0", "", "\u16DE"),
         Runa("Othel",
              " Будьте готовы к неожиданным материальным доходам. Это может наложить на Вас немалую ответственность.",
              "  Вы на чужом поле. Действуйте так, как Вам кажется правильным на данный момент времени. Если Вы встретитесь с убытком – не расстраивайтесь: сегодня потеряли, завтра найдете больше потерянного.",
              "", "", "\u16DF"),
         Runa("Wyrd", "Следует довериться воле богов и их мудрости. Пусть ситуация развивается сама собой",
              "Следует довериться воле богов и их мудрости. Пусть ситуация развивается сама собой", "0", "", "\u25CB")]


@bot.message_handler(commands=['start'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    onerune = types.KeyboardButton('One_rune')
    threerunes = types.KeyboardButton('Three_runes')
    markup.add(onerune, threerunes)
    bot.send_message(message.chat.id, 'Выбери расклад', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons_actions(message):
    if (message.text == 'One_rune'):
        runa = str(choice(runes))
        bot.send_message(message.chat.id, runa)
    elif (message.text == 'Three_runes'):
        newList = runes.copy()
        for i in range(3):
            runa = choice(newList)
            runa1 = str(runa)
            newList.remove(runa)
            bot.send_message(message.chat.id, runa1)
    else:
        pass

@server.route('/' + TOKEN, methods=['POST', 'GET'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
