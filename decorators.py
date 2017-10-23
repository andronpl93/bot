import datetime
import sys
import traceback
import config
def fatallError(func):
    def wrap(*args,**kargs):
        try:
            func(*args,**kargs)
        except :
            f = open('fattalErrors.txt' , 'a')
            f.write("{0}~ {1} \n\n".format(datetime.datetime.now(),traceback.format_exc()))
            f.close()
    return wrap

def Buttons(bot):
    def dec(func):
        def wrap(message):
            nonlocal bot
            if message.text in [config.home,'/start']:
                return 0
            try:
                func(message)
            except KeyError:
                bot.register_next_step_handler(message,wrap)
        return wrap
    return dec
