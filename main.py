import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = '5306944270:AAFstlblEWr-Reb6V8IgQMXuHObDgKOgg5k'
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Одна руна"))
    bot.send_message(message.chat_id, "One rune", reply_markup=markup)
        

@server.route('/' + TOKEN, methods=['POST'])
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
