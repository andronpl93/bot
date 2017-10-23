def isOdmen(id,file):
    try:
        with open(file,'r') as f:
            for i in f:
                if str(id)==i[:-1]:
                    return 1
            return 0
    except Exception:
        pass

def check(id,first,l):
    try:
        with open('files/people/all.txt','a') as f:
            f.write('{0};{1};{2}\n'.format(id,first,l))
    except Exception:
        pass
