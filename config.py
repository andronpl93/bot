﻿import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs
fpath='C:/BOTTelegram/'
#fpath='D:/Phyton/bot/'
lang='ru'
token= "493097551:AAHVx4ULGVd0GZ2QcpRJaItyy7_NdSlgajo"
botan_key = "a9f7a52b-9036-46ad-a648-d38b3be179a3"
text={
	'textHelp':{'ru':(u"Несколько советов: \n <b>1.</b> Если вы видите буквенную клавиатуру, то нажмите на эту иконку \U00002B07","<b>2.</b> Не пытайтесь вводить команды вручную, используйте кнопки. \n <b>3.</b> Дожидайтесь ответа от бота(он вам обязательно ответит), только потом вводите новую команду \n <b>4.</b> В любой непонятной ситуации воспользуйтесь командой /start"),'ua':(u"Декілька порад: \n <b>1.</b> Якщо ви бачите літерну клавіатуру, то натисніть цю кнопку \U00002B07","<b>2.</b> Не намагайтесь вводити команди вручну, використовуйте кнопки. \n <b>3.</b> Дочекайтесь відповіді від бота(він вам обов`язково відповість), тільки потім вводьте нову команду \n<b>4.</b> В будь-якій незрозумілій ситуації скористайтесь командою /start")},
	'textWait':{'ru':'Возможно будет долго... ⌛','ua':'Можливо доведеться почекати... ⌛'},
	'textErrorPrice':{'ru':'На данный момент информация о ценах недоступна по техническим причинам, попробуйте позже','ua':'На даний час інформація щодо цін недоступна, спробуйте пізніше'},
	'textselL':{'ru':'Русский','ua':'Українська'},
	'textContactHotLine':{'ru':'Горячая линия','ua':'Гаряча лінія'},
	'textBan':{'ru':'Карта {0} заблокированна. Для разблокировки обратитесь на горячую линию (бесплатно с мобильных и стационарных телефонов)\n <em>Обратите внимание, информация по карте обновится в течении суток после разблокировки</em>','ua':'Карта {0} заблокована. Для розблокування зверніться на гарячу лінію (безкоштовно з мобільних і стаціонарних телефонів)\n <em> Зверніть увагу, інформація по карті оновиться протягом доби після розблокування </em>'},
	'textLengEdit':{'ru':'Язык успешно установлен','ua':'Мова успiшно встановлена'},
	'textLang':{'ru':'Выберите язык общения🗣','ua':'Оберіть мову спілкування🗣'},
	'textLangSel':{'ru':'Изменить язык🗣','ua':'Змінити мову🗣'},
	'textMoreInfo':{'ru':'Детальная информация на сайте','ua':'Детальна інформація на сайті'},
	'textNotActions':{'ru':'На данный момент нет активных акций','ua':'На даний момент немає активних акцій'},
	'textCardDel':{'ru':'Карта была удалена','ua':'Карта була видалена'},
	'textInCard':{'ru':'Введите номер карты','ua':'Введіть номер карти'},
	'textInPass':{'ru':'Введите пароль','ua':'Введіть пароль'},
	'textPop':{'ru':'Введите номер карты чтобы попробовать еще раз или нажмите ','ua':'Введіть номер карти щоб спробувати ще раз або натисніть '},
	'textTelCardError':{'ru':u'Телефон горячей линии (бесплатный с мобильных и стационарных телефонов):\n +380800503333','ua':'Телефон горячої лініі (безкоштовний з мобільних та стаціонарних телефонів):\n +380800503333'},
	'textCardIn':{'ru':'Данная карта уже зарегистрирована','ua':'Ця карта вже зареэстрована'},
	'textCardNot':{'ru':'Данная карта не зарегистрирована','ua':'Ця карта не зареэстрована'},
	'textCardSave':{'ru':'Карта сохранена','ua':'Карта збережена'},
	'textSelCard':{'ru':"Выберите карту",'ua':'Оберіть карту'},
	'textLogOut':{'ru':'Убрать карту','ua':'Прибрати карту'},
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
	'contacts':{'ru':u'Контакты'+u"\U0001F4DE",'ua':u'Контакти'+u"\U0001F4DE"},
	'showMap':{'ru':'Показать на карте 🌏','ua':'Показати на карті 🌏'},
	'changeAction':{'ru':'Выберите акцию','ua':'Оберіть акцію'},
	'verySorry':{'ru':'Произошла ошибка, просим прощения, попробуйте еще раз','ua':'Відбулася технічна помилка, просимо вибачення, спробуйте ще раз'},
	'selectAreaOrCity':{'ru':'Выберите область или сохраненный город','ua':'Оберіть область чи збережене місто'},
	'selectArea':{'ru':"Выберите область",'ua':'Оберіть область'}
	}
contactsText=[
	{'ru':u'Телефон горячей линии (бесплатный с мобильных и стационарных телефонов): +380800503333','ua':u'Телефон гарячої лінії (безкоштовний з мобільних і стаціонарних телефонів): +380800503333'},
	{'ru':u'Центр по работе с корпоративными клиентами: \n 69091, г.Запорожье, бул. Шевченко, 71а\nТелефон: +380937268708 , +380937268642 , +380937268873','ua':u'Центр по роботі з корпоративними клієнтами: \n 69091, м.Запорожжя, бул. Шевченко, 71а\nТелефон: +380937268708 , +380937268642 , +380937268873'},
	{'ru':u'Заказ талонов и топливных карт: +380937268708','ua':u'Замовлення талонів і паливних карт: +380937268708'},
	{'ru':u'Мелкий опт (бензовозные партии): +380937268884, +380935316772','ua':u'Дрібний гурт (бензовозні партіі) : +380937268884, +380935316772'},
	{'ru':u'Крупный опт (поставка жд нормами): +380937268830','ua':u'Великий гурт (поставка залізничними нормами): +380937268830'},
	{'ru':u'Электронная почта: post@parallel.ua ','ua':u'Електронна пошта: post@parallel.ua '}
]
contactsLink=[
	{'ru':('Веб-сайт компании "Параллель"','http://parallel.ua'),'ua':('Веб-сайт компанії "Паралель"','http://parallel.ua')},
	{'ru':('Группа в facebook','https://www.facebook.com/parallel.ua'),'ua':('Cпільнота в facebook','https://www.facebook.com/parallel.ua')},
	{'ru':('Блог в twitter','https://twitter.com/tm_parallel'),'ua':('Блог в twitter','https://twitter.com/tm_parallel')},
	{'ru':('Instagram','https://www.instagram.com/parallel_ua/'),'ua':('Instagram','https://www.instagram.com/parallel_ua/')}
]


class NotComands(Exception):
   pass
def dMaps(city,l):
	with codecs.open(fpath+'files/mapsAZS.txt','r',encoding='utf-8') as f:
			for i,v in enumerate(f):
				if l=='ua':
					if i<31:
						continue
				else:
					if i>=31:
						continue					
				if v.split(';')[0]==city:
					return v.split(';')[1][:-1]
				
def fLang(cur,con):
	di={}
	cur.execute("select * from lang;")
	rows=cur.fetchall()
	for row in rows:
		di[row[1]]=row[2]
	return di
			
			   
			   
			   
			   
			   
			   
			   
			   
			   
