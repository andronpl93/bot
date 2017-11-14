import config
import sys
from decorators import fatallError,Buttons,LangError
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
import re
from PIL import Image, ImageDraw, ImageFont
import os
import pickle
from config import NotComands
import fdb


try:
        con = fdb.connect(dsn='DB.FDB', user='SYSDBA', password='masterkey')
        cur=con.cursor()
        bot = telebot.TeleBot(config.token)
        language=config.fLang(cur,con)
except Exception:
	pass
tb={}
pr={}

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)



@bot.message_handler(commands=["start",config.text['home']['ua'][1:],config.text['home']['ru'][1:]])
@fatallError
def start(message):
    if message.text=='/start':
            global con, cur
            spaming.check(message.from_user.id,message.from_user.first_name,message.from_user.last_name,cur,con)
            selectLang.f=1
            selectLang(message)
            return 0
    try:
            if selectLang.f:
                    help(message)
                    return 0
    except AttributeError:
            pass
    f=open('files/stikers/logo.webp','rb')
    bot.send_sticker(message.chat.id,f)
    f.close()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textPrice'][language[str(message.from_user.id)]],config.text['textActions'][language[str(message.from_user.id)]],config.text['textBalance'][language[str(message.from_user.id)]]]])
    keyboard.add(*[types.KeyboardButton(name) for name in [config.text['contacts'][language[str(message.from_user.id)]],config.text['textLangSel'][language[str(message.from_user.id)]]]])
    bot.send_message(message.chat.id,'{1}, {0} '.format(message.chat.first_name,config.text['hello'][language[str(message.from_user.id)]])+u'\U0001F44B\n'+config.text['selInfo'][language[str(message.from_user.id)]],reply_markup=keyboard)
    botan.track(config.botan_key, message.chat.id, message, 'Старт')

###########################
@bot.message_handler(func=lambda m:m.text[:-1]==config.text['textLangSel']['ru'][:-1] or m.text[:-1]==config.text['textLangSel']['ua'][:-1])
@LangError
def selectLang(message):
        if message.text == config.text['textLangSel']['ru'][:-1] or message.text == config.text['textLangSel']['ua'][:-1]:
                selectLang.f=0
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textselL']['ua'],config.text['textselL']['ru']]])
        try:
                mess=bot.send_message(message.chat.id,config.text['textLang'][language[str(message.from_user.id)]],reply_markup=keyboard)
        except KeyError:
                mess=bot.send_message(message.chat.id,config.text['textLang']['ua'],reply_markup=keyboard)
        bot.register_next_step_handler(mess,selectLang2)

def selectLang2(message):
        if message.text not in config.text['textselL'].values():
                selectLang(message)
                return 0
        ret=[]

        global bot,language,cur,con
        try:
                language[str(message.from_user.id)]
                nou=0
        except KeyError:
                nou=1
        if message.text==config.text['textselL']['ua']:
                language[str(message.from_user.id)]='ua'
        else:
                        language[str(message.from_user.id)]='ru'
        if nou is not None:
                cur.execute("insert into lang (id_user,l) values ('{0}','{1}')".format(message.from_user.id,language[str(message.from_user.id)]))
        else:
              cur.executecute("update lang id_user='{0}',l='{1}' where id_user='{0}'".format(message.from_user.id,language[str(message.from_user.id)]))  
        con.commit()
        botan.track(config.botan_key, message.chat.id, message, "Язык - {0}".format(language[str(message.from_user.id)]))
        bot.send_message(message.chat.id,config.text['textLengEdit'][language[str(message.from_user.id)]])
        start(message)
