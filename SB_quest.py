import telebot
import random
from telebot import apihelper
#Сингапурский proxy для работы Бота 
apihelper.proxy = {'https':'https://2.37.211.206:8118'}
#Вызов бота
bot = telebot.TeleBot('927384225:AAGTqnR5FdySLThmeUCnuBR-4MIyfxx5jSQ');

#клавиатура
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/input')

#Прием сообщения
money = 1000000
stamina = 100
ABSfav = 0
progressbar = 0
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ура! Вам предстоит руководить программой по трансфофрмации сети Бета-Банка. Это не простая задача, у вас есть ограниченный бюджет и запас нервных клеток. А еще надо не расстроить Руководство Банка. Поехали?', reply_markup=keyboard1)
    bot.send_message(message.chat.id, 
    'Бюджет:',money,'$'
 	'Энергия:', stamina,
 	'Благосклонность Руководства:', ABSfav,
 	'Вероятность открыть отделение в срок:',progressbar, '%')
@bot.message_handler(commands=['да'])
def start_message(message):
	bot.send_message(message.chat.id, 'Итак, у вас на руках есть концепция отделения будущего и задача открыть отделение нового формата через полгода. Что делаем в первую очередь?')
keyboard1.row('Разрабатываем модель гео-локации. Нужно же знать, где строить!',
	'Выбираем цвет потолка, это крайне важно.')
bot.polling()
print('ok')