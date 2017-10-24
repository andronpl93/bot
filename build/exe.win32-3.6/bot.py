import config
from config import saveLoveCity,delLoveCity,home
import sys
from decorators import fatallError,Buttons
import botan
import telebot
from telebot import types
from bs4 import BeautifulSoup
from urllib.request import urlopen
import login
import spaming
import time
import datetime
import traceback
import pyodbc


try:
	bot = telebot.TeleBot(config.token)
except Exception:
	pass
tb={}
pr={}

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	
@bot.message_handler(commands=["start",home[1:]])
@fatallError
def start(message):
    if message.text=='/start':
            spaming.check(message.from_user.id,message.from_user.first_name,message.from_user.last_name)
    bot.send_photo(message.chat.id,"https://pp.userapi.com/c841023/v841023015/307a2/eck54_5e5S8.jpg",
		'Компания Параллель приветствует вас, {0} '.format(message.chat.first_name)+u'\U0001F44B'  )  
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [u'Цены'+u'\U0001F4B9',u'Баланс на карте'+u'\U0001F4B3','Акции'+u"\U00002728"]])
    bot.send_message(message.chat.id, 'Выберите интересующую информацию',reply_markup=keyboard)
    botan.track(config.botan_key, message.chat.id, message, 'Старт')

############################################################
@bot.message_handler(func=lambda m:m.text[:4]==u'Цены')
@fatallError
def price(message):
        obl=config.obl()
        if not len(obl):
               bot.send_message(message.chat.id,config.verySorry,reply_markup=types.ReplyKeyboardRemove())
               start(message)
               return  0
        fObl.obl=obl
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        a = login.findLoveCity(message.from_user.id)
        if len(a)!=0:
                keyboard.add(*[types.KeyboardButton(name+u'\U0001F31F') for name in a])
        keyboard.add(*[types.KeyboardButton(name) for name in obl[:2]])
        keyboard.add(*[types.KeyboardButton(name) for name in obl[2:]])
        keyboard.add(types.KeyboardButton(home))
        obl = bot.send_message(message.chat.id, 'Выберите область',
                reply_markup=keyboard)

        bot.register_next_step_handler(obl,fObl)
        botan.track(config.botan_key, message.chat.id, message, 'Цена')