##################################################################
@bot.message_handler(commands=["help"])
@fatallError
def help(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Ну ок")
        bot.send_message(message.chat.id,config.text['textHelp'][language[str(message.from_user.id)]][0],parse_mode='HTML')
        f=open('files/stikers/help.webp','rb')
        bot.send_sticker(message.chat.id,f)
        f.close()
        mess=bot.send_message(message.chat.id,config.text['textHelp'][language[str(message.from_user.id)]][1],reply_markup=keyboard,parse_mode='HTML')
        selectLang.f=0
        bot.register_next_step_handler(mess,lambda x: start(message))
        
############################################################
@bot.message_handler(func=lambda m:m.text[:4]==config.text['textPrice']['ru'][:-1] or m.text[:4]==config.text['textPrice']['ua'][:-1])
@fatallError
def price(message):
        global dataPrice
        with open('files/data.dat', 'rb') as f:
                unpickler = pickle.Unpickler(f)
                dataPrice = unpickler.load()
        obl=list(dataPrice[language[str(message.from_user.id)]])
        if not len(obl):
               bot.send_message(message.chat.id,config.text['verySorry'][language[str(message.from_user.id)]],reply_markup=types.ReplyKeyboardRemove())
               start(message)
               return  0
        fObl.obl=obl
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        a = login.findLoveCity(message.from_user.id,language[str(message.from_user.id)],cur)
        if len(a)!=0:
                cobl=config.text['selectAreaOrCity'][language[str(message.from_user.id)]]
                keyboard.add(*[types.KeyboardButton(name+u'\U0001F31F') for name in a])
                fCity.lov=a
        else:
                fCity.lov=[]
                cobl=config.text['selectArea'][language[str(message.from_user.id)]]

        fObl.comands=obl[:]#
        fObl.comands.extend(a)#
        
        keyboard.add(*[types.KeyboardButton(name) for name in obl[:2]])
        keyboard.add(*[types.KeyboardButton(name) for name in obl[2:]])
        keyboard.add(types.KeyboardButton(config.text['home'][language[str(message.from_user.id)]]))
        obl = bot.send_message(message.chat.id, cobl,
                reply_markup=keyboard)

        bot.register_next_step_handler(obl,fObl)
        botan.track(config.botan_key, message.chat.id, message, 'Цена')
        
@fatallError
@Buttons(bot,language)
def fObl(message):
        message.text=str(message.text).translate(non_bmp_map)[-1]=='�' and str(message.text).translate(non_bmp_map)[:-1]or str(message.text).translate(non_bmp_map)  
        if message.text not in fObl.comands:
                raise NotComands
        
        if message.text not in fObl.obl:
                for i in dataPrice[language[str(message.from_user.id)]]:
                        if message.text in dataPrice[language[str(message.from_user.id)]][i]:
                                fObl.obl=i
                                break
                fCity.comands=[message.text]       
                fCity.d=message.text
                fCity.l=0
                fCity(message)
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                a=list(dataPrice[language[str(message.from_user.id)]][message.text])
                if not len(a):
                       bot.send_message(message.chat.id,config.text['verySorry'][language[str(message.from_user.id)]],reply_markup=types.ReplyKeyboardRemove())
                       start(message)
                       return  0
                
                fCity.comands=a[:]#
                
                keyboard.add(*[types.KeyboardButton(str(name)) for name in a])
                keyboard.add(types.KeyboardButton(config.text['home'][language[str(message.from_user.id)]]))
                city = bot.send_message(message.chat.id, config.text['textCity'][language[str(message.from_user.id)]],
                        reply_markup=keyboard)
                fCity.d=a
                fObl.obl=message.text
                fCity.l=1
                bot.register_next_step_handler(city,fCity)
                botan.track(config.botan_key, message.chat.id, message, message.text)
@fatallError
@Buttons(bot,language)
def fCity(message):
                if message.text not in fCity.comands:
                        raise NotComands
                global pr,tb
                if fCity.l:
                        nameCity=message.text
                else:
                        nameCity=fCity.d
                pr['nameCity']=nameCity
                a1='{0}{1}{2}{3}{4}{5}'.format(*[str(j).replace('.','').replace(' ','-') for j in dataPrice[language[str(message.from_user.id)]][fObl.obl][nameCity][0][1:]])      

                keyboard = types.InlineKeyboardMarkup()
                if len(dataPrice[language[str(message.from_user.id)]][fObl.obl][nameCity])>1:
                        keyboard.add(*[types.InlineKeyboardButton(text=i,callback_data=str(i))
                                       for i in range(1,len(dataPrice[language[str(message.from_user.id)]][fObl.obl][nameCity])+1)])
                a=config.dMaps(nameCity,language[str(message.from_user.id)])
                if a is not None:
                       keyboard.add(*[types.InlineKeyboardButton(text=config.text['showMap'][language[str(message.from_user.id)]],url=a)])
                azs = bot.send_message(message.chat.id, '\n'.join("<b>{0}</b>. {1}".format(str(i+1),j[0])
                        for i,j in enumerate(dataPrice[language[str(message.from_user.id)]][fObl.obl][nameCity])),parse_mode='HTML',reply_markup=keyboard)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if message.text not in fCity.lov:
                        save_or_del=config.text['saveLoveCity'][language[str(message.from_user.id)]]
                else:
                        save_or_del=config.text['delLoveCity'][language[str(message.from_user.id)]]

                keyboard.add(*[types.KeyboardButton(name) for name in [config.text['home'][language[str(message.from_user.id)]],save_or_del]])
                pr['k']=keyboard
                if len(dataPrice[language[str(message.from_user.id)]][fObl.obl][nameCity])==1:
                        f=open('price/{0}.webp'.format(a1),'rb')
                        pr['t']=bot.send_sticker(message.chat.id,f,reply_markup=keyboard)
                        f.close()
                else:
                        pr['t'] = bot.send_message(message.chat.id,'<b>{0}</b>'.
                                                   format(config.text['selAZS'][language[str(message.from_user.id)]]),parse_mode='HTML',reply_markup=keyboard)
                fCity.mes=message
                fCity.city=message.text
                botan.track(config.botan_key, message.chat.id, message, message.text)


@bot.message_handler(func=lambda m:m.text==config.text['saveLoveCity']['ru'] or m.text==config.text['saveLoveCity']['ua'] or m.text==config.text['delLoveCity']['ua'] or m.text==config.text['delLoveCity']['ru'])        
@Buttons(bot,language)
def saveCity(message):
        global cur,con
        try:
                fCity.city
        except AttributeError:
                return 0
        if message.text==config.text['saveLoveCity'][language[str(message.from_user.id)]]:
                cur.execute("insert into savecity (id_user,city,l) values('{0}','{1}','{2}')".format(fCity.mes.from_user.id,fCity.city,language[str(message.from_user.id)]))               
        else:
              cur.execute("delete from savecity where id_user='{0}' and city='{1}' and l='{2}'".format(fCity.mes.from_user.id,fCity.city,language[str(message.from_user.id)]))  
        con.commit()
        botan.track(config.botan_key, message.chat.id, message, "Сохранил город - {0}".format(fCity.city))
        start(message)
        
@bot.callback_query_handler(func=lambda c: c.data)
@fatallError
def pages(c):
        global pr
        try:
                int(c.data)
        except ValueError:
                return
        try:
                bot.delete_message(pr['t'].chat.id,pr['t'].message_id)
        except KeyError:
                pass
        try:
                f=open('price/{0}{1}{2}{3}{4}{5}.webp'.format
                       (*[str(j).replace('.','').replace(' ','-') for j in dataPrice['ru'][fObl.obl][pr['nameCity']][int(c.data)-1][1:]]),'rb')
        except KeyError:
                f=open('price/{0}{1}{2}{3}{4}{5}.webp'.format
                       (*[str(j).replace('.','').replace(' ','-') for j in dataPrice['ua'][fObl.obl][pr['nameCity']][int(c.data)-1][1:]]),'rb')
        pr['t'] = bot.send_sticker(pr['t'].chat.id,f,reply_markup=pr['k'])
        f.close()




#########################################
def balanceStiker(message,log,bal,k):
        sB=85
        H=230
        fnt24 = ImageFont.truetype('files/stikers/tnr.ttf', sB)
        fnt14 = ImageFont.truetype('files/stikers/tnr.ttf', 50)
        f=Image.open('files/stikers/balance{0}{1}.png'.format(log[0]=='0' and 'KB' or 'MB',language[str(message.from_user.id)]))
        d = ImageDraw.Draw(f)
        w, h = d.textsize(str(bal))

        x=(12-len(str(bal)))
        d.text((x*(sB)-(x*sB)/1.5,109.5), str(bal), font=fnt24, fill=(255,255,255,255))
        if len(log)==10:
                x=log[:4]+' '+log[4:10]
                d.text((215,265), x, font=fnt14, fill=(255,255,255,255))
        else:
              x=log[:4]+' '+log[4:8]
              d.text((264,265), x, font=fnt14, fill=(255,255,255,255))
        f.save('files/stikers/{0}.webp'.format(message.from_user.id),'WEBP')
        f=open('files/stikers/{0}.webp'.format(message.from_user.id),'rb')
        mess=bot.send_sticker(message.chat.id,f,reply_markup=k)
        f.close()
        os.remove('files/stikers/{0}.webp'.format(message.from_user.id))
        return mess
        

@bot.message_handler(func=lambda m:m.text[:15]==config.text['textBalance']['ru'][:-1] or m.text[:15]==config.text['textBalance']['ua'][:-1])
@fatallError
def balance(message):
        card=login.findCard(message.from_user.id,cur)
        if len(card)==0:
                message.text=config.text['textAddCard'][language[str(message.from_user.id)]]
                nomCard.comands=message.text
                nomCard(message)  
        else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if len(card)==1:
                        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textLogOut'][language[str(message.from_user.id)]],config.text['textAddCard'][language[str(message.from_user.id)]],config.text['home'][language[str(message.from_user.id)]]]])
                        nomCard.x=[config.text['textLogOut'][language[str(message.from_user.id)]],config.text['textAddCard'][language[str(message.from_user.id)]],config.text['home'][language[str(message.from_user.id)]]]
                        messDel=bot.send_message(message.chat.id,config.text['textWait'][language[str(message.from_user.id)]])
                        a=login.req(card[0][1],card[0][2],language[str(message.from_user.id)])
                        if a[1][1]=='KB' or a[1][1]=='MB' :
                                f=open('files/stikers/ban{0}.webp'.format(a[1][1]),'rb')
                                bot.send_sticker(message.chat.id,f)
                                f.close()
                                bot.send_message(message.chat.id,config.text['textBan'][language[str(message.from_user.id)]].format(a[1][0]),parse_mode='HTML')
                                mess=bot.send_contact(message.chat.id,'+380800503333',config.text['textContactHotLine'][language[str(message.from_user.id)]],reply_markup=keyboard)
                        else:
                                mess=balanceStiker(message,a[1][0],a[1][1],keyboard)
                        nomCard.comands=[config.text['textLogOut'][language[str(message.from_user.id)]],config.text['textAddCard'][language[str(message.from_user.id)]]]
                        bot.delete_message(message.chat.id,messDel.message_id)
                        nomCard.loginn=card[0][1]
                        bot.register_next_step_handler(mess,nomCard)
                else:
                        keyboard.add(*[types.KeyboardButton(name[1]) for name in card])
                        keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textAddCard'][language[str(message.from_user.id)]],config.text['home'][language[str(message.from_user.id)]]]])

                        choiceCard.comands=list(map(lambda y: y[1],card))#Костыли для защиты от ввоода говнища
                        choiceCard.comands.extend([config.text['textAddCard'][language[str(message.from_user.id)]],config.text['home'][language[str(message.from_user.id)]]])

                        mess=bot.send_message(message.chat.id, config.text['textSelCard'][language[str(message.from_user.id)]],reply_markup=keyboard)   
                        bot.register_next_step_handler(mess,choiceCard)
                
        botan.track(config.botan_key, message.chat.id, message, u'Баланс')


@fatallError
@Buttons(bot,language)
def nomCard(message):
        if message.text not in nomCard.comands:
                raise NotComands
        global con
        if message.text!=config.text['textLogOut'][language[str(message.from_user.id)]]:
                @Buttons(bot,language)
                def logC(message):
                        if  message.text in [config.text['home'][language[str(message.from_user.id)]],'/start']:
                                return 0
                        log=message.text
                        @Buttons(bot,language)
                        def pas(message):
                                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                keyboard.add(config.text['home'][language[str(message.from_user.id)]])
                                pas=message.text
                                messDel=bot.send_message(message.chat.id,config.text['textWait'][language[str(message.from_user.id)]])
                                a=login.req(log,pas,language[str(message.from_user.id)])
                                
                                if a[0]:
                                        if  a[1][1]=='KB' or a[1][1]=='MB' :
                                                f=open('files/stikers/ban{0}.webp'.format(a[1][1]),'rb')
                                                bot.send_sticker(message.chat.id,f)
                                                f.close()
                                                bot.send_message(message.chat.id,config.text['textBan'][language[str(message.from_user.id)]].format(a[1][0]),parse_mode='HTML')
                                                bot.send_contact(message.chat.id,'+380800503333',config.text['textContactHotLine'][language[str(message.from_user.id)]])
                                        else:
                                                balanceStiker(message,a[1][0],a[1][1],keyboard)
                                        
                                if a[0]:
                                        if login.findCard(message.from_user.id,cur,log,s=False)!=0:
                                                login.writeCard(message.from_user.id,log,pas,cur,con)
                                                bot.send_message(message.chat.id, config.text['textCardSave'][language[str(message.from_user.id)]],reply_markup=keyboard)
                                        else:
                                                bot.send_message(message.chat.id, config.text['textCardIn'][language[str(message.from_user.id)]],reply_markup=keyboard) 
                                else:
                                        bot.send_message(message.chat.id,config.text['textCardNot'][language[str(message.from_user.id)]]+"\n"+config.text['textTelCardError'][language[str(message.from_user.id)]])
                                        mess=bot.send_message(message.chat.id, u'{1} {0}'.format(config.text['home'][language[str(message.from_user.id)]],config.text['textPop'][language[str(message.from_user.id)]]),reply_markup=keyboard)
                                        bot.register_next_step_handler(mess,logC)
                                bot.delete_message(message.chat.id,messDel.message_id)
                        mess=bot.send_message(message.chat.id, config.text['textInPass'][language[str(message.from_user.id)]],reply_markup=keyboard)
                        bot.register_next_step_handler(mess,pas)
                        
                ###############keyboard = types.ReplyKeyboardRemove()
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(config.text['home'][language[str(message.from_user.id)]])
                mess=bot.send_message(message.chat.id,config.text['textInCard'][language[str(message.from_user.id)]],reply_markup=keyboard)
                bot.register_next_step_handler(mess,logC)
        else:
                login.logOut(message.from_user.id,nomCard.loginn,cur,con)
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, config.text['textCardDel'][language[str(message.from_user.id)]],reply_markup=keyboard)
                start(message)
                botan.track(config.botan_key, message.chat.id, message, config.text['textLogOut'][language[str(message.from_user.id)]])
                                                                                                                                                            
