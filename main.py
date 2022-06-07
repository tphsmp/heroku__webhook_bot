import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = '5306944270:AAFstlblEWr-Reb6V8IgQMXuHObDgKOgg5k'
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    website = types.KeyboardButton('Site')
    start = types.KeyboardButton('Start')
    markup.add(website, start)
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def buttons_actions(message):
    if(message.text == 'Site'):
        bot.send_message(message.chat.id, text="Будь как дома юзер")
        bot.send_message(message.chat.id, message)
    elif (message.text == 'Start'):
        bot.send_message(message.chat.id, text="Порно в интернете коль желаешь покажу")
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
