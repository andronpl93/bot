import datetime
import sys
import traceback
import config
from config import NotComands

def fatallError(func):
    def wrap(*args,**kargs):
        try:
            func(*args,**kargs)
        except KeyError:
            langFunc(*args)
        except :
            f = open('fattalErrors.txt' , 'a')
            f.write("{0}~ {1} \n\n".format(datetime.datetime.now(),traceback.format_exc()))
            f.close()
    return wrap

def LangError(func):
    global langFunc
    langFunc=func
    def wrap(message):
            langFunc=func(message)
    return wrap

def Buttons(bot,language):
    def dec(func):
        def wrap(message):
            nonlocal bot
            if message.text in [config.text['home'][language[str(message.from_user.id)]],'/start']:
                return 0
            try:
                func(message)
            except NotComands:
                bot.register_next_step_handler(message,wrap)
        return wrap
    return dec