@fatallError
@Buttons(bot,language)
def choiceCard(message):
        if message.text not in choiceCard.comands:
                raise NotComands
        
        if message.text==config.text['textAddCard'][language[str(message.from_user.id)]]:
                nomCard.comands=[config.text['textAddCard'][language[str(message.from_user.id)]]]
                nomCard(message)
        else:
                card=login.findCard(message.from_user.id,cur,message.text)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in [config.text['textLogOut'][language[str(message.from_user.id)]],config.text['textAddCard'][language[str(message.from_user.id)]],config.text['home'][language[str(message.from_user.id)]]]])
                messDel=bot.send_message(message.chat.id,config.text['textWait'][language[str(message.from_user.id)]])
                a=login.req(card[0][1],card[0][2],language[str(message.from_user.id)])
                
                if a[1][1]=='KB' or a[1][1]=='MB' :
                        f=open('files/stikers/ban{0}.webp'.format(a[1][1]),'rb')
                        bot.send_sticker(message.chat.id,f)
                        f.close()
                        bot.send_message(message.chat.id,config.text['textBan'][language[str(message.from_user.id)]].format(a[1][0]),parse_mode='HTML')
                        mess=bot.send_contact(message.chat.id,'+380800503333',config.text['textContactHotLine'][language[str(message.from_user.id)]],reply_markup=keyboard)
                        
                else:
                        mess=balanceStiker(message,a[1][0],a[1][1],keyboard)
                nomCard.comands=[config.text['textLogOut'][language[str(message.from_user.id)]],config.text['textAddCard'][language[str(message.from_user.id)]]]
                bot.delete_message(message.chat.id,messDel.message_id)
                nomCard.loginn=card[0][1]
                bot.register_next_step_handler(mess,nomCard)

