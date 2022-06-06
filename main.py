import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = '5306944270:AAFstlblEWr-Reb6V8IgQMXuHObDgKOgg5k'
APP_URL = f'https://implebot.herokuapp.com/{TOKEN}'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "Start":
        bot.reply_to(message, 'Привет ' + message.from_user.first_name + ' я онлайн оракул')
        # Готовим кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        website = types.KeyboardButton('одна руна')
        start = types.KeyboardButton('три руны')
        markup.add(website, start)
        bot.send_message(message.chat.id, 'Выбери расклад', reply_markup=markup)

    #else:
        #bot.send_message(message.from_user.id, 'Напиши Start')


@bot.message_handler(content_types=['text'])
def callback_worker(message):
    if message.text == "одна руна":
        bot.send_message(message.chat_id, 'One rune')

    elif message.text == "три руны":
        bot.send_message(message.chat_id, 'Three runes')
        

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


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