@fatallError
@Buttons(bot)
def fObl(message):
        if message.text not in fObl.obl:
                message.text=str(message.text).translate(non_bmp_map)[:-1]
                a=config.city(message.text,0)
                if not len(a):
                       bot.send_message(message.chat.id,config.verySorry,reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0
                fCity.d=a
                fCity.l=0
                fCity(message)
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                a=config.city(message.text)
                if not len(a):
                       bot.send_message(message.chat.id,config.verySorry,reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0                
                keyboard.add(*[types.KeyboardButton(str(name)) for name in a])
                keyboard.add(types.KeyboardButton(home))
                city = bot.send_message(message.chat.id, 'Город',
                        reply_markup=keyboard)
                fCity.d=a
                fCity.l=1
                bot.register_next_step_handler(city,fCity)
                botan.track(config.botan_key, message.chat.id, message, message.text)
@fatallError
@Buttons(bot)
def fCity(message):
        global pr,tb
        site=urlopen("http://parallel.ua/retail-prices/?city_id="+str(fCity.d[message.text]))
        site = BeautifulSoup(site,"html.parser")
        table = site.find('table',{'class':'regions'})
        tb={
            'head':[],
            'body':[],
            'address':[]}
        for j,th in enumerate(table.findAll('th')):
                    tb["head"].append(th.text.replace('*',''))
        for i,tr in enumerate(table.findAll('tr'),1):      
            for j,td in enumerate(tr.findAll('td')):
                if j==0:
                    if i%2==0:
                        tb['body'].append([])
                    if i%2==0:
                       tb['body'][-1].append(td.text)     
                else:
                    if i%2==0:
                        tb['body'][-1].append(td.text)
                    else:
                        tb['address'].append(td.findAll('p')[0].text)
        if not len(tb['body']):
                       bot.send_message(message.chat.id,config.verySorry,reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0
        print(tb['head'])
        del tb['head'][1]
        tb['head'][0]='Бренд     '
        for i in tb['body']:
                del i[1]
        
                
        
        keyboard = types.InlineKeyboardMarkup()
        if len(tb['address'])==1:
            pr = bot.send_message(chat_id=message.chat.id,
                                  text="\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+'<b>'+str(tb['body'][0][i])+"</b>"
                                                 for i in range(len(tb['head']))),parse_mode='HTML')
        else:
            pr = bot.send_message(message.chat.id,'<b>Выберите АЗС</b>',parse_mode='HTML')
            keyboard.add(*[types.InlineKeyboardButton(text=i,callback_data=str(i)) for i in range(1,len(tb['address'])+1)])
        try:
                keyboard.add(*[types.InlineKeyboardButton(text=config.showMap,url=config.dMaps(message.text))])
        except :
                pass
        azs = bot.send_message(message.chat.id, '\n'.join("<b>{0}</b>. {1}".format(str(i+1),j) for i,j in enumerate(tb['address'])),parse_mode='HTML',reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if fCity.l!=0:
                save_or_del=saveLoveCity
        else:
                save_or_del=delLoveCity
        keyboard.add(*[types.KeyboardButton(name) for name in [home,save_or_del]])

        mess=bot.send_message(message.chat.id, 'Горячая линия - +380800503333',reply_markup=keyboard)
        saveCity.city=message.text
        bot.register_next_step_handler(mess,saveCity)
        botan.track(config.botan_key, message.chat.id, message, message.text)
        
@fatallError
@Buttons(bot)        
def saveCity(message):
        if message.text==saveLoveCity:
                f = open('files/saveAZS.txt' , 'a')
                f.write("{0};{1}\n".format(message.from_user.id,saveCity.city))
                f.close()
                
        else:
            ret=[]
            with open('files/saveAZS.txt','r') as f:
                    for i in f:                           
                            if str(message.from_user.id)==i.split(";")[0] and saveCity.city==i.split(";")[1][:-1]:
                                pass
                            else:
                                ret.append(i)

            with open('files/saveAZS.txt','w') as f:
                for i in ret:
                    f.write(i)
        start(message)
        
@bot.callback_query_handler(func=lambda c: c.data)
@fatallError 
def pages(c):
    try:
        int(c.data)
    except ValueError:
        return
    bot.edit_message_text(chat_id=c.message.chat.id, message_id=pr.message_id,
                          text="\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+"<b>"+str(tb['body'][int(c.data)-1][i])+"</b>"
                                         for i in range(len(tb['head']))),parse_mode='HTML')




#########################################

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
                        keyboard.add(*[types.KeyboardButton(name) for name in [u"Разлогинить",u"Добавить карту",home]])
                        mess=bot.send_message(message.chat.id, login.req(card[0][1],card[0][2])[1],reply_markup=keyboard)
                        nomCard.loginn=card[0][1]
                        bot.register_next_step_handler(mess,nomCard)
                else:
                        keyboard.add(*[types.KeyboardButton(name[1]) for name in card])
                        keyboard.add(*[types.KeyboardButton(name) for name in [u"Добавить карту",home]])
                        mess=bot.send_message(message.chat.id, u'Выберите карту',reply_markup=keyboard)   
                        bot.register_next_step_handler(mess,choiceCard)
                
        botan.track(config.botan_key, message.chat.id, message, u'Баланс')


@fatallError
@Buttons(bot)
def nomCard(message):
        d=dict.fromkeys([u"Разлогинить",u"Добавить карту"])
        d[message.text]
        if message.text!=u"Разлогинить":
                def logC(message):
                        if  message.text in [home,'/start']:
                                return 0
                        log=message.text                
                        def pas(message):
                                pas=message.text
                                a=login.req(log,pas)
                                bot.send_message(message.chat.id,a[1])
                                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                keyboard.add(home)
                                if a[0]:
                                        if login.findCard(message.from_user.id,log,s=False)!=0:
                                                login.writeCard(message.from_user.id,log,pas)
                                                bot.send_message(message.chat.id, u'Карта сохранена',reply_markup=keyboard)
                                        else:
                                                bot.send_message(message.chat.id, u'Данная карта уже зарегистрированна',reply_markup=keyboard) 
                                else:
                                        bot.send_message(message.chat.id, u'Телефон горячей линии (бесплатный с мобильных и стационарных телефонов):\n +380800503333')
                                        mess=bot.send_message(message.chat.id, u'Введите номер карты чтобы попробовать еще раз или нажмите {}'.format(home),reply_markup=keyboard)
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
                botan.track(config.botan_key, message.chat.id, message, 'Разлогинились')
                                                                                                                                                            
@fatallError
@Buttons(bot)
def choiceCard(message):
        if message.text==u"Добавить карту":
                nomCard(message)
        else:
                card=login.findCard(message.from_user.id,message.text)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in [u"Разлогинить",u"Добавить карту",home]])
                mess=bot.send_message(message.chat.id,login.req(card[0][1],card[0][2])[1],reply_markup=keyboard)
                nomCard.loginn=card[0][1]
                bot.register_next_step_handler(mess,nomCard)

                