###################
@bot.message_handler(func=lambda m:m.text[:-1]==config.text['contacts']['ru'][:-1] or m.text[:-1]==config.text['contacts']['ua'][:-1])
@fatallError
def contacts(message):
        keyboard = types.InlineKeyboardMarkup()
        for i in config.contactsLink:
                keyboard.add(types.InlineKeyboardButton(text=i[language[str(message.from_user.id)]][0],url=i[language[str(message.from_user.id)]][1]))
        for i in config.contactsText[:-1]:
                bot.send_message(message.chat.id,i[language[str(message.from_user.id)]])
        else:
                bot.send_message(message.chat.id,config.contactsText[-1][language[str(message.from_user.id)]],reply_markup=keyboard)

##############################spam
isOdmenSpam=0
dataSpam=0
k2= types.ReplyKeyboardMarkup(resize_keyboard=True)
@bot.message_handler(commands=["spaming"])
def spam(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeni.txt'):
                global isOdmenSpam,dataSpam,k2
                isOdmenSpam=1
                k2= types.ReplyKeyboardMarkup(resize_keyboard=True)
                dataSpam={}
                k2.add(*[types.KeyboardButton(name) for name in ['[Получатель]','[Русское описание]','[Украинское описание]']])
                k2.add('[Проверить]')
                k2.add(config.text['home']['ru'])
                bot.send_message(message.chat.id, 'Дороу',reply_markup=k2)
        else:
                bot.send_message(message.chat.id, 'Данная функция доступна только Одмену',reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m:m.text=='[Получатель]')
def spamFile(message):
        if isOdmenSpam:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in ['Все пользователи телеграм','Карты КБ','Карты МБ']])
                text = bot.send_message(message.chat.id, 'Выберите получателя или введите ссылку на файл(в файле первым должен идти id) (прим. files/text.txt)',reply_markup=keyboard)
                bot.register_next_step_handler(text,spamFile2)
