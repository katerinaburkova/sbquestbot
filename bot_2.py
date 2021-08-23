#dost_setup.py
#импорт пакетов
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import telebot
import random
from telebot import apihelper
import pickle 
from datetime import datetime
import pandas as pd
from datetime import date, timedelta
print('v2.1')
#прокси
#apihelper.proxy = {'https': 'socks5://feUCSf:fcVcSj@138.59.204.151:9359'}
import requests
session = requests.Session()
session.verify = False
#импорт словарного запаса бота
f = open('comments_list.txt', 'r') 
comments_list = f.read().split('\n')
f = open('scope_list.txt', 'r') 
scope_list = f.read().split('\n')
f = open('content_list.txt', 'r') 
content_list = f.read().split('\n')
f = open('random_shit_list.txt', 'r') 
rs_list = f.read().split('\n')
f = open('addition.txt', 'r') 
add_list = f.read().split('\n')
f = open('personal_rs.txt', 'r') 
prs_list = f.read().split('\n')
f = open('reaction_triggers.txt', 'r') 
triggers = f.read().split('\n')
f = open('reaction_triggers_pb.txt', 'r') 
triggers_pb = f.read().split('\n')
f = open('reaction_list.txt', 'r') 
reac_list = f.read().split('\n')
reaction =[]
for i in range (0, len(reac_list)-1):
	reaction.append(reac_list[i].split('/'))
#формат для записи данных
#hist= pd.DataFrame(columns=['chat','name','message','timestamp','date','hour', 'min'])
hist=list()
hist.append([0,0,0,0,0,0,0]) 
#запуск бота
bot = telebot.TeleBot('1030051620:AAGtlWX2jxhKnLLmaOKy5NpJOefU7BMgRaw');
#клавиатуры
keyboard_basic = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard_basic.row('тимбарометр 🌡','комментарий к документу 📄', 'обсудить скоуп 🌚','поговорить за контент 💩')
#старт бота
@bot.message_handler(commands=['start'])
def send_hello(message):
	bot.send_message(message.chat.id, 'Команда, привет!',reply_markup=keyboard_basic)

#базовые ответы
@bot.message_handler(content_types=['text'])
def send_text(message):
		count_mess=0 #не трогать, завязано на триггеры
		
		#запись сообщений
		global hist

		hist.append([
			message.chat.id, 
			message.from_user.first_name, 
			message.text.lower(), 
			message.date, 
			datetime.fromtimestamp(message.date).date(),
			int(datetime.fromtimestamp(message.date).strftime('%H')),
			int(datetime.fromtimestamp(message.date).strftime('%M'))
			])
		hist2 = pd.DataFrame(hist, columns=['chat','name','message','timestamp','date','hour','min'])
		
		#knopki
		if message.text.lower() == 'комментарий к документу 📄':
			name = message.from_user.first_name
			bot.send_message(message.chat.id, name+', '+comments_list[int(random.random()*(len(comments_list)-1))])
		if message.text.lower() == 'обсудить скоуп 🌚':
			name = message.from_user.first_name
			bot.send_message(message.chat.id, name+', '+scope_list[int(random.random()*(len(scope_list)-1))])
		if message.text.lower() == 'поговорить за контент 💩':
			name = message.from_user.first_name
			bot.send_message(message.chat.id, name+', '+content_list[int(random.random()*(len(content_list)-1))])
		if message.text.lower() == 'тимбарометр 🌡':
			this_chat_hist = hist2[hist2['chat']==message.chat.id]
			this_chat_hist = this_chat_hist[this_chat_hist['date']>=date.today()-timedelta(days=7)]
			#обработка ошибки пустого датафрейма
			if this_chat_hist.empty == 1:
				tm=0
			else:
				tm=this_chat_hist.groupby(['chat']).count().iloc[0,0]
			print(tm)
			suboptimal_time_pivot = this_chat_hist[this_chat_hist['hour']<9]
			suboptimal_time_pivot.append(this_chat_hist[this_chat_hist['hour']>21])
			if suboptimal_time_pivot.empty ==1:
				sttm=0
			else:
				sttm=suboptimal_time_pivot.groupby(['chat']).count().iloc[0,0]

			if sttm/tm*100>35:
				zone="Кажется, что-то пошло не так. :( Нужно срочно исправлять!" 
			else:
				if sttm/tm*100>20:
					zone="Ну в целом ок. Работаем дальше" 
				else:
					zone="Гениальный лайфстайл!"

			if tm/100*100>250:
					zone2="Вы только болтаете? Или работаете тоже?"
			else:
				if tm/100*100>100:
					zone2="Рабочая атмосфера!"
				else: 
					if tm/100*100>50:
						zone2="Что-то вы притихли, все в порядке?"
					else:
						zone2="А вы вообще работаете?"


			bot.send_message(message.chat.id, 
				'Активность в чате за последнюю неделю: '+str(int(tm/100*100))+"% "+zone2+"  "
				'Доля сообщений в чате после 21:00 и ранее 9:00 за последнюю неделю: '+str(int(sttm/tm*100))+"% "+zone)
			name_pivot =this_chat_hist.groupby(['name']).count() #по юзерам
			name_pivot['share']=name_pivot[['message']]/tm*100
			m = name_pivot[['share']].sort_values(by=['share'], ascending=False).to_string()
			bot.send_message(message.chat.id, 'Активность в чате:'+m)

		#реакция на триггеры
		for i in range (0,len(triggers)-1):
			#print(i)
			#print(triggers[i])
			#print(triggers_pb[i])
			pb=float(triggers_pb[i])
			if 	message.text.lower().find(triggers[i])>=0:
				if random.random()>pb:
					bot.send_message(message.chat.id, reaction[i][int((random.random()*len(reaction[i])-1))])
					count_mess =+1

		#TLDR-триггер
		#print(len(message.text.lower()))
		if len(message.text.lower()) > 450 :
			name = message.from_user.first_name
			bot.send_message(message.chat.id, name+', '+' а синтез можно?')

		#рандомные вбросы
		if count_mess<1:
			if random.random()>0.97:
				if random.random()>0.95:
					bot.send_message(message.chat.id, add_list[int((random.random()*len(add_list)-1))])
					bot.send_message(message.chat.id, rs_list[int((random.random()*len(rs_list)-1))])
				else:
					bot.send_message(message.chat.id, rs_list[int((random.random()*len(rs_list)-1))])
			if random.random()<0.03:
				name = message.from_user.first_name
				bot.send_message(message.chat.id, name+', '+prs_list[int((random.random()*len(prs_list)-1))])

		
		#name_pivot['share'][i] = name_pivot['message'][i]/total_mes_in_the_chat
		#токенизатор и сентимент анализ
		tokenizer = RegexTokenizer()
		tokens = tokenizer.split(message.text.lower())
		model = FastTextSocialNetworkModel(tokenizer=tokenizer)
		msgs = [message.text.lower()]
		results = model.predict(msgs, k=5)
		print(results)

		#эмоциональные реакции
		if count_mess<1:
			if results[0]['positive']>=0.45:
				if random.random()>0.7:
					bot.send_message(message.chat.id, '👍')
			if results[0]['negative']>=0.:
				if random.random()>0.7:
					bot.send_message(message.chat.id, '💩')


#запуск
bot.polling()
print('ok')
