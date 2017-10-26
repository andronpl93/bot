import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs

lang='ru'
token= "449516678:AAG-3WuJMd6bmJMY5gSmow7BQZZe1qb3nHw"
botan_key = "ced7eedf-3482-4f6a-bc62-1cba635cdbd4"
text={
	'textselL':{'ru':'Русский','ua':'Українська'},
	'textLengEdit':{'ru':'Язык успешно изменен','ua':'Мова успiшно змінена'},
	'textLang':{'ru':'Выберите язык общения🗣','ua':'Оберіть мову спілкування🗣'},
	'textLangSel':{'ru':'Изменить язык🗣','ua':'Змінити мову🗣'},
	'textMoreInfo':{'ru':'Детальная информация на сайте','ua':'Детальна інформація на сайті'},
	'textNotActions':{'ru':'На данный момент нет активных акций','ua':'На даний момент немає активних акцій'},
	'textCardDel':{'ru':'Карта была удалена','ua':'Карта була видалена'},
	'textInCard':{'ru':'Введите номер каты','ua':'Введіть номер карти'},
	'textInPass':{'ru':'Введите пароль','ua':'Введіть пароль'},
	'textPop':{'ru':'Введите номер карты чтобы попробовать еще раз или нажмите ','ua':'Введіть номер карти щоб спробувати ще раз або натисніть '},
	'textTelCardError':{'ru':u'Телефон горячей линии (бесплатный с мобильных и стационарных телефонов):\n +380800503333','ua':'Телефон горячої лініі (безкоштовний з мобільних та стаціонарних телефонів):\n +380800503333'},
	'textCardIn':{'ru':'Данная карта уже зарегистрирована','ua':'Ця карта вже зареэстрована'},
	'textCardSave':{'ru':'Карта сохранена','ua':'Карта збережена'},
	'textSelCard':{'ru':"Выберите карту",'ua':'Оберіть карту'},
	'textLogOut':{'ru':'Разлогинить','ua':'Разлогинить'},
	'textAddCard':{'ru':"Добавить карту",'ua':'Додати карту'},
	'hoteLine':{'ru':'Горячая линия','ua':'Горяча лінія'},
	'selAZS':{'ru':'Выберите АЗС','ua':'Оберіть АЗС'},
	'textCity':{'ru':'Город','ua':'Місто'},
	'selInfo':{'ru': 'Выберите интересующую информацию','ua':'Оберіть цікаву для вас інформацію'},
	'textActions':{'ru':'Акции'+u"\U00002728",'ua':'Акції'+u"\U00002728"},
	'textBalance':{'ru':u'Баланс на карте'+u'\U0001F4B3','ua':u'Баланс на карті'+u'\U0001F4B3'},
	'textPrice':{'ru':u'Цены'+u'\U0001F4B9','ua':'Ціни'+u'\U0001F4B9'},
	'hello':{'ru':'Компания Параллель приветствует вас','ua':'Компанія Параллель вітає вас'},
	'saveLoveCity':{'ru':'Запомнить город','ua':'Зберегти місто'},
	'delLoveCity':{'ru':"Удалить город",'ua':'Видалити місто'},
	'home':{'ru':u'/Домой'+u"\U0001F3E0",'ua':u'/Додому'+u"\U0001F3E0"},
	'showMap':{'ru':'Показать на карте 🌏','ua':'Показати на карті 🌏'},
	'changeAction':{'ru':'Выберите акцию','ua':'Оберіть акцію'},
	'verySorry':{'ru':'Произошла ошибка, просим прощения,попробуйте еще раз','ua':'Відбулася технічна помилка, просимо вибачення, спробуйте ще раз'},
	'selectAreaOrCity':{'ru':'Выберите область или сохраненный город','ua':'Оберіть область чи збережене місто'},
	'selectArea':{'ru':"Выберите область",'ua':'Оберіть область'}
	}

def obl(lang):
        try:
                site=urlopen("http://parallel.ua/"+str(lang=='ua' and 'uk/' or '')+"retail-prices/")
                site = BeautifulSoup(site,"html.parser")
                ul = site.find('ul',{'class':'regions'})
                sp=ul.findAll('span')
				
                return [s.text for s in sp]
        except Exception:
                return []
def city(obl,love,lang):
        try:
                site=urlopen("http://parallel.ua/"+str(lang=='ua' and 'uk/' or '')+"retail-prices/")
                site = BeautifulSoup(site,"html.parser")
                ul = site.find('ul',{'class':'regions'})
                li=ul.findAll('li')
                if love:
                        
                        for l in li:
                                if l.find('span') is not  None and  l.find('span').text==obl: 
                                        return {str(l2.find('a').text).rstrip():l2.find('a')['href'][9:].rstrip() for l2 in l.find('ul').findAll('li') if l2.find('a') is not None}
                        else:
                                raise KeyError
                else:

                    for l in li:
                            for l2 in l.findAll('ul'):
                                        for l3 in l2:
                                               
                                                if l3.find('a') is not None and l3.find('a').text==obl:
                                                        return {str(l3.find('a').text).rstrip():l3.find('a')['href'][9:].rstrip()}

                                        
 
        except Exception:
                return []

def dMaps(city):
	with codecs.open('files/mapsAZS.txt','r',encoding='utf-8') as f:
			for i in f:
				if i.split(';')[0]==city:
					return i.split(';')[1][:-1]
				
def fLang():
	di={}
	with open('files/lang.txt','r') as f:
		for i in f:
			i=i.split(';')
			di[i[0]]=i[1][:-1]
	return di
			
			   
			   
			   
			   
			   
			   
			   
			   
			   