def spamFile2(message):
        global dataSpam
        dataSpam['people']={}
        dataSpam['komu']=message.text
        dataSpam['peopleLang']={}
        with open('files/lang.txt','r') as f:
                for i in f:
                        i=i.split(';')
                        dataSpam['peopleLang'][i[0]]=i[1][:-1]
        if  message.text=="Все пользователи телеграм":
                
                for i in dataSpam['peopleLang']:
                        dataSpam['people'][i]=dataSpam['peopleLang'][i]
        else:
                if message.text=="Карты КБ" or message.text=="Карты МБ":
                        if message.text=="Карты КБ":
                                a=0
                        else:
                                a=9
                        with open('files/AllCard.txt','r') as f:
                                for i in f:
                                        i=i.split(';')
                                        if i[1][0]==str(a):
                                                dataSpam['people'][i[0]]='ua'
                else:
                        try:
                                with open(message.text,'r') as f:
                                        for i in f:
                                                i=i.split(';')
                                                if i[0][-1]=='\n':
                                                        i[0]=i[0][:-1]
                                                dataSpam['people'][i[0]]='ua'
                        except FileNotFoundError:
                                bot.send_message(message.chat.id, 'Файл который вы ввели не нашелся',reply_markup=k2)
                for i in dataSpam['people']:
                        try:
                                dataSpam['people'][i]=dataSpam['peopleLang'][i]
                        except KeyError:
                                dataSpam['people'][i]='ua'
        bot.send_message(message.chat.id, 'ok',reply_markup=k2)
        
@bot.message_handler(func=lambda m:m.text=='[Русское описание]' or m.text=='[Украинское описание]')
def spamText(message):
        if isOdmenSpam:
                text = bot.send_message(message.chat.id, """Введите {0} \n
Чтобы текст был жирным используйте <b> жирный</b> 
Чтобы текст был курсивом используйте <em>курсив</em> 
Чтобы вставить картинку использусте следующий шаблон <g>url.jpg Описание</g> где  url.jpg это ссылка на картинку, можно использовать gif png jpg
Чтобы вставить стикер используйте <st>path</st> где path это путь к картинке, которую вы УЖЕ положили в папку(прим. files/img/pick.png)
Собственно, в чем соль: Картинка будет грузится на устройство пользователя, если у человека мобильный интернет, то ему вряд ли понравится
что вы выкачали его трафик.Стикер в свою очередь трафика выкачает очень мало. НО стикер сам по себе очень маленький, так что если у вас там
много текста, то он будет нечитаемым, кароч, смотрите по ситуации
НЕЛЬЗЯ делать текст одновременно жирным и курсивом! НЕЛЬЗЯ вкладывать жирный и курсивный текст в описание картинки
                """.format(message.text),reply_markup=types.ReplyKeyboardRemove())
                spamText2.l=message.text
                bot.register_next_step_handler(text,spamText2)
