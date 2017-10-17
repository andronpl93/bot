import config
import sys
from decorators import fatallError,Buttons
import botan
import telebot
from telebot import types
from bs4 import BeautifulSoup
from urllib.request import urlopen
import login


try:
	bot = telebot.TeleBot(config.token)
except Exception:
	pass
tb={}
pr={}

	
@bot.message_handler(commands=["start",'Выход'])
def start(message): 
    photo = open('parallel_logo.jpg', 'rb')
    bot.send_photo(message.chat.id,"https://pp.userapi.com/c841023/v841023015/307a2/eck54_5e5S8.jpg",
		'Компания Параллель приветствует вас, {0} '.format(message.chat.first_name)+u'\U0001F44B'  )  
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name+' ') for name in ['Цены '+u'\U0001F4B9','Баланс на карте'+u'\U0001F4B3']])
    bot.send_message(message.chat.id, 'Выберите интересующую информацию',reply_markup=keyboard)
    botan.track(config.botan_key, message.chat.id, message, 'Старт')


@bot.message_handler(func=lambda m:m.text=='Цены '+u'\U0001F4B9')
@fatallError
def price(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Днепропетровская','Донецкая']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Запорожская','Луганская']])
        obl = bot.send_message(message.chat.id, 'Выберите область',
                reply_markup=keyboard)
        bot.register_next_step_handler(obl,fObl)
        botan.track(config.botan_key, message.chat.id, message, 'Цена')
@fatallError
@Buttons(bot)
def fObl(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in config.dObl[message.text]])
        city = bot.send_message(message.chat.id, 'Город',
                reply_markup=keyboard)
        bot.register_next_step_handler(city,fCity)
        botan.track(config.botan_key, message.chat.id, message, message.text)
@fatallError
@Buttons(bot)
def fCity(message):
        global pr,tb
        site=urlopen("http://parallel.ua/retail-prices/?city_id="+str(config.dCity[message.text]))
        site = BeautifulSoup(site,"html.parser")
        table = site.find('table',{'class':'regions'})
        tb={
            'head':[],
            'body':[],
            'address':[]}
        for j,th in enumerate(table.findAll('th')):
                if j==0:
                    continue
                else:
                    tb["head"].append(th.text.replace('*',''))
        for i,tr in enumerate(table.findAll('tr'),1):      
            for j,td in enumerate(tr.findAll('td')):
                if j==0:
                    if i%2==0:
                        tb['body'].append([])
                    continue
                else:
                    if i%2==0:
                        tb['body'][-1].append(td.text)
                    else:
                        tb['address'].append(td.findAll('p')[0].text)

        if len(tb['address'])!=0:                
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(*[types.InlineKeyboardButton(text=i,callback_data=str(i)) for i in range(1,len(tb['address'])+1)])
        azs = bot.send_message(message.chat.id, '\n'.join("{0}. {1}".format(str(i+1),j) for i,j in enumerate(tb['address'])),
                reply_markup=keyboard)
        if len(tb['address'])==1:
            pr = bot.send_message(chat_id=message.chat.id, text="\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+str(tb['body'][0][i]) for i in range(len(tb['head']))))
        else:
            pr = bot.send_message(message.chat.id, 'Выберите АЗС')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['/Выход']])
        bot.send_message(message.chat.id, 'Горячая линия - 0 800 50 3333',reply_markup=keyboard)
        botan.track(config.botan_key, message.chat.id, message, message.text)
        
@bot.callback_query_handler(func=lambda c: c.data)
@fatallError 
def pages(c):
    try:
        int(c.data)
    except ValueError:
        return
    bot.edit_message_text(chat_id=c.message.chat.id, message_id=pr.message_id, text=
                          "\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+str(tb['body'][int(c.data)-1][i]) for i in range(len(tb['head']))))






@bot.message_handler(func=lambda m:m.text[:15]==u'Баланс на карте')
@fatallError
def balance(message):
        card=login.findCard(message.from_user.id)
        if len(card)==0:
                message.text=u"Добавить карту"
                nomCard(message)  
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if len(card)==1:
                        keyboard.add(*[types.KeyboardButton(name) for name in [u"Разлогинить",u"Добавить карту",u"/Выход"]])
                        mess=bot.send_message(message.chat.id, login.req(card[0][1],card[0][2])[1],reply_markup=keyboard)
                        nomCard.loginn=card[0][1]
                        bot.register_next_step_handler(mess,nomCard)
                else:
                        keyboard.add(*[types.KeyboardButton(name[1]) for name in card])
                        keyboard.add(*[types.KeyboardButton(name) for name in [u"Добавить карту",u"/Выход"]])
                        mess=bot.send_message(message.chat.id, u'Выберите карту',reply_markup=keyboard)   
                        bot.register_next_step_handler(mess,choiceCard)
                
        botan.track(config.botan_key, message.chat.id, message, u'Баланс')


@fatallError
@Buttons(bot)
def nomCard(message):
        if  message.text==u"/Выход":
                return 0
        d=dict.fromkeys([u"Разлогинить",u"Добавить карту"])
        d[message.text]
        if message.text!=u"Разлогинить":
                def logC(message):
                        log=message.text                
                        def pas(message):
                                pas=message.text
                                a=login.req(log,pas)
                                bot.send_message(message.chat.id,a[1])
                                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                keyboard.add(u"/Выход")
                                if a[0]:
                                        if login.findCard(message.from_user.id,log,s=False)!=0:
                                                login.writeCard(message.from_user.id,log,pas)
                                                bot.send_message(message.chat.id, u'Карта сохранена',reply_markup=keyboard)
                                        else:
                                                bot.send_message(message.chat.id, u'Данная карта уже зарегистрированна',reply_markup=keyboard) 
                                else:
                                        bot.send_message(message.chat.id, u'Телефон горячей линии (бесплатный с мобильных и стационарных телефонов):\n 0 800 50 3333')
                                        mess=bot.send_message(message.chat.id, u'Введите номер карты чтобы попробовать еще раз или нажмите Выход',reply_markup=keyboard)
                                        bot.register_next_step_handler(mess,logC)
                        mess=bot.send_message(message.chat.id, u'Введите пароль')   
                        bot.register_next_step_handler(mess,pas)
                        
                keyboard = types.ReplyKeyboardRemove()
                mess=bot.send_message(message.chat.id, u'Введите номер карты',reply_markup=keyboard)
                bot.register_next_step_handler(mess,logC)
        else:
                login.logOut(message.from_user.id,nomCard.loginn)
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, u'Карта была удалена',reply_markup=keyboard)
                start(message)
                                                                                                                                                            
@fatallError
@Buttons(bot)
def choiceCard(message):
        if  message.text==u"/Выход":
                return 0
        if message.text==u"Добавить карту":
                nomCard(message)
        else:
                card=login.findCard(message.from_user.id,message.text)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in [u"Разлогинить",u"Добавить карту",u"/Выход"]])
                mess=bot.send_message(message.chat.id,login.req(card[0][1],card[0][2])[1],reply_markup=keyboard)
                nomCard.loginn=card[0][1]
                bot.register_next_step_handler(mess,nomCard)

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
