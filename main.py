import os
import telebot
import datetime
from telebot import types
from flask import Flask, request
from parse_news import parse



TOKEN = '5188420032:AAHPoq0xXoR9YJgaSi_Q36-KsToaSwnF1f8'
APP_URL = f'https://uanews2022.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
LAST_SEND = datetime.time(0, 00, 00)

#bot

@bot.message_handler(commands=['start', 'help'])
def start(message):
    print("start start func")
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привіт!🇺🇦\n"
                              "Цей бот був створений для отримання актуальної інформації в Україні.\n"
                              "Надішліть:\n"
                              "/news - щоб отримувати актуальні новини.\n"
                              "/stop - щоб зупинити розсилку.\n")
    print("end start func")

@bot.message_handler(commands=['news'])
def send_news(message):
    print("start send_news")
    chat_id = message.chat.id

    SEND = True

    if SEND == True:
        print("Im here 1")
        start_time_data = datetime.datetime.now() + datetime.timedelta(hours=2)
        now_time = start_time_data.time()
        start_time = start_time_data.time()
        zero_time = datetime.time(0, 00, 00)
        hour_time = datetime.time(1, 00, 00)
        if start_time > zero_time and start_time < hour_time:
            start_time = datetime.time(0, 00, 00)
        else:
            start_time = start_time_data - datetime.timedelta(hours=2)
            start_time = start_time.time()

        newss = parse()
        print('news parsed succes')
        for news in newss:
            print("start newss for")
            news_time = datetime.datetime.strptime(news['time'], '%H:%M').time()
            print("======")
            print(start_time)
            print(news_time)
            print(now_time)
            print(news['header'])
            if news_time > start_time and news_time < now_time:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton('Читати', url=news['href'])
                markup.add(item)
                if news['subheader'] != None:
                    title = f" *{news['header']}*\n{news['subheader']}\n*{news['time']}*"
                else:
                    title = f" *{news['header']}*\n*{news['time']}*"
                if news['image'] == None:
                    LAST_SEND = news_time
                    print("send news without image")
                    bot.send_message(chat_id=chat_id,
                                    parse_mode='Markdown',
                                    text=title,
                                    reply_markup=markup,
                                    )
                else:
                    LAST_SEND = news_time
                    print("send news with image")
                    bot.send_photo(chat_id=chat_id,
                                   parse_mode='Markdown',
                                   photo=news['image'],
                                   caption=title,
                                   reply_markup=markup,
                                   )
    print("end for")
    while SEND:
        print('Start while')
        now_time = datetime.datetime.now().time()
        newss = parse()
        for news in newss:
            news_time = datetime.datetime.strptime(news['time'], '%H:%M').time()
            if news_time > LAST_SEND:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton('Читати', url=news['href'])
                markup.add(item)
                if news['subheader'] != None:
                    title = f" *{news['header']}*\n{news['subheader']}\n*{news['time']}*"
                else:
                    title = f" *{news['header']}*\n*{news['time']}*"
                if news['image'] == None:
                    LAST_SEND = news_time
                    bot.send_message(chat_id=chat_id,
                                     caption=title,
                                     reply_markup=markup
                                     )
                else:
                    LAST_SEND = news_time
                    bot.send_photo(chat_id=chat_id,
                                    parse_mode='Markdown',
                                    photo=news['image'],
                                    caption=title,
                                    reply_markup=markup
                                    )
        if SEND == False:
            print("exit from while")
            break

@bot.message_handler(commands=['test'])
def ffff(message):
    print(message.text)




#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo(message):
#    bot.reply_to(message, message.text)

#server

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
    SEND = False
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