def spamText2(message):
        global dataSpam
        if spamText2.l=='[Русское описание]':
                dataSpam['ruText']=message.text
        else:
                dataSpam['uaText']=message.text
        bot.send_message(message.chat.id, 'ok',reply_markup=k2)
                
@bot.message_handler(func=lambda m:m.text=='[Проверить]')
def excample(message):
        if len(dataSpam)<5:
                bot.send_message(message.chat.id, 'Что ты проверять собрался? Сначала заполни: {0} {1} {2}'.format('people' not in dataSpam and 'Получателей;' or '','ruText'  not in dataSpam and 'Русское описание;' or '','uaText' not in dataSpam and 'Украинское описание;' or ''),reply_markup=k2)
        else:
                bot.send_message(message.chat.id, '<b>Вы собираетесь отправить {0}, \n это сообщение:</b>'.format(dataSpam['komu']),parse_mode='HTML')
                excample2.textsRu=re.split(r'[\s]*?(<g>.*?</g>)[\s]*?|[\s]*?(<st>.*?</st>)[\s]*?',dataSpam['ruText'],re.DOTALL)
                excample2.textsUa=re.split(r'[\s]*?(<g>.*?</g>)[\s]*?|[\s]*?(<st>.*?</st>)[\s]*?',dataSpam['uaText'],re.DOTALL)

                k= types.ReplyKeyboardMarkup(resize_keyboard=True)
                k.add(*[types.KeyboardButton(name) for name in ['[Получатель]','[Русское описание]','[Украинское описание]',config.text['home']['ru']]])
                k.add('[Отправить тестовой группе]')
                k.add('[Отправить!!!]')
                push(message.from_user.id,excample2.textsRu,1)
                bot.send_message(message.chat.id, '<b>И украинская версия:</b>',parse_mode='HTML')
                push(message.from_user.id,excample2.textsUa,1)
                mess=bot.send_message(message.chat.id, '<b>Пришло время выбирать</b>',parse_mode='HTML',reply_markup=k)
                bot.register_next_step_handler(mess,excample2)
                
                
def excample2(message):
        if message.text in ['[Получатель]','[Русское описание]','[Украинское описание]',config.text['home']['ru']]:
                return 0
        else:
                if message.text=='[Отправить тестовой группе]':
                        dataTest={}
                        with open('files/people/test.txt','r') as f:
                                for i in f:
                                        dataTest[i[:-1]]='ua'
                        for i in dataTest:
                                        try:
                                                dataTest[i]=dataSpam['peopleLang'][i]
                                        except KeyError:
                                                dataTest[i]='ua'
                        for i in dataTest:
                                        if dataTest[i]=='ru':
                                               push(i,excample2.textsRu,1)
                                        else:
                                                push(i,excample2.textsUa,1)
                        k= types.ReplyKeyboardMarkup(resize_keyboard=True)
                        k.add(*[types.KeyboardButton(name) for name in ['[Получатель]','[Русское описание]','[Украинское описание]',config.text['home']['ru']]])
                        k.add('[Отправить!!!]')
                        mess=bot.send_message(message.chat.id, '<b>Пришло время выбирать</b>',parse_mode='HTML',reply_markup=k)
                        bot.register_next_step_handler(mess,excample2)
                else:
                        if message.text=='[Отправить!!!]':
                                
                                for i in dataSpam['people']:
                                        if dataSpam['people'][i]=='ru':
                                               push(i,excample2.textsRu,0)
                                        else:
                                                push(i,excample2.textsUa,0)
                        bot.send_message(message.chat.id, 'Сообщение отправленно',parse_mode='HTML')
                        start(message)
                                

def push(id,text,test):
        for i in text:
                if i is not None and len(i)>0:
                        if i[:3]=='<g>':
                                try:
                                        murl=re.search(r'(http.*?jpg|http.*?png|http.*?gif)',i).group(0)
                                        desc=i.replace(murl,'').replace('<g>','').replace('</g>','')
                                        if desc:
                                                bot.send_photo(id,murl,desc)
                                        else:
                                                bot.send_photo(id,murl)
                                except Exception:
                                        if test:
                                                bot.send_message(id,'С картинкой что-то не так')
                        else:
                                if i[:4]=='<st>':
                                        try:
                                                murl=re.search(r'(.*?jpg|.*?png|.*?gif)',i).group(0).replace('<st>','')
                                                f=Image.open(murl)
                                                d = ImageDraw.Draw(f)
                                                murl=murl.replace('.','')
                                                f.save('files/{0}.webp'.format(murl),'WEBP')
                                                f=open('files/{0}.webp'.format(murl),'rb')
                                                mess=bot.send_sticker(id,f)
                                                f.close()
                                                os.remove('files/{0}.webp'.format(murl))
                                        except Exception:
                                                if test:
                                                        bot.send_message(id,'Со стикером что-то пошло не так')
                                else:
                                        try:
                                                bot.send_message(id,i,parse_mode='HTML')
                                        except Exception:
                                                if test:
                                                        bot.send_message(id,"С текстом что-то не так",parse_mode='HTML')
        
                


