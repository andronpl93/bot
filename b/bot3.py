import xlrd,os,sys
import imaplib,time
from datetime import datetime,timedelta
import pickle
from PIL import Image,ImageDraw, ImageFont
fpath='C:/BOTTelegram/'
x=0
def go():
    global x
    a=[]
    file=open(fpath+'logbot2.txt','a')
    z=datetime.now()
    file.write('Время: {0}. Проснулся\n'.format(z))
    if 7<=z.hour<=14:
        file.write('Проверяю файл\n')
        path2='//192.168.0.222/аналитика/1 Ежедневная отчетность/Продажи/2017/05 Цены на сайте/'
        dirpath, dirnames, filenames = next(os.walk(path2))
        for f in filenames:
                try:
                    if f[-5:]==".xlsx" and f.find('.')==2 and os.path.getsize(path2+f):
                            a.append((f,os.path.getmtime(path2+f)))
                except FileNotFoundError:
                    file.write("Нашел мутный файл "+str(f)+'\n')
        y=max(a,key=lambda x: x[1])
        if y[1]!=x:
            file.write('Нашел новый файл\n')
            x=y[1]
            flag=1
            
            Func(path2+y[0],file)
            #z2=datetime(z.year,z.month,z.day)+timedelta(seconds=115200)
            #sl=(z2-z).seconds
            sl=3600
        else:
            file.write('Не нашел новый файл\n')
            sl=600
    else:
            sl=3600
    file.write("Засыпаю на {0} секунд\n\n".format(sl))
    file.close()
    print(1)
    time.sleep(sl)
    go()
        
def Func(f,file):
    rb = xlrd.open_workbook(f)
    sheet = rb.sheet_by_index(0)
    data={'ru':{},'ua':{}}
    for i in range(2,63):
        x=sheet.row_values(i)
        data['ru'][x[0]]={}
        data['ua'][x[1]]={}
    for i in range(2,63):
        x=sheet.row_values(i)
        if x[2]=='Город 15':
            continue
        data['ru'][x[0]][x[2]]=[]
        data['ua'][x[1]][x[3]]=[]
    for i in range(2,63):
        x=sheet.row_values(i)
        if x[2]=='Город 15':
            continue
        data['ru'][x[0]][x[2]].append((x[7],x[17],x[14],x[16],x[10],x[15],x[11]))
        data['ua'][x[1]][x[3]].append((x[8],x[17],x[14],x[16],x[10],x[15],x[11]))
        
    with open(fpath+'files/data.dat', 'wb') as f:
        pickle.dump(data,f)
    file.write("Сохранил словарь\n")
        #data_new = pickle.load(f)
    for dirpath, dirnames, filenames in os.walk(fpath+'price/'):
            for f in filenames:
                if f[-5:]=='.webp':
                    os.remove(fpath+'price/'+f)
    file.write("Удалил стикеры\n")

                    
    fnt = ImageFont.truetype(fpath+'price/7.ttf', 50)
    for i in data['ru']:
        for j in data['ru'][i]:
            for c in range(len(data['ru'][i][j])):
                a='{0}{1}{2}{3}{4}{5}'.format(*[str(e).replace('.','').replace(' ','-') for e in data['ru'][i][j][c][1:]])
                file.write(str(data['ru'][i][j][c])+'\n')
                f=Image.open(fpath+'price/bot.png')
                d = ImageDraw.Draw(f)
                for q in range(6):
                    d.text((215,q*65+61),str(data['ru'][i][j][c][q+1]).replace(' ','--.--') , font=fnt, fill=(255,255,255,255))
                    f.save(fpath+'price/{0}.webp'.format(a))
    file.write("Создал новые стикеры \n")

if __name__=='__main__':
    #try:
        go()
    #except Exception:
       # time.sleep(180)
        #go()
        
