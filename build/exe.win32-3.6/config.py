import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs


token= "449516678:AAG-3WuJMd6bmJMY5gSmow7BQZZe1qb3nHw"
botan_key = "ced7eedf-3482-4f6a-bc62-1cba635cdbd4"
saveLoveCity='Запомнить город'
delLoveCity="Удалить город"
home=u'/Домой'+u"\U0001F3E0"
showMap='Показать на карте 🌏'
changeAction='Выберите акцию'
verySorry= 'Произошла ошибка, просим прощения,попробуйте еще раз'
def obl():
        try:
                site=urlopen("http://parallel.ua/retail-prices/")
                site = BeautifulSoup(site,"html.parser")
                ul = site.find('ul',{'class':'regions'})
                sp=ul.findAll('span')
                return [s.text for s in sp]
        except Exception:
                return []
def city(obl,love=1):
        try:
                site=urlopen("http://parallel.ua/retail-prices/")
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
				

			   
			   
			   
			   
			   
			   
			   
			   
			   