#########################################################################
@bot.message_handler(func=lambda m:m.text[:5]==config.text['textActions']['ru'][:-1] or m.text[:5]==config.text['textActions']['ua'][:-1])
@fatallError
def actions(message):      
        rez={}
        with open('files/actions.txt','r',encoding='utf-8') as f:
                for i in f:
                        i=i.split(';')
                        if language[str(message.from_user.id)]=='ru':
                                rez[i[0]]=(str(i[2]).replace('\\n','\n'),str(i[4]))
                        else:
                               rez[i[1]]=(str(i[3]).replace('\\n','\n'),str(i[4]))
        if len(rez)==0:
                bot.send_message(message.chat.id,config.text['textNotActions'][language[str(message.from_user.id)]])
                return 0
        long1=[]
        long2=[]
        short=[]
        action.comands=list(rez.keys())[:]
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
        keyboard.add(config.text['home'][language[str(message.from_user.id)]])
        mess=bot.send_message(message.chat.id,config.text['changeAction'][language[str(message.from_user.id)]],reply_markup=keyboard)
        action.rez=rez
        action.mess=mess
        botan.track(config.botan_key, message.chat.id, message, 'Акции')
        bot.register_next_step_handler(mess,action)
        
        
@Buttons(bot,language)
def action(message):
        if message.text not in action.comands:
                        raise NotComands
        imgs=re.findall(r'<g>[\s]*?(http.*?jpg.*?|http.*?png.*?|http.*?gif.*?)</g>',action.rez[message.text][0],re.DOTALL)
        texts=re.split(r'[\s]*?<g>.*?</g>[\s]*?',action.rez[message.text][0],re.DOTALL)
        keyboard=types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=config.text['textMoreInfo'][language[str(message.from_user.id)]],url=action.rez[message.text][1][:18]+str(language[str(message.from_user.id)]=='ua' and '/uk' or '')+action.rez[message.text][1][18:])]) 
 
        bot.send_message(message.chat.id,'<b>{0}</b>'.format(message.text),parse_mode='HTML')
        for i in range(len(imgs)):
                if len(texts[i])!=0:
                        bot.send_message(message.chat.id,str(texts[i]),parse_mode='HTML')
                murl=re.search(r'(http.*?jpg|http.*?png|http.*?gif)',imgs[i]).group(0)
                desc=imgs[i].replace(murl,'')
                if texts[-1]=="" and i+1==len(imgs):
                        mess=bot.send_photo(message.chat.id,murl,desc,reply_markup=keyboard)
                        break
                else:
                        bot.send_photo(message.chat.id,murl,desc)
        else:
                mes=bot.send_message(message.chat.id,texts[-1],reply_markup=keyboard)
        botan.track(config.botan_key, message.chat.id, message,"Акции:"+str(message.text))
        bot.register_next_step_handler(action.mess,action)

