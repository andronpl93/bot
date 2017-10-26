import config
import sys
from decorators import fatallError,Buttons,ButtLang
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
	language=config.fLang()
except Exception:
	pass
tb={}
pr={}

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	
@bot.message_handler(commands=["start",config.text['home']['ua'][1:],config.text['home']['ru'][1:]])
@fatallError
@ButtLang(bot,language)
def start(message):
    if message.text=='/start':
            spaming.check(message.from_user.id,message.from_user.first_name,message.from_user.last_name)
            selectLang(message)
            return 0
    bot.send_photo(message.chat.id,"https://pp.userapi.com/c841023/v841023015/307a2/eck54_5e5S8.jpg",
		'{1}, {0} '.format(message.chat.first_name,config.text['hello'][bot.lang])+u'\U0001F44B'  )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textPrice'][bot.lang],config.text['textActions'][bot.lang]]])
    keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textBalance'][bot.lang],config.text['textLangSel'][bot.lang]]])
    bot.send_message(message.chat.id,config.text['selInfo'][bot.lang],reply_markup=keyboard)
    botan.track(config.botan_key, message.chat.id, message, 'Старт')

###########################
@bot.message_handler(func=lambda m:m.text[:-1]==config.text['textLangSel']['ru'][:-1] or m.text[:-1]==config.text['textLangSel']['ua'][:-1])
@fatallError
@ButtLang(bot,language)
def selectLang(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textselL']['ua'],config.text['textselL']['ru']]])
        keyboard.add(config.text['home'][bot.lang])
        mess=bot.send_message(message.chat.id,config.text['textLang'][bot.lang],reply_markup=keyboard)
        bot.register_next_step_handler(mess,selectLang2)
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def selectLang2(message):
        ret=[]
        global bot
        if message.text==config.text['textselL']['ua']:
                bot.lang='ua'
                language[message.from_user.id]='ua'
        else:
                if message.text==config.text['textselL']['ru']:
                        bot.lang='ru'
                        language[message.from_user.id]='ru'
                else:
                       raise KeyError
        with open('files/lang.txt','r') as f:
                for i in f:
                        i=i.split(';')

                        if i[0]!=str(message.from_user.id):
                                ret.append(i)
        with open('files/lang.txt','w') as f:
                for i in ret:
                        f.write("{0};{1}\n".format(i[0],i[1]))
                f.write("{0};{1}\n".format(message.from_user.id,bot.lang))    
        bot.send_message(message.chat.id,config.text['textLengEdit'][bot.lang])
        start(message)

############################################################
@bot.message_handler(func=lambda m:m.text[:4]==config.text['textPrice']['ru'][:-1] or m.text[:4]==config.text['textPrice']['ua'][:-1])
@fatallError
@ButtLang(bot,language)
def price(message):
        obl=config.obl(bot.lang)
        if not len(obl):
               bot.send_message(message.chat.id,config.text['verySorry'][bot.lang],reply_markup=types.ReplyKeyboardRemove())
               start(message)
               return  0
        fObl.obl=obl
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        a = login.findLoveCity(message.from_user.id,bot.lang)
        if len(a)!=0:
                cobl=config.text['selectAreaOrCity'][bot.lang]
                keyboard.add(*[types.KeyboardButton(name+u'\U0001F31F') for name in a])
                fCity.lov=a
        else:
                fCity.lov=[]
                cobl=config.text['selectArea'][bot.lang]
        keyboard.add(*[types.KeyboardButton(name) for name in obl[:2]])
        keyboard.add(*[types.KeyboardButton(name) for name in obl[2:]])
        keyboard.add(types.KeyboardButton(config.text['home'][bot.lang]))
        obl = bot.send_message(message.chat.id, cobl,
                reply_markup=keyboard)

        bot.register_next_step_handler(obl,fObl)
        botan.track(config.botan_key, message.chat.id, message, 'Цена')
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def fObl(message):
        if message.text not in fObl.obl:
                message.text=str(message.text).translate(non_bmp_map)[:-1]
                a=config.city(message.text,0,bot.lang)
                if not len(a):
                       bot.send_message(message.chat.id,config.text['verySorry'][bot.lang],reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0
                fCity.d=a
                fCity(message)
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                a=config.city(message.text,1,bot.lang)
                if not len(a):
                       bot.send_message(message.chat.id,config.text['verySorry'][bot.lang],reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0                
                keyboard.add(*[types.KeyboardButton(str(name)) for name in a])
                keyboard.add(types.KeyboardButton(config.text['home'][bot.lang]))
                city = bot.send_message(message.chat.id, config.text['textCity'][bot.lang],
                        reply_markup=keyboard)
                fCity.d=a
                fCity.l=1
                bot.register_next_step_handler(city,fCity)
                botan.track(config.botan_key, message.chat.id, message, message.text)
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def fCity(message):
        global pr,tb
        site=urlopen("http://parallel.ua/"+str(bot.lang=='ua' and 'uk/' or '')+"retail-prices/?city_id="+str(fCity.d[message.text]))
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
                       bot.send_message(message.chat.id,config.text['verySorry'][bot.lang],reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0
        del tb['head'][1]
        tb['head'][0]='Бренд   '
        for i in tb['body']:
                del i[1]
        
                
        
        keyboard = types.InlineKeyboardMarkup()
        if len(tb['address'])>1:
            keyboard.add(*[types.InlineKeyboardButton(text=i,callback_data=str(i)) for i in range(1,len(tb['address'])+1)])
        a=config.dMaps(message.text)
        if a is not None:
               keyboard.add(*[types.InlineKeyboardButton(text=config.text['showMap'][bot.lang],url=a)])
        azs = bot.send_message(message.chat.id, '\n'.join("<b>{0}</b>. {1}".format(str(i+1),j) for i,j in enumerate(tb['address'])),parse_mode='HTML',reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if message.text not in fCity.lov:
                save_or_del=config.text['saveLoveCity'][bot.lang]
        else:
                save_or_del=config.text['delLoveCity'][bot.lang]

        if len(tb['address'])==1:
                pr = bot.send_message(chat_id=message.chat.id,
                text="\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+'<b>'+str(tb['body'][0][i])+"</b>"+str(i==0 and '\n' or '')
                                                 for i in range(len(tb['head']))),parse_mode='HTML')
        else:
                pr = bot.send_message(message.chat.id,'<b>{0}</b>'.format(config.text['selAZS'][bot.lang]),parse_mode='HTML')
        pages.pr=pr
        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['home'][bot.lang],save_or_del]])
        mess=bot.send_message(message.chat.id, '{0} - +380800503333'.format(config.text['hoteLine'][bot.lang]),reply_markup=keyboard)
        saveCity.city=message.text
        bot.register_next_step_handler(mess,saveCity)
        botan.track(config.botan_key, message.chat.id, message, message.text)
        
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def saveCity(message):
        if message.text==config.text['saveLoveCity'][bot.lang]:
                f = open('files/saveAZS.txt' , 'a')
                f.write("{0};{1};{2}\n".format(message.from_user.id,saveCity.city,bot.lang))
                f.close()
                
        else:
            ret=[]
            with open('files/saveAZS.txt','r') as f:
                    for i in f:                           
                            if str(message.from_user.id)==i.split(";")[0] and saveCity.city==i.split(";")[1] and i.split(";")[2][:-1]==bot.lang:
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
    bot.edit_message_text(chat_id=c.message.chat.id, message_id=pages.pr.message_id,
                          text="\n".join(str(tb['head'][i])+" "*int((25-len(tb['head'][i]))*1.8)+"<b>"+str(tb['body'][int(c.data)-1][i])+"</b>"+str(i==0 and '\n' or '')
                                         for i in range(len(tb['head']))),parse_mode='HTML')




#########################################

@bot.message_handler(func=lambda m:m.text[:15]==config.text['textBalance']['ru'][:-1] or m.text[:15]==config.text['textBalance']['ua'][:-1])
@fatallError
@ButtLang(bot,language)
def balance(message):
        card=login.findCard(message.from_user.id)
        if len(card)==0:
                message.text=config.text['textAddCard'][bot.lang]
                nomCard(message)  
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if len(card)==1:
                        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textLogOut'][bot.lang],config.text['textAddCard'][bot.lang],config.text['home'][bot.lang]]])
                        mess=bot.send_message(message.chat.id, login.req(card[0][1],card[0][2],bot.lang)[1],reply_markup=keyboard)
                        nomCard.loginn=card[0][1]
                        bot.register_next_step_handler(mess,nomCard)
                else:
                        keyboard.add(*[types.KeyboardButton(name[1]) for name in card])
                        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textAddCard'][bot.lang],config.text['home'][bot.lang]]])
                        mess=bot.send_message(message.chat.id, config.text['textSelCard'][bot.lang],reply_markup=keyboard)   
                        bot.register_next_step_handler(mess,choiceCard)
                
        botan.track(config.botan_key, message.chat.id, message, u'Баланс')


@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def nomCard(message):
        d=dict.fromkeys([config.text['textLogOut'][bot.lang],config.text['textAddCard'][bot.lang]])
        d[message.text]
        if message.text!=config.text['textLogOut'][bot.lang]:
                @Buttons(bot)
                def logC(message):
                        if  message.text in [config.text['home'][bot.lang],'/start']:
                                return 0
                        log=message.text
                        @Buttons(bot)
                        def pas(message):
                                pas=message.text
                                a=login.req(log,pas,bot.lang)
                                bot.send_message(message.chat.id,a[1])
                                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                keyboard.add(config.text['home'][bot.lang])
                                if a[0]:
                                        if login.findCard(message.from_user.id,log,s=False)!=0:
                                                login.writeCard(message.from_user.id,log,pas)
                                                bot.send_message(message.chat.id, config.text['textCardSave'][bot.lang],reply_markup=keyboard)
                                        else:
                                                bot.send_message(message.chat.id, config.text['textCardIn'][bot.lang],reply_markup=keyboard) 
                                else:
                                        bot.send_message(message.chat.id,config.text['textTelCardError'][bot.lang])
                                        mess=bot.send_message(message.chat.id, u'{1} {0}'.format(config.text['home'][bot.lang],config.text['textPop'][bot.lang]),reply_markup=keyboard)
                                        bot.register_next_step_handler(mess,logC)
                        
                        mess=bot.send_message(message.chat.id, config.text['textInPass'][bot.lang],reply_markup=keyboard)   
                        bot.register_next_step_handler(mess,pas)
                        
                ###############keyboard = types.ReplyKeyboardRemove()
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(config.text['home'][bot.lang])
                mess=bot.send_message(message.chat.id,config.text['textInCard'][bot.lang],reply_markup=keyboard)
                bot.register_next_step_handler(mess,logC)
        else:
                login.logOut(message.from_user.id,nomCard.loginn)
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, config.text['textCardDel'][bot.lang],reply_markup=keyboard)
                start(message)
                botan.track(config.botan_key, message.chat.id, message, config.text['textLogOut'][bot.lang])
                                                                                                                                                            
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def choiceCard(message):
        if message.text==config.text['textAddCard'][bot.lang]:
                nomCard(message)
        else:
                card=login.findCard(message.from_user.id,message.text)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textLogOut'][bot.lang],config.text['textAddCard'][bot.lang],config.text['home'][bot.lang]]])
                mess=bot.send_message(message.chat.id,login.req(card[0][1],card[0][2],bot.lang)[1],reply_markup=keyboard)
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
                if message.text in [config.text['home'][bot.lang],'/start']:
                        return 0
                for l in li:
                        if len(img)>3 :
                                bot.send_photo(int(l[:-1]), str(img) )
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        keyboard.add(types.KeyboardButton(config.text['home'][bot.lang]))
                        bot.send_message(int(l[:-1]),pushSpam.text,reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Вы собираетесь отправить данному к-ву человек : {0}, \n это сообщение:'.format(len(li)))
        if len(img)>3 :
                bot.send_photo(message.chat.id,message.text )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Отправить',config.text['home'][bot.lang]]])
        mess=bot.send_message(message.chat.id,pushSpam.text,reply_markup=keyboard )
        bot.register_next_step_handler(mess,push)  

#########################################################################
@bot.message_handler(func=lambda m:m.text[:5]==config.text['textActions']['ru'][:-1] or m.text[:5]==config.text['textActions']['ua'][:-1])
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def actions(message):
        rez={}
        with open('files/actions.txt','r',encoding='utf-8') as f:
                for i in f:
                        i=i.split(';')
                        if bot.lang=='ru':
                                rez[i[0]]=(str(i[2]).replace('\\n','\n'),str(i[4]),i[5])
                        else:
                               rez[i[1]]=(str(i[3]).replace('\\n','\n'),str(i[4]),i[5])
        if len(rez)==0:
                bot.send_message(message.chat.id,config.text['textNotActions'][bot.lang])
                return 0
        long1=[]
        long2=[]
        short=[]
        for i in rez.keys():
                if len(i)>21 and len(i)<=33:
                        long1.append(i)
                else:
                        if len(i)>33:
                                long2.append(i)
                        else:
                                short.append(i)
       
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if short:
                keyboard.add(*[types.KeyboardButton(name) for name in short])
        for i in range(0,len(long1),2):
                if  i+1<len(long1):
                        keyboard.add(*[types.KeyboardButton(name) for name in [long1[i],long1[i+1]]])
        if len(long1)%2!=0:
                keyboard.add(long1[-1])
                
        for i in long2:
                keyboard.add(i) 
        keyboard.add(config.text['home'][bot.lang])
        mess=bot.send_message(message.chat.id,config.text['changeAction'][bot.lang],reply_markup=keyboard)
        action.rez=rez
        action.mess=mess
        botan.track(config.botan_key, message.chat.id, message, 'Акции')
        bot.register_next_step_handler(mess,action)
        
        
@fatallError
@ButtLang(bot,language)
@Buttons(bot)
def action(message):
        if len(action.rez[message.text][2])>5:
                bot.send_photo(message.chat.id,action.rez[message.text][2])
        keyboard=types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=config.text['textMoreInfo'][bot.lang],url=action.rez[message.text][1])]) 
        mes=bot.send_message(message.chat.id,'<b>{0}</b>\n\n {1}'.format(message.text,str(action.rez[message.text][0])),parse_mode='HTML',reply_markup=keyboard)
        botan.track(config.botan_key, message.chat.id, message, message.text)
        bot.register_next_step_handler(action.mess,action)

