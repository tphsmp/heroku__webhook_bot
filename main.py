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
    if message.text == 'Start':
        bot.reply_to(message, 'Привет ' + message.from_user.first_name)
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик
        key_runeoftheday = types.InlineKeyboardButton(text='Рандомная карта', callback_data='runeoftheday')
        keyboard.add(key_runeoftheday)
        key_threerunes = types.InlineKeyboardButton(text='Три карты', callback_data='threerunes')
        keyboard.add(key_threerunes)
        bot.send_message(message.from_user.id, text='Выбери расклад', reply_markup=keyboard)

    else:
        bot.send_message(message.from_user.id, 'Напиши Start')
    
    
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "runeoftheday":
        bot.send_message(call.message.chat_id, 'One rune')
        bot.send_message(call.chat_id, call)

    elif call.data == "threerunes":
        bot.send_message(call.message.chat_id, 'Three runes')
        bot.send_message(call.chat_id, call)
        

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
