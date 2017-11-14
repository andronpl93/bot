def isOdmen(id,file):
    try:
        with open(file,'r') as f:
            for i in f:
                if str(id)==i[:-1]:
                    return 1
            return 0
    except Exception:
        pass

def check(id,f,l,cur,con):
    cur.execute("select * from allpeople where id_user='{0}'".format(id))
    a=cur.fetchall()
    if len(a)==0:
        cur.execute("insert into allpeople (id_user,f_name,l_name) values('{0}','{1}','{2}');".format(id,f,l))
        con.commit()