##############################spam

@bot.message_handler(commands=["spaming"])
def spam(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeni.txt'):
                file = bot.send_message(message.chat.id, 'Введите название файла с получателями',reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(file,spamFile)  
        else:
                bot.send_message(message.chat.id, 'Данная функция доступна только Одмену',reply_markup=types.ReplyKeyboardRemove())
def spamFile(message):
        text = bot.send_message(message.chat.id, 'Введите текст сообщения',reply_markup=types.ReplyKeyboardRemove())
        spamText.file=message.text
        bot.register_next_step_handler(text,spamText)
        
def spamText(message):
        img = bot.send_message(message.chat.id, 'Введите ссылку на картинку или "нет", если картинки не будет',reply_markup=types.ReplyKeyboardRemove())
        pushSpam.file=spamText.file
        pushSpam.text=message.text
        bot.register_next_step_handler(img,pushSpam)

@fatallError
def pushSpam(message):
        img=message.text
        li=[]
        with open('files/people/'+pushSpam.file,'r') as f:
                for i in f:
                        li.append(i)
        def push(message):
                if message.text in [home,'/start']:
                        return 0
                for l in li:
                        if len(img)>3 :
                                bot.send_photo(int(l[:-1]), str(img) )
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        keyboard.add(types.KeyboardButton(home))
                        bot.send_message(int(l[:-1]),pushSpam.text,reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Вы собираетесь отправить данному к-ву человек : {0}, \n это сообщение:'.format(len(li)))
        if len(img)>3 :
                bot.send_photo(message.chat.id,message.text )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Отправить',home]])
        mess=bot.send_message(message.chat.id,pushSpam.text,reply_markup=keyboard )
        bot.register_next_step_handler(mess,push)  

#########################################################################
@bot.message_handler(func=lambda m:m.text[:5]==u'Акции')
@fatallError
@Buttons(bot) 
def actions(message):
        rez={}
        with open('files/actions.txt','r',encoding='utf-8') as f:
                for i in f:
                        i=i.split(';')
                        rez[i[0]]=(str(i[1]).replace('\\n','\n'),str(i[2]),i[3])
        if len(rez)==0:
                bot.send_message(message.chat.id,"На данный момент, нет активных акций")
                return 0
        long=[]
        short=[]
        for i in rez.keys():
                if len(i)>21:
                        long.append(i)
                else:
                        short.append(i)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(*[types.KeyboardButton(name) for name in short])
        for i in long:
                keyboard.add(i) 
        keyboard.add(home)
        mess=bot.send_message(message.chat.id,config.changeAction,reply_markup=keyboard)
        action.rez=rez
        action.mess=mess
        botan.track(config.botan_key, message.chat.id, message, 'Акции')
        bot.register_next_step_handler(mess,action)
        
        
@fatallError
@Buttons(bot)        
def action(message):
        if len(action.rez[message.text][2])>5:
                bot.send_photo(message.chat.id,action.rez[message.text][2])
        keyboard=types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text='Детальная информация на сайте',url=action.rez[message.text][1])]) 
        mes=bot.send_message(message.chat.id,'<b>{0}</b>\n\n {1}'.format(message.text,str(action.rez[message.text][0])),parse_mode='HTML',reply_markup=keyboard)
        botan.track(config.botan_key, message.chat.id, message, message.text)
        bot.register_next_step_handler(action.mess,action)