##
@bot.message_handler(commands=["addAction"])
@fatallError
@Buttons(bot)
def addAction(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeniAction.txt'):
                mess=bot.send_message(message.chat.id,"Введите <b>русское</b> название акции. Название будет отображаться на кнопке, желаемая длина должна быть не более 20-ти символов. Очень рекомендуем использовать эмоджи, стикеры использовать нельзя",parse_mode='HTML',reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(mess,addAction22)
@fatallError
@Buttons(bot)
def addAction22(message):
                addAction22.ruName=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>украинское</b> название акции. Название будет отображаться на кнопке, желаемая длина должна быть не более 20-ти символов. Очень рекомендуем использовать эмоджи, стикеры использовать нельзя",parse_mode='HTML',reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(mess,addAction2)
@fatallError
@Buttons(bot)
def addAction2(message):
                addAction3.uaName=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>русское</b> описание акции. Описание не обязательно должно быть таким же как и на сайте.Рекомендуем кратко и лаконично описать акцию, а детальную механику можно посмотреть на сайте",parse_mode='HTML')
                bot.register_next_step_handler(mess,addAction33)
@fatallError
@Buttons(bot)
def addAction33(message):
                addAction33.ruDescription=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>украинское</b> описание акции. Описание не обязательно должно быть таким же как и на сайте.Рекомендуем кратко и лаконично описать акцию, а детальную механику можно посмотреть на сайте",parse_mode='HTML')
                bot.register_next_step_handler(mess,addAction3)                
@fatallError
@Buttons(bot)
def addAction3(message):
                addAction4.uaDescription= message.text
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
                f.write("{0};{1};{2};{3};{4};{5}\n".format(addAction22.ruName,addAction3.uaName,addAction33.ruDescription.replace('\n','\\n').replace(';',' '),addAction4.uaDescription.replace('\n','\\n').replace(';',' '),addAction5.link,message.text))

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(config.text['home'][bot.lang])
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
                                rez[i[0]]=(i[1],i[2],i[3],i[4],i[5])
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
                keyboard.add(*[types.KeyboardButton(name) for name in rez.keys()])
                keyboard.add(config.text['home'][bot.lang])
                mess=bot.send_message(message.chat.id,"Выберите акцию, которую хотите удалить",reply_markup=keyboard)
                deleteAction2.rez=rez
                bot.register_next_step_handler(mess,deleteAction2)
@fatallError
@Buttons(bot)
def deleteAction2(message):
                deleteAction3.mess=message.text
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
                keyboard.add(*[types.KeyboardButton(name) for name in ['Удалить',config.text['home'][bot.lang]]])
                bot.send_message(message.chat.id,"Вы собираетесь удалить акцию {0}".format(message.text))
                if len(deleteAction2.rez[message.text][2])>5:
                        bot.send_photo(message.chat.id,deleteAction2.rez[message.text][2])
                bot.send_message(message.chat.id,'<b>{0}</b>\n\n {1}'.format(message.text,str(deleteAction2.rez[message.text][1])),parse_mode='HTML')
                mess=bot.send_message(message.chat.id,'<b>Удалить?</b>',parse_mode='HTML',reply_markup=keyboard)
                bot.register_next_step_handler(mess,deleteAction3)
@fatallError
@Buttons(bot)
def deleteAction3(message):
        with open('files/actions.txt','w',encoding='utf-8') as f:
                for i in deleteAction2.rez.keys():
                        if  i!=deleteAction3.mess:
                            f.write("{0};{1};{2};{3};{4};{5}".format(i,deleteAction2.rez[i][0],deleteAction2.rez[i][1],deleteAction2.rez[i][2],deleteAction2.rez[i][3],deleteAction2.rez[i][4]))
        message.text='start'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(config.text['home'][bot.lang])
        bot.send_message(message.chat.id,'Акция успешно удалена',reply_markup=keyboard)
                
                
                
                

###############################################################        
@bot.message_handler(commands=["db"])
def db(message):
        pass
       # connectString = 'Driver={Oracle in OraHome92};Server=172.24.10.13:1600;DATABASE=KONTORA.BEZNAL.PARALLEL.UA;uid=PARALLEL_USER;pwd=S1mple_U5er'
        #dsn=  '(DESCRIPTION =(ADDRESS =(PROTOCOL = TCP)(HOST = 172.24.10.13)(PORT = 1600))(CONNECT_DATA = (SERVER = DEDICATED)(service_name = mainpr)))'
        #cnxn = pyodbc.connect(connectString)
       # conn = pyodbc.connect(
   # r'DRIVER={Oracle in OraHome92};'+
   # r'PROTOCOL = TCP;'+
   # r'SERVER=DEDICATED;'+
  #  r'HOST = 172.24.10.13;'+
   # r'PORT = 1600;'+
   # r'service_name = mainpr;'+
  #  r'DATABASE=KONTORA.BEZNAL.PARALLEL.UA;'+
  #  r'UID=PARALLEL_USER;'+
  #  r'PWD=S1mple_U5er'
  #  )
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

