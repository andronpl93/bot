from urllib.request import urlopen
from decorators import fatallError
import time

def findCard(id_,card=0,s=True):
    ret=[]
    with open('files/login.txt','r') as f:
            for i in f:
                if card==0:

                        if str(id_)==i.split(";")[0] :
                            ret.append([i.split(";")[0],i.split(";")[1],i.split(";")[2][:-1]])
                else:
                    if s:
                         if str(id_)==i.split(";")[0] and str(card)==i.split(";")[1] :
                            ret.append([i.split(";")[0],i.split(";")[1],i.split(";")[2][:-1]])
                    else:
                        if str(id_)==i.split(";")[0] and str(card)==i.split(";")[1]:
                            return 0
            return ret
        
 
def req(log,pas,lang):
    a='FAIL0'
    try:   
        a=urlopen("http://85.17.143.174:8080/parallel_app/parallel.p_mob_app.get_bonus?login={0}&password={1}".format(log,pas)).read().decode("utf-8")

        if a[:-1]=="FAIL":
                        if lang=='ru':
                            return [0,u"Карта {0} не зарегистрированна".format(log)]
                        else:
                            return [0,u"Карта {0} не зареєстрована".format(log)]
        else:
                        if lang=='ru':
                            return [1,u"На карте {0} \n{1}бонусов".format(log,a)]
                        else:
                            return [1,u"На карті {0} \n{1}бонусів".format(log,a)]
    except :
        return [0,u"Произошла ошибка, просим прощения, попробуйте еще раз."]

def writeCard(id,log,pas):
    with open('files/login.txt','a') as f:
        f.write('{0};{1};{2}\n'.format(id,log,pas))
    with open('files/AllCard.txt','a') as f:
        f.write('{0};{1};{2}\n'.format(id,log,pas))
        
       
def logOut(id_,card):
    ret=[]
    with open('files/login.txt','r') as f:
            for i in f:
                    if str(id_)==i.split(";")[0] and str(card)==i.split(";")[1]:
                         pass
                    else:
                        ret.append(i)

    with open('files/login.txt','w') as f:
        for i in ret:
            f.write(i)

def findLoveCity(id_,lang):
        rez=[]
        with open('files/saveAZS.txt','r') as f:
            for i in f:
                    if str(id_)==i.split(";")[0] and lang==i.split(";")[2][:-1]:
                         rez.append(i.split(";")[1])
            return rez
    