##
@bot.message_handler(commands=["addAction"])
@fatallError
@Buttons(bot,language)
def addAction(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeniAction.txt'):
                mess=bot.send_message(message.chat.id,"Введите <b>русское</b> название акции. Название будет отображаться на кнопке, желаемая длина должна быть не более 20-ти символов. Очень рекомендуем использовать эмоджи, стикеры использовать нельзя",parse_mode='HTML',reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(mess,addAction22)
@fatallError
@Buttons(bot,language)
def addAction22(message):
                addAction22.ruName=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>украинское</b> название акции. Название будет отображаться на кнопке, желаемая длина должна быть не более 20-ти символов. Очень рекомендуем использовать эмоджи, стикеры использовать нельзя",parse_mode='HTML',reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(mess,addAction2)
@fatallError
@Buttons(bot,language)
def addAction2(message):
                addAction2.uaName=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>русское</b> описание акции. Описание не обязательно должно быть таким же как и на сайте.Рекомендуем кратко и лаконично описать акцию, а детальную механику можно посмотреть на сайте",parse_mode='HTML')
                bot.register_next_step_handler(mess,addAction33)
@fatallError
@Buttons(bot,language)
def addAction33(message):
                addAction33.ruDescription=message.text
                mess=bot.send_message(message.chat.id,"Введите <b>украинское</b> описание акции. Описание не обязательно должно быть таким же как и на сайте.Рекомендуем кратко и лаконично описать акцию, а детальную механику можно посмотреть на сайте",parse_mode='HTML')
                bot.register_next_step_handler(mess,addAction3)                
@fatallError
@Buttons(bot,language)
def addAction3(message):
                addAction3.uaDescription= message.text
                mess=bot.send_message(message.chat.id,"Введите ссылку на <b>русскую</b> версию акции, на сайте parallel.ua",parse_mode='HTML')
                bot.register_next_step_handler(mess,addAction5)
@fatallError
@Buttons(bot,language)
def addAction5(message):
        with open('files/actions.txt','a',encoding='utf-8') as f:
                f.write("{0};{1};{2};{3};{4}\n".format(addAction22.ruName,addAction2.uaName,addAction33.ruDescription.replace('\n','\\n').replace(';',' '),addAction3.uaDescription.replace('\n','\\n').replace(';',' '),message.text))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(config.text['home'][language[str(message.from_user.id)]])
        bot.send_message(message.chat.id,'Акция успешно добавлена',reply_markup=keyboard)
                
##
@bot.message_handler(commands=["deleteAction"])
@fatallError
@Buttons(bot,language)
def deleteAction(message):
        if spaming.isOdmen(message.chat.id,'files/people/odmeniAction.txt'):
                rez={}
                with open('files/actions.txt','r',encoding='utf-8') as f:
                        for i in f:
                                i=i.split(';')
                                rez[i[0]]=(i[1],str(i[2]).replace('\\n','\n'),str(i[3]).replace('\\n','\n'),i[4])
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
                keyboard.add(*[types.KeyboardButton(name) for name in rez.keys()])
                keyboard.add(config.text['home'][language[str(message.from_user.id)]])
                mess=bot.send_message(message.chat.id,"Выберите акцию, которую хотите удалить",reply_markup=keyboard)
                deleteAction2.rez=rez
                bot.register_next_step_handler(mess,deleteAction2)
@fatallError
def deleteAction2(message):
                deleteAction3.mess=message.text
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in ['Удалить',config.text['home'][language[str(message.from_user.id)]]]])
                bot.send_message(message.chat.id,"Вы собираетесь удалить акцию {0}".format(message.text))
                imgs=re.findall(r'<g>[\s]*?(http.*?jpg.*?|http.*?png.*?|http.*?gif.*?)</g>',deleteAction2.rez[message.text][1+int(language[str(message.from_user.id)]=='ua' and 1 or 0)],re.DOTALL)
                texts=re.split(r'[\s]*?<g>.*?</g>[\s]*?',deleteAction2.rez[message.text][1+int(language[str(message.from_user.id)]=='ua' and 1 or 0)],re.DOTALL)
                bot.send_message(message.chat.id,'<b>{0}</b>'.format(message.text),parse_mode='HTML')
                for i in range(len(imgs)):
                        if len(texts[i])!=0:
                                bot.send_message(message.chat.id,str(texts[i]),parse_mode='HTML')
                        murl=re.search(r'(http.*?jpg|http.*?png|http.*?gif)',imgs[i]).group(0)
                        desc=imgs[i].replace(murl,'')
                        if texts[-1]=="" and i+1==len(imgs):
                                mess=bot.send_photo(message.chat.id,murl,desc)
                                break
                        else:
                                bot.send_photo(message.chat.id,murl,desc)
                else:
                        mes=bot.send_message(message.chat.id,texts[-1])
                mess=bot.send_message(message.chat.id,'<b>Удалить?</b>',parse_mode='HTML',reply_markup=keyboard)
                bot.register_next_step_handler(mess,deleteAction3)
@fatallError
@Buttons(bot,language)
def deleteAction3(message):
        with open('files/actions.txt','w',encoding='utf-8') as f:
                for i in deleteAction2.rez.keys():
                        if  i!=deleteAction3.mess:
                            f.write("{0};{1};{2};{3};{4}".format(i,deleteAction2.rez[i][0],deleteAction2.rez[i][1],deleteAction2.rez[i][2],deleteAction2.rez[i][3]))
        message.text='start'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)     
        keyboard.add(config.text['home'][language[str(message.from_user.id)]])
        bot.send_message(message.chat.id,'Акция успешно удалена',reply_markup=keyboard)
                
                


                
a=0
###############################################################        
@bot.message_handler(commands=["db"])
def db(message):
        global con, cur
        cur.execute("select * from allpeople;")
  #      cur.execute("CREATE SEQUENCE login_id_sequence;")
 #       cur.execute("""CREATE TRIGGER login_AUTOINCREMENT FOR login
#ACTIVE BEFORE INSERT POSITION 0
#AS
#BEGIN
#  NEW.ID = next value for login_id_sequence;
#END""")
        #con.commit()
        print(cur.fetchall())
       # row = cursor.fetchone()
        #if row:
        #    
        
        #f=Image.open('help.png')
        
        #f.save('help.webp','WEBP')
       # f=open('ava.webp','rb')
       # x=bot.send_sticker(message.chat.id,f)
        print(2)


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

