import os,time
from  datetime import datetime
def go():
        sub_size=0
        for path, subdirs, files in os.walk('price/'):
                for file in files:
                    if file[-5:]!='.webp':
                            continue
                    filename = os.path.join(path, file)
                    sub_size += os.path.getsize(filename) /1024 /1024
        print('Текущее время: '+str(datetime.now())+" Размер в папке:"+str(round(sub_size,2))+" МБ ")
        if sub_size>8:
            for path, subdirs, files in os.walk('price/'):
                for file in files:
                    if file[-5:]!='.webp':
                            continue
                    os.remove('price/'+file)
            print("Удалил файлы")
        else:
            print('Удалять не нужно')
        time.sleep(864000)
        go()
        #864000

if __name__ == '__main__':
        go()
