import datetime
import sys
import traceback
def fatallError(func):
    def wrap(*args,**kargs):
        try:
            func(*args,**kargs)
        except Exception:
            f = open('fattalErrors.txt' , 'a')
            f.write("{0}~ {1} \n\n".format(datetime.datetime.now(),traceback.format_exc()))
            f.close()
    return wrap

def Buttons(bot):
    def dec(func):
        def wrap(message):
            nonlocal bot
            try:
                func(message)
            except KeyError:
                bot.register_next_step_handler(message,wrap)
        return wrap
    return dec
