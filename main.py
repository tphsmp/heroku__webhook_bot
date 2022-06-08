import os
import telebot
from telebot import types
from flask import Flask, request
from runa import Runa
from random import random, choice

TOKEN = '5306944270:AAFstlblEWr-Reb6V8IgQMXuHObDgKOgg5k'
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

runes = ["Fehu", "Uruz", "Thurisaz", "Ansuz", "Raido", "Kenaz", "Gifu", "Wunjo"]
newList = []
runa = choice(runes)


def ranumber():
    x = random.randint(1, 24)
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
        bot.send_message(message.chat.id, text="Руня дня " + runa)
    elif (message.text == 'Three_runes'):
        bot.send_message(message.chat.id, text="Три руны " + ranumber())
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
