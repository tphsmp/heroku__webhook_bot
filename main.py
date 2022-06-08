import os
from copy import copy

import telebot
from telebot import types
from flask import Flask, request
from runa import Runa
from random import random, choice, randint

TOKEN = '5306944270:AAFstlblEWr-Reb6V8IgQMXuHObDgKOgg5k'
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

# runes = ["Fehu", "Uruz", "Thurisaz", "Ansuz", "Raido", "Kenaz", "Gifu", "Wunjo"]
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
              "", "", "\u16A6")]
newList = []


def ranumber():
    x = randint(1, 24)
    return str(x)


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
        for i in range(3):
            runa = choice(runes)
            runa1 = str(copy(runa))
            runes.remove(runa)
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