##
@bot.message_handler(commands=["addAction"])
@fatallError
@Buttons(bot)
def addAction(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeniAction.txt'):
                addAction2.flag=True
                mess=bot.send_message(message.chat.id,"Введите название акции. Название будет отображаться на кнопке, желаемая длина должна быть не более 20-ти символов. Очень рекомендуем использовать эмоджи, стикеры использовать нельзя",reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(mess,addAction2)
@fatallError
@Buttons(bot)
def addAction2(message):
                addAction3.name=message.text
                mess=bot.send_message(message.chat.id,"Введите описание акции. Описание не обязательно должно быть таким же как и на сайте.Рекомендуем кратко и лаконично описать акцию, а детальную механику можно посмотреть на сайте")
                bot.register_next_step_handler(mess,addAction3)
@fatallError
@Buttons(bot)
def addAction3(message):
                addAction4.description= message.text
                mess=bot.send_message(message.chat.id,"""Введите ссылку на акцию, на сайте parallel.ua""")
                bot.register_next_step_handler(mess,addAction4)
@fatallError
@Buttons(bot)
def addAction4(message):
                addAction5.link=message.text
                mess=bot.send_message(message.chat.id,"""Введите ссылку на картинку, или напишите "нет", если картинка не нужна """)
                bot.register_next_step_handler(mess,addAction5)
@fatallError
@Buttons(bot)
def addAction5(message):
        with open('files/actions.txt','a',encoding='utf-8') as f:
                f.write("{0};{1};{2};{3}\n".format(addAction3.name,addAction4.description.replace('\n','\\n').replace(';',' '),addAction5.link,message.text))

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(home)
        bot.send_message(message.chat.id,'Акция успешно добавлена',reply_markup=keyboard)
                
##
@bot.message_handler(commands=["deleteAction"])
@fatallError
@Buttons(bot)
def deleteAction(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeniAction.txt'):
                rez={}
                with open('files/actions.txt','r',encoding='utf-8') as f:
                        for i in f:
                                i=i.split(';')
                                rez[i[0]]=(i[1],i[2],i[3])
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
                keyboard.add(*[types.KeyboardButton(name) for name in rez.keys()])
                keyboard.add(home)
                mess=bot.send_message(message.chat.id,"Выберите акцию, которую хотите удалить",reply_markup=keyboard)
                deleteAction2.rez=rez
                bot.register_next_step_handler(mess,deleteAction2)
@fatallError
@Buttons(bot)
def deleteAction2(message):
                deleteAction3.mess=message.text
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
                keyboard.add(*[types.KeyboardButton(name) for name in ['Удалить',home]])
                bot.send_message(message.chat.id,"Вы собираетесь удалить акцию {0}".format(message.text))
                if len(deleteAction2.rez[message.text][2])>5:
                        bot.send_photo(message.chat.id,deleteAction2.rez[message.text][2])
                bot.send_message(message.chat.id,'<b>{0}</b>\n\n {1}'.format(message.text,str(deleteAction2.rez[message.text][0])),parse_mode='HTML')
                mess=bot.send_message(message.chat.id,'<b>Удалить?</b>',parse_mode='HTML',reply_markup=keyboard)
                bot.register_next_step_handler(mess,deleteAction3)
@fatallError
@Buttons(bot)
def deleteAction3(message):
        with open('files/actions.txt','w',encoding='utf-8') as f:
                for i in deleteAction2.rez.keys():
                        if  i!=deleteAction3.mess:
                            f.write("{0};{1};{2};{3}".format(i,deleteAction2.rez[i][0],deleteAction2.rez[i][1],deleteAction2.rez[i][2]))
        message.text='start'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(home)
        bot.send_message(message.chat.id,'Акция успешно удалена',reply_markup=keyboard)
                
                
                
                

###############################################################        
@bot.message_handler(commands=["db"])
def db(message):
       # connectString = 'Driver={Oracle in OraHome92};Server=172.24.10.13:1600;DATABASE=KONTORA.BEZNAL.PARALLEL.UA;uid=PARALLEL_USER;pwd=S1mple_U5er'
        #dsn=  '(DESCRIPTION =(ADDRESS =(PROTOCOL = TCP)(HOST = 172.24.10.13)(PORT = 1600))(CONNECT_DATA = (SERVER = DEDICATED)(service_name = mainpr)))'
        #cnxn = pyodbc.connect(connectString)
        conn = pyodbc.connect(
    r'DRIVER={Oracle in OraHome92};'+
    r'PROTOCOL = TCP;'+
    r'SERVER=DEDICATED;'+
    r'HOST = 172.24.10.13;'+
    r'PORT = 1600;'+
    r'service_name = mainpr;'+
    r'DATABASE=KONTORA.BEZNAL.PARALLEL.UA;'+
    r'UID=PARALLEL_USER;'+
    r'PWD=S1mple_U5er'
    )
       # dsn=cx_Oracle.makedsn('172.24.10.13','1600','KONTORA.BEZNAL.PARALLEL.UA')

       # con=cx_Oracle.connect('PARALLEL_USER', 'S1mple_U5er', 'KONTORA.BEZNAL.PARALLEL.UA') 
       # print(con)


######################
def gogo():
    try:
        bot.polling(none_stop=True)
    except:
        f = open('fattalErrors.txt' , 'a')
        f.write("{0}~ {1} \n\n".format(datetime.datetime.now(),traceback.format_exc()))
        f.close()
        time.sleep(5)
        gogo()

        
if __name__ == '__main__':
        gogo()

