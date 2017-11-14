from urllib.request import urlopen
from decorators import fatallError
import time
import pyodbc
dbq = pyodbc.connect('DSN=Oracl;'+'PWD=S1mple_U5er')
cursor = dbq.cursor()
def findCard(id_,cur,card=0,s=True):
    ret=[]
    cur.execute("select * from login where id_user='{0}'".format(id_))
    f=cur.fetchall()
    for i in f:
                if card==0:

                        if str(id_)==i[1] :
                            ret.append([i[1],i[2],i[3]])
                else:
                    if s:
                         if str(id_)==i[1] and str(card)==i[2] :
                            ret.append([i[1],i[2],i[3]])
                    else:
                        if str(id_)==i[1] and str(card)==i[2]:
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
            a=float(str(a).strip().replace(',','.'))
            if a==0:
                if len(log)==8:
                    if log[0]=='0':
                        x='2330'+log+'%'
                    else:
                        x='2350'+log+'%'
                else:
                    x='989898'+log

                cursor.execute("select c.card_lock from card  c where c.graphic_number like '{0}'".format(x))
                row = cursor.fetchone()
                if row is not None:
                    if str(row[0])=='1':
                        return  [1,(log,log[0]=='0' and 'KB' or 'MB')]
                    else:
                        return [1,(log,'0')]      
            else:
                   return [1,(log,a)]

    except :
        return [0,u"Произошла ошибка, просим прощения, попробуйте еще раз."]

def writeCard(id_,log,pas,cur,con):
    cur.execute("insert into login (id_user,login,pass) values('{0}','{1}','{2}')".format(id_,log,pas))
    
    con.commit()
    cur.execute("select * from allcard where id_user='{0}' and login='{1}'".format(id_,log))
    a=cur.fetchall()
    if len(a)==0:
        cur.execute("insert into allcard (id_user,login,pass) values('{0}','{1}','{2}')".format(id_,log,pas))
        
    con.commit()
        
       
def logOut(id_,card,cur,con):
    cur.execute("delete from login where id_user='{0}' and login='{1}'".format(id_,card))
    con.commit()

def findLoveCity(id_,lang,cur):
        cur.execute("select  city from savecity where id_user='{0}' and l='{1}'".format(id_,lang) )
        x=cur.fetchall()
        rez=[i[0] for i in x]
        return rez
    
def request(card,dStart,dEnd):
    cursor.execute("""select 
       pos.name "AZS",
       gl.name "Name",
       t.date_of "Day",
       ch.PRICE "Price",
       sum(-ch.amount_curr) "LitresCURR",
       sum(-ch.cost_orig) "Summa",
       t.BONUS_CHARGE "Bonus",
       t.FLAG_PAY_BONUS "B"
from  parallel.card c,
       parallel.t_data_check CH,
       parallel.goods_pos GP,
       parallel.goods_prll gl,
       parallel.pos,
       parallel.t_data t
where t.id_caRD = c.id
   and t.id = ch.id_data
   and ch.id_goods_pos = gp.id
   and gp.code = gl.code(+)
   and t.KIND in (3, 13)
   and t.FLAG_PRESENT_RET = 0
   and t.state = 2
   and c.graphic_number = '{0}'
   and t.id_pos = pos.id
   and t.date_of between to_date('{1}', 'dd.mm.yyyy') and to_date('{2}', 'dd.mm.yyyy')
group by pos.name, gl.name, t.date_of, c.graphic_number,  ch.PRICE, t.FLAG_PAY_BONUS, t.BONUS_CHARGE
order by t.date_of""".format(card,dStart,dEnd))
    rows=cursor.fetchall()
    rez={}
    for row in rows:
        if str(row[2]) not in rez:
            rez[str(row[2])]={}
            if row[0] not in  rez[str(row[2])]:
                rez[str(row[2])][row[0]]=[]
        rez[str(row[2])][row[0]].append((row[1],round(row[3],2),round(row[4]),round(row[5],2),round(row[6],2),int(row[7])))
    print(rez)




















    
