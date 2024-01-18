import telebot
from telebot import types
import random
import requests

API_TOKEN = '***'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Функционал')
    button2 = types.KeyboardButton('Случайное число')
    button3 = types.KeyboardButton('Курс $ и € на сегодня')
    button_next = types.KeyboardButton('Далее ->')

    markup.add(button2, button3, button1, button_next)

    bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}, что бы узнать '
                                           '\nфункционал бота, напиши /help', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id, "Бот может выполнить следующие функции: "
                                      "\n1 - отправить случайное число от 0 до 1000 "
                                      "\n2 - отправить актуальный курс доллара / евро "
                                      "\nс сайта ЦБ на сегодня "
                                      "\n3 - отправить мою ссылку на GitHub"
                                      "\n4 - отправить стикер :)")


@bot.message_handler(content_types=['text'])
def bot_message(message):
    global data
    if message.chat.type == 'private':
        if message.text == 'Случайное число':
            bot.send_message(message.chat.id, 'Ваше число: ' + str(random.randint(0, 1000)))
        elif message.text == 'Курс $ и €':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Курс $')
            button2 = types.KeyboardButton('Курс €')
            button_back = types.KeyboardButton('<- Назад')
            markup.add(button1, button2, button_back)

            bot.send_message(message.chat.id, 'Курс $ и €', reply_markup=markup)

        elif message.text == 'Курс $':
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            bot.send_message(message.chat.id, data['Valute']['USD']['Value'])

        elif message.text == 'Курс €':
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            bot.send_message(message.chat.id, data['Valute']['EUR']['Value'])

        elif message.text == 'Далее ->':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Стикер')
            button2 = types.KeyboardButton('О боте')
            button3 = types.KeyboardButton('Мой GitHub')
            button_back = types.KeyboardButton('<- Назад')
            markup.add(button1, button2, button3, button_back)

            bot.send_message(message.chat.id, 'Далее ->', reply_markup=markup)

        elif message.text == '<- Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Функционал')
            button2 = types.KeyboardButton('Случайное число')
            button3 = types.KeyboardButton('Курс $ и €')
            button_next = types.KeyboardButton('Далее ->')

            markup.add(button2, button3, button1, button_next)

            bot.send_message(message.from_user.id, '<- Назад', reply_markup=markup)

        elif message.text == 'Функционал':
            bot.send_message(message.chat.id, 'Бот может выполнить следующие функции: '
                                              "\n1 - отправить случайное число от 0 до 1000 "
                                              "\n2 - отправить актуальный курс доллара / евро "
                                              "\nс сайта ЦБ на сегодня "
                                              "\n3 - отправить мою ссылку на GitHub"
                                              "\n4 - отправить стикер :)")
        elif message.text == 'О боте':
            bot.send_message(message.chat.id, f'Это первый и экспериментальный бот :) '
                                              '\nЛюбой фидбек будет принят во внимание и учтен, ')

        elif message.text == 'Стикер':
            sticker = telebot.types.InputFile('static/sticker.webp')
            bot.send_sticker(message.chat.id, sticker)

        elif message.text == 'Мой GitHub':
            text = '[Мой GitHub](https://github.com/AndreyArte)'
            bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')


bot.polling(none_stop=True)


