# -*- coding: iso-8859-1 -*-

"""Libreria di funzioni utili per aprire file di metastock e calcolare indicatori"""

#per lm (vedi sotto)
try: from scipy.stats import fcdf
except ImportError:
    from scipy.stats import f
    fcdf = f.cdf

try:
    from numpy import array,mean,mat
except:
    from scipy import array,mean,mat
###

import string
import datetime
import array
import copy
#from m2ipy import m2i
from struct import *
import statist
import encodings
#per yahoo
import  urllib2
from urllib import urlopen,urlencode
from time import sleep

###
def apridb(db,order=1):
    """apre un archivio sqlite3 e ritorna una lista di dizionari come apridir"""
    from sqlite3 import dbapi2 as sqlite
    con=sqlite.connect(db,detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    cur=con.cursor()
    if order:
        cur.execute('select * from "stocks" order by "symbol"')
    else:
        cur.execute('select * from "stocks"')
    app=cur.fetchall()
    con.close()
    l=[]
    for x in app:
        l.append({'symb':x[0],'desc':x[1]})
    return(l)

def stock_db(db,stock,last_date=0):
    """estrae la lista dei dati di un titolo da un db sqlite3
    e ritorna la lista come in aprifile, se si vuole estrarre le quotazioni
    fino a una certa data allora passare una data datetime in last_date"""
    from sqlite3 import dbapi2 as sqlite
    sqlite.register_converter("ts_oo", sqlite.converters['TIMESTAMP'])
    con=sqlite.connect(db,detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    cur=con.cursor()
    if not last_date:
        cur.execute('select * from "%s" order by "date" asc'%stock)
    else:
        cur.execute('select * from "%s" where "date" <= "%s" order by "date" asc'%(stock,last_date))
    app=cur.fetchall()
    con.close()
    l=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f'),]
    for x in app:
        for y in range(0,len(l)):
            l[y].append(x[y])
    return(l)

def crea5min_day(l):
    #questa funzione e' sostituita da creaNmin_day ma rimane per eventuale compatibilita
    """trasforma dati di un solo giorno da 1 min a 5 min"""
    #trovo l'orario iniziale per difetto a 5min prima
    min5=[[],]
    for x in range(0,len(l)-1):
        min5+=[array.array('f'),]
    ora_ini=l[0][0]-datetime.timedelta(0,0,0,0,(l[0][0].minute%5))
    #print l[0][0],ora_ini,datetime.timedelta(0,0,0,0,l[0][0].minute-l[0][0].minute%5)
    #print (l[0][0].minute%5)
    ini=0
    delta=datetime.timedelta(0,0,0,0,5)
    for x in range(0,len(l[0])):
        if (l[0][x]>=ora_ini+delta)or(x==len(l[0])):
            if x<len(l[0])-1:
                fin=x
            else:
                fin=x+1
            min5[0].append(l[0][x-1])
            min5[1].append(l[1][ini])
            min5[2].append(max(l[2][ini:x]))
            min5[3].append(min(l[3][ini:x]))
            min5[4].append(l[4][x-1])
            min5[5].append(sum(l[5][ini:x]))
            ini=x
            ora_ini=l[0][x]
    #print min5
    #raw_input('ts')
    return(min5)

def creaNmin_day_ex(l,N=5):
    """trasforma dati di un solo giorno da m min a N min"""
    #trovo l'orario iniziale per difetto a Nmin prima
    minN=[[],]
    for x in range(0,len(l)-1):
        minN+=[array.array('f'),]
    ora_ini=l[0][0]-datetime.timedelta(0,0,0,0,(l[0][0].minute%N+1))
    #print l[0][0],ora_ini,datetime.timedelta(0,0,0,0,l[0][0].minute-l[0][0].minute%5)
    #print (l[0][0].minute%5)
    ini=0
    delta=datetime.timedelta(0,0,0,0,N)
    for x in range(0,len(l[0])):
        if (l[0][x]>=ora_ini+delta)or(x==len(l[0])):
            if x<len(l[0])-1:
                fin=x
            else:
                fin=x+1
            minN[0].append(l[0][x-1])
            minN[1].append(l[1][ini])
            minN[2].append(max(l[2][ini:x]))
            minN[3].append(min(l[3][ini:x]))
            minN[4].append(l[4][x-1])
            minN[5].append(sum(l[5][ini:x]))
            ini=x
            ora_ini=l[0][x]
    #print min5
    #raw_input('ts')
    return(minN)

def creaNmin_day(l,N=5):
    """trasforma dati di un solo giorno da m min a N min"""
    #trovo l'orario iniziale per difetto a Nmin prima
    minN=[[],]
    for x in range(0,len(l)-1):
        minN+=[array.array('f'),]
    ora_ini=datetime.datetime(l[0][0].year,l[0][0].month,l[0][0].day,l[0][0].hour,1,0)
    #ora_ini=l[0][0]-datetime.timedelta(0,0,0,0,(l[0][0].minute%N+1))
    #print l[0][0],ora_ini,datetime.timedelta(0,0,0,0,l[0][0].minute-l[0][0].minute%5)
    #print (l[0][0].minute%5)
    
    ini=0
    delta=datetime.timedelta(0,0,0,0,N)
    #print 'trovo la prima ora',ora_ini,l[0][0]
    while ora_ini+delta<l[0][0]:
        ora_ini+=delta
        #print ora_ini
    ###
    for x in range(0,len(l[0])):
        if (l[0][x]>=ora_ini+delta)or(x==len(l[0])):
            if (x<len(l[0])-1)and(x<>0):
                fin=x
            else:
                fin=x+1
            #print'ini',ini,'fin',fin
            minN[0].append(l[0][fin-1])
            minN[1].append(l[1][ini])
            minN[2].append(max(l[2][ini:fin]))
            minN[3].append(min(l[3][ini:fin]))
            minN[4].append(l[4][fin-1])
            minN[5].append(sum(l[5][ini:fin]))
            ini=x
            ora_ini+=delta
    #print min5
    #raw_input('ts')
    return(minN)
            

def min12min5(l):
    #quetsa funzione e' stata sostituita da minM2minN ma e' rimasta per eventuali compatibilita'
    """trasforma l 1 min in l 5 min, effettuando il controllo sull'orario"""
    #si suppone che le quotazioni inizino ad un orario arrotondato a 5 minuti, es.: 9:00, 9:05
    min5=[[],]
    for x in range(0,len(l)-1):
        min5+=[array.array('f'),]
    ini=0
    for x in range(0,len(l[0])):
        if (l[0][ini].day<>l[0][x].day)or(x==len(l[0])-1):
            if x<len(l[0])-1:
                fin=x
            else:
                fin=x+1
            #a questo punto ho trovato inizio e fine di un giorno
            #al suo interno trovo i 5 minuti
            appl=[]
            for k in l:
                appl.append(k[ini:fin])
            min5_day=crea5min_day(appl)
            #print min5_day[0][:3]
            #raw_input('ts')
            for y in range(0,len(min5_day)):
                min5[y]+=min5_day[y]
            #print min5[:3]
            #raw_input('ts')
            ini=x
    return(min5)

def minM2minN(l,N=5):
    """trasforma l M min in l N min, effettuando il controllo sull'orario"""
    #si suppone che le quotazioni inizino ad un orario arrotondato a M minuti, es.: 9:00, 9:05
    minN=[[],]
    for x in range(0,len(l)-1):
        minN+=[array.array('f'),]
    ini=0
    for x in range(0,len(l[0])):
        if (l[0][ini].day<>l[0][x].day)or(x==len(l[0])-1):
            if x<len(l[0])-1:
                fin=x
            else:
                fin=x+1
            #a questo punto ho trovato inizio e fine di un giorno
            #al suo interno trovo i N minuti
            appl=[]
            for k in l:
                appl.append(k[ini:fin])
            minN_day=creaNmin_day(appl,N=N)
            #print min5_day[0][:3]
            #raw_input('ts')
            for y in range(0,len(minN_day)):
                minN[y]+=minN_day[y]
            #print min5[:3]
            #raw_input('ts')
            ini=x
    return(minN)
            

def i2d(l):
    """trasfroma l intraday in l daily"""
    d=[[],]
    for x in range(0,len(l)-1):
        d+=[array.array('f'),]
    #print 'd_sl',d
    ini=0
    delta_ah=datetime.timedelta(0,0,0,0,11)
    for x in range(0,len(l[0])):
        if (l[0][ini].day<>l[0][x].day)or(x==len(l[0])-1):
            if x<len(l[0])-1:
                fin=x
            else:
                fin=x+1
            #ora ho ini e fin di ogni gg
            #bisogna togliere l'eventuale afterhour
            #trovando il primi 2 buchi di almeno 11 minuti
            #(chiusura e inizio ah)
            for y in range(ini,fin-1,1):
                if l[0][y+1]-l[0][y]>delta_ah:
                    fin=y+1
                    break
            ###
            d[0].append(l[0][fin-1])
            #print 'd0',d[0][-1],d[0]
            d[1].append(l[1][ini])
            #print 'd1',d[1][-1],d[1]
            d[2].append(max(l[2][ini:fin]))
            #print 'd2',d[2][-1],d[2]
            d[3].append(min(l[3][ini:fin]))
            #print 'd3',d[3][-1],d[3]
            d[4].append(l[4][fin-1])
            #print 'd4',d[4][-1],d[4]
            d[5].append(sum(l[5][ini:fin]))
            ini=x
    return(d)

def raggruppa(l):
    """funzione usata per aggregare le quotazioni in settimanali o
    in altri periodi, ritorna un array a 1 dimensione"""
    #print len(l[0]),l[0][0]
    if len(l[0])==0:
        return(0)
    l_out=[]
    l_out.append(l[0][-1])
    l_out.append(l[1][0])
    l_out.append(max(l[2]))
    l_out.append(min(l[3]))
    l_out.append(l[4][-1])
    l_out.append(sum(l[5]))
    return(l_out)

def trasf_w(l_in,):
    """trasforma dati (con data datetime) in settimanali"""
    
    def trova_fine_sett(l,x,domenica):
        """trova l'indice di l corrispondente all'ultimo giorno utile della settimana 
        partendo da x"""
        y=x
        while (y<len(l[0]))and(l[0][y]<domenica):
            y+=1
        if y<len(l[0]):
            return(y)
        else:
            return(y+1)

    l_out=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f')]
    day=datetime.timedelta(1)
    week=datetime.timedelta(7)
    #trovo la prima domenica
    sunday=l_in[0][0]
    while sunday.weekday()<>6:
        sunday+=day
    x=0
    while x<len(l_in[0]):
        y=trova_fine_sett(l_in,x,sunday)
        app_l_w=raggruppa([l_in[0][x:y],l_in[1][x:y],l_in[2][x:y],
                           l_in[3][x:y],l_in[4][x:y],l_in[5][x:y]])
        if app_l_w:
            for x in range(0,len(l_out)):
                l_out[x].append(app_l_w[x])
        x=y
        sunday+=week
    return(l_out)

    
def trasforma(lista,opt='w'):
    """trasforma una lista di dati in settimanale o mensile"""
    lw=[[],[],[],[],[],[]]
    ind=0
    day=datetime.timedelta(days=1)
    if str(type(lista[0][ind])).find('datetime')<>-1:
        sw_datetime=1
    else:
        sw_datetime=0
    while ind<len(lista[0]):
        if sw_datetime:
            ini=lista[0][ind]
        else:
            aa,mm,gg=ftodate(lista[0][ind])
            ini=datetime.date(aa,mm,gg)
        #print ini,ind
        if opt=='w':
            while datetime.date.weekday(ini)<>6:
                ini+=day
        elif opt=='m':
            mese=ini.month
            while ini.month==mese:
                ini+=day
            ini-=day
        #print 'ini1 ',ini,ind
        dt=lista[0][ind]
        op=lista[1][ind]
        max=0
        min=999999999999999999999999999999999999
        vol=0.0
        if sw_datetime==0:
            fin=datafl(ini.strftime('%d/%m/%Y'),fmt="gg/mm/aaaa")
        else:
            fin=ini
        #print 'fin',fin
        while (ind<len(lista[0]))and(lista[0][ind]<=fin):
            if max<lista[2][ind]:
                max=lista[2][ind]
            if min>lista[3][ind]:
                min=lista[3][ind]
            vol+=lista[5][ind]
            ind+=1
        cl=lista[4][ind-1]
        lw[0].append(dt)
        lw[1].append(op)
        lw[2].append(max)
        lw[3].append(min)
        lw[4].append(cl)
        lw[5].append(vol)
        #print 'ind finale',ind
    return(lw)

def apridir(filepath):
    """apre l'archivio,specificare il file "MASTER",ritorna
    una lista di dizionari [first,last,format,simb]"""
    from m2ipy import m2i
    try:
        fd=open(filepath,'rb')
    except:
        print 'errore in ',filepath
        return([])
    else:
        buf=fd.read()
        fd.close()
        num=unpack('B',buf[0])
        #print 'numero di file contenuti:',num[0]
        v=unpack('B',buf[1])
        #print 'numero massimo usato:',v[0]
        list=[]
        for i in range(0,num[0]):
            v=unpack('B2c4s16s',buf[(53+i*53):(76+i*53)])
            D1={'num':v[0],'tipo':v[1],'nome':v[4],'first':'','last':'','format':'','simb':''}
            #print 'D!:',D1
            v=unpack('ffc2s14s',buf[(78+i*53):(103+i*53)])
            D1['first']=(m2i(v[0]))
            D1['last']=(m2i(v[1]))
            D1['format']=v[2]
            D1['simb']=v[4]
            list.append(D1)
        return(list)

def aprifile(filepath,intr=0,narray=6,masterfile='master'):
    """apre un file metastock ==> list [6(7 se intraday) X n] :data(string AAAAMMGG),open(fl),max,min,close,vol(,time se intra)"""
    from m2ipy import m2i
    #print 'apertura',filepath
    filepath=string.replace(filepath,'\\','/')
    ind=string.rfind(filepath,'/')
    ind1=string.rfind(filepath,'.')
    #print filepath[ind+1:ind1]
    num=int(filepath[ind+2:ind1])
    #print num
    #print filepath
    #se intr == 2 non effettua il controllo sul file master
    if intr<>2:
        lmaster=apridir(filepath[:ind+1]+masterfile)
        for x in lmaster:
            if x['num']==num:
                if x['format']=='I':
                    intr=1
                    break
    else:
        #presuppongo che se salto il controllo sul file master e' daily
        intr=0
    try:
        fd=open(filepath,'rb')
    except:
        print 'impossibile aprire il file o il master specificato:',filepath
        return(list)
    else:
        buf=fd.read()
        fd.close()
        if intr:
            list=[[],[],[],[],[],[],[]]
            stunpack='ffffffff'
            num=32
        else:
            list=[[],[],[],[],[],[]]
            stunpack='fffffff'
            num=28
        v=unpack('HH',buf[0:4])
        #print ' max rec: %d , last rec: %d'%(v[0],v[1])
        i=num
        while i<len(buf):
            v=unpack(stunpack,buf[i:i+num])
            for x in range(0,len(stunpack)-1):
                list[x].append(m2i(v[x]))
            i+=num
        if intr:
            applist=list[1]
            for x in range(1,6):
                list[x]=list[x+1]
            list[6]=applist
            if narray==6:
                for x in range(0,len(list[0])):
                    list[0][x]=list[0][x]+list[6][x]/1000000
                del list[6]                
        #vedere gli aggiornameniti di at2 se si vuole aggiornare agli ultimi giorni
        return (list)

def rigadati(riga,sep='\t',ord=[]):
    """prende dei dati separati da 'sep' da una riga di testo nelle colonne ord"""
    riga1=string.replace(riga,'\r','')
    riga1=string.replace(riga1,'\n','')
    valori=[]
    ini=0
    #cont=0
    while string.find(riga1,sep,ini)<>-1:
        fin=string.find(riga1,sep,ini)
        valori.append(riga1[ini:fin])
        #print valori
        #valori[cont]=riga1[ini:fin]
        #cont+=1
        ini=fin+1
    valori.append(riga1[ini:])
    #print 'valori',len(valori),valori
    ris=[]
    for x in ord:
        ris.append(valori[x])
    return(ris)

def aprifiletxtintra(fdfile,sep=',',ord=[2,4,5,6,7,8,3]):
    """apre i file txtintra e ritorna l come aprifile normale\
    ord: data,apertura,max,min,close,vol,ora"""
    #print 'in apri',fdfile
    fd=open(fdfile,'r')
    lines=fd.readlines()
    fd.close()
    l=[[],[],[],[],[],[]]
    for line in lines:
        if line[0]=='<':
            continue
        #line1=string.replace(line,',','.')
        appquot=rigadati(line,sep=sep,ord=ord)
        appquot[0]+='.'+appquot[-1][:4]
        for x in range(0,6):
            l[x].append(float(appquot[x]))
    #fd.close()
    return(l)

def aprifiletxt(fdfile,datafmt='fl',sep=',',dec='.',ord=[2,4,5,6,7,8]):
    """apre i file txtintra e ritorna l come aprifile normale\
    ord: data,apertura,max,min,close,vol___ per i formati della data vedi datafl"""
    #print 'in apri',fdfile
    fd=open(fdfile,'r')
    lines=fd.readlines()
    fd.close()
    #l=[[],[],[],[],[],[]]
    l=[]
    for x in ord:
        l.append([])
    for line in lines:
        if line[0]=='<':
            continue
        #line1=string.replace(line,',','.')
        appquot=rigadati(line,sep=sep,ord=ord)
        #appquot[0]+='.'+appquot[-1][:4]
        if datafmt=='fl':
            l[0].append(float(appquot[0]))
        else:
            #print appquot[0] , datafmt
            l[0].append(datafl(appquot[0],fmt=datafmt))
        for x in range(1,len(ord)):
            if dec <>'.':
                l[x].append(float(string.replace(appquot[x],dec,'.')))
            else:
                l[x].append(float(appquot[x]))
    while len(l)<6:
        app=[]
        for x in range(0,len(l[0])):
            app.append(0)
        l.append(app)
    #fd.close()
    return(l)

def yahoo_today(symbol):
    """cattura i dati odierni e ritorna una riga come l"""
    #c'e' differenza per i titoli americani e italiani quindi differenzio
    if symbol[-3:] in ['.MI','.mi']:
        url='http://it.old.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv'%symbol
        sep=';'
        rep={'\n':'',',':'.'}
    else:
        url='http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv'%symbol
        sep=','
        rep={'\n':'','"':''}
    fd=urllib2.urlopen(url)
    line=fd.read()
    fd.close()
    #print 'symb',symbol
    #print 'l1',line
    for x in rep.keys():
        line=line.replace(x,rep[x])
    #print 'l2',line
    [sym,last,time,date,var,o,h,l,vol]=line.split(sep)
    print(date)
    [mm,dd,yy]=map(int,date.split('/'))                       
    return([datetime.datetime(yy,mm,dd)]+map(float,[o,h,l,last,vol]))

def apriyahoo3(symbol,d1=0,d2=0):
    """usa datetime e usa il sito finance.yahoo.com per avere i link corretti"""

    def convert_date_vecchio(date_y):
        """converte la data yahoo in datetime"""
        month_com=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        [gg,mm,yy]=date_y.split('-')
        mm=month_com.index(mm.lower())+1
        yy=int(yy)
        if yy>=30:
            yy+=1900
        else:
            yy+=2000
        #print 'data_y',yy,mm,int(gg)   
        return(datetime.datetime(yy,mm,int(gg)))

    def convert_date(date_y):
        """converte la data yahoo in datetime"""
        #print("date_y ",date_y)
        [yy,mm,dd]=date_y.split('-')
        return(datetime.datetime(int(yy),int(mm),int(dd)))

    print("apri yahoo 3")
    url="http://finance.yahoo.com/q/hp"#?a=&b=&c=&d=0&e=20&f=2007&g=d&s=%5Eftse
    #imposto le date di inizio(d1) e fine(d2)
    delta=datetime.timedelta(2)
    if not d1:
        #d1=datetime.datetime(1980,1,1)
        #[a,b,c]=d1.timetuple()[:3]
        a=b=c=''
    if not d2:
        d2=datetime.datetime.today()+delta
    [d,e,f]=d2.timetuple()[:3]
    g='d'#per ottenere dati daily
    dict_qs=[('a',a),('b',b),('c',c),('d',d),('e',e),('f',f),('g',g),('s',symbol)]
    ###
    #carico la pagina dei dati storici del titolo
    web_page=urlopen(url+'?'+urlencode(dict_qs))
    print 'info',web_page.info()
    print 'url',web_page.geturl()
    web_page=web_page.read()    
    #cerco il link  "Download To Spreadsheet" al csv
    #spsh_index=web_page.rfind('Spreadsheet')
    spsh_index=web_page.rfind('.csv')
    spsh_index=web_page.rfind('href',0,spsh_index)
    print("url_quote1 ",web_page[spsh_index:spsh_index+40])
    ini_index=web_page.find('http',spsh_index)
    print("url_quote2 ",web_page[ini_index:ini_index+40])
    fin_index=web_page.find('">',ini_index)
    url_quote=web_page[ini_index:fin_index]
    print 'url_quote',url_quote
    ###
    quotes=urlopen(url_quote).readlines()
    l=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f'),]
    for x in quotes[1:]:
        split=x.split(',')
        l[0].append(convert_date(split[0]))
        for y in range(1,6):
            l[y].append(float(split[y]))
    #aggiungo eventuali dati odierni
    #if symbol:
        #aggiungo eventuali dati odierni
    #    l_today=yahoo_today(symbol)
    #    if len(l[0])>0:
    #        if l_today[0]<>l[0][0]:
    #            for x in range(0,len(l_today)):
    #                l[x].insert(0,l_today[x])
    #    else:
    #        for x in range(0,len(l_today)):
    #                l[x].insert(0,l_today[x])
    #    print 'aggiornato today'
    #ordino l dal piu' remoto al piu' recente
    for x in range(0,len(l)):
        l[x].reverse()
    print("len l ",len(l))
    print("len l[1] ", len(l[1]))
    #print("l ",l)
    return(l)
    

def apriyahoo2(symbol,d1=0,d2=0):
    #d1 e d2 devono essere datetime, il formato della data e' datetime
    #questa versione non usa matplotlib.finance.quotes_historical_yahoo
    """prende le quotazioni da yahoo dato il simbolo e ritorna la lista"""  
   
    def convert_date(date_y):
        """converte la data yahoo in datetime"""
        month_com=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        [gg,mm,yy]=date_y.split('-')
        mm=month_com.index(mm.lower())+1
        yy=int(yy)
        if yy>=30:
            yy+=1900
        else:
            yy+=2000
        #print 'data_y',yy,mm,int(gg)   
        return(datetime.datetime(yy,mm,int(gg)))

    print("apri yahoo 2")        
    url_quotes_com='http://ichart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=%d&b=%d&c=%d&ignore=.csv'
    #esempio fiat 3 gennaio 2000 -  26 novembre 2006: http://ichart.finance.yahoo.com/table.csv?s=F.MI&d=10&e=26&f=2006&g=d&a=0&b=3&c=2000&ignore=.csv
    #imposto le date di inizio(d1) e fine(d2)
    delta=datetime.timedelta(2)
    if not d1:
        d1=datetime.datetime(1980,1,1)
    if not d2:
        d2=datetime.datetime.today()+delta
    [a,b,c]=d1.timetuple()[:3]
    [d,e,f]=d2.timetuple()[:3]
    url_quotes=url_quotes_com%(symbol,d-1,e,f,a-1,b,c)
    #print 'url_quotes',url_quotes
    quotes=[]
    try:
        app_quotes=urllib2.urlopen(url_quotes).readlines()
        ###
        #provo a rileggere se non viene caricato per cont volt
        cont=0
        while (len(app_quotes)<2)and(cont<10):
            cont+=1
            print'sleep',symbol,cont
            sleep(2)
            app_quotes=urllib2.urlopen(url_quotes).readlines()
    except:
        pass
    else:
        quotes=app_quotes
            
    ###
    #print 'quotes',quotes
    l=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f'),]
    for x in quotes[1:]:
        split=x.split(',')
        l[0].append(convert_date(split[0]))
        for y in range(1,6):
            l[y].append(float(split[y]))
    #aggiungo eventuali dati odierni
    if symbol:
        #aggiungo eventuali dati odierni
        l_today=yahoo_today(symbol)
        if len(l[0])>0:
            if l_today[0]<>l[0][0]:
                for x in range(0,len(l_today)):
                    l[x].insert(0,l_today[x])
        else:
            for x in range(0,len(l_today)):
                    l[x].insert(0,l_today[x])
        print 'aggiornato today'
    #ordino l dal piu' remoto al piu' recente
    for x in range(0,len(l)):
        l[x].reverse()
    return(l)
    
    

def apriyahoo(symbol,d1=0,d2=0):
    #d1 e d2 devono essere datetime,
    """prende le quotazioni da yahoo dato il simbolo e ritorna la lista"""
    from matplotlib.finance import quotes_historical_yahoo
    from matplotlib.dates import num2date
    from datetime import datetime,timedelta

    print("apri yahoo")
    delta=timedelta(2)
    if not d1:
        d1=datetime(1980,1,1)
    if not d2:
        d2=datetime.today()+delta
    #dati storici
    dati=quotes_historical_yahoo(symbol, d1, d2,adjusted=False)
    l=[]
    for x in range(0,6):
        l.append([])
    #print 'dati yahoo'
    for x in dati:
        #print x
        #print num2date(x[0]),datafl(str(num2date(x[0]))[:10],fmt='aaaa/mm/gg')
        l[0].append(datafl(str(num2date(x[0]))[:10],fmt='aaaa/mm/gg'))
        l[1].append(x[1])
        l[2].append(x[3])
        l[3].append(x[4])
        l[4].append(x[2])
        l[5].append(x[5])
    #print 'l[0]',l[0]
##    for x in range(0,len(l)):
##        for y in l[x]:
##            print y,
##        print
    #dati odierni
    if symbol[-3:]==".MI":
        url="http://it.old.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv"%symbol
    else:
        url="http://finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv"%symbol
    line = urlopen(url).readlines()
    print 'lines=',len(line)
    if symbol[-3:]==".MI":
        today=rigadati(line[0],sep=';',ord=[2,5,6,7,1,8])
        for num in range(0,len(today)):
            today[num]=string.replace(today[num],',','.')
    else:
        today=rigadati(line[0],sep=',',ord=[2,5,6,7,1,8])
        today[0]=string.replace(today[0],'"','')
    if string.find(today[0],'/')==1:
        today[0]='0'+today[0]
    if string.find(today[0],'/',3)==4:
        print today[0]
        today[0]=today[0][:3]+'0'+today[0][3:]
    appdata=datafl(today[0],fmt='mm/gg/aaaa')
    print 'appdata',appdata
    if appdata<>l[0][-1]:
        l[0].append(appdata)
        for x in range(1,6):
            l[x].append(float(today[x]))
    return(l)

def aprimsn2(symbol,symb_yahoo=0,per=12):
    """ scarica le quotazioni da msn, per è il periodo di riferimento e
    può essere: 12 (1 anno), 6, 3, 1 (per i mesi)
    symb_yahoo serve per aggiornare co n idati odierni"""
##    url_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?Symbol=%s&FileDownload=&C1=2&C2=&C5=1&C6=2000&C7=%d&C8=%d&C9=0&CE=0&CF=0&D3=0&D4=1&D5=2"#%(symbol,mese_corrente,anno_corrente)
##    today=datetime.datetime.today()
##    url=url_csv%(symbol,today.month,today.year)
    #print 'in msn2',symbol,symb_yahoo
    if per==6:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=%s&C1=1&C2=0&C3=6&C4=2&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    elif per==3:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=&C1=1&C2=0&C3=3&C4=2&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    elif per==1:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=IT:F&C1=0&C2=0&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    else:#suppongo un anno per qualsiasi altro valore di per
        url_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=%s&C1=1&C3=333&C4=0&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    url=url_csv%(symbol)
    #print 'url',url
    st_dati=urlopen(url).readlines()
    #print len(st_dati)
    l=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f')]
    if len(st_dati)>0:
        x=0
        while x<len(st_dati)and(st_dati[x][:5]<>'DATE,'):
            x+=1
        if x<len(st_dati):
            #x+1 indica la posizione dell'inizio delle quotazioni
            for z in st_dati[x+1:]:
                app_st=string.replace(z,'\r\n','')
                elem=app_st.split(',')
                [mm,gg,aa]=map(int,elem[0].split('/'))
                l[0].append(datetime.datetime(aa,mm,gg))
                for y in range(1,6):
                    l[y].append(float(elem[y]))
    #le quotazioni di msn non contengono quelle attuali quindi le cerco su yahoo
    if symb_yahoo:
        #aggiungo eventuali dati odierni
        l_today=yahoo_today(symb_yahoo)
        print 'l_today_m',l_today
        if len(l[0])>0:
            if l_today[0]<>l[0][0]:
                for x in range(0,len(l_today)):
                    l[x].insert(0,l_today[x])
        else:
            for x in range(0,len(l_today)):
                    l[x].append(l_today[x])
                    #print 'inserimento',l_today[x]
    #msn fornisce quotazioni dalla piu' recente alla piu' remota
    for x in range (0,len(l)):
        l[x].reverse()
    return(l)

def aprimsn(symbol,symb_yahoo=0,per=12):
    """ scarica le quotazioni da msn, per è il periodo di riferimento e
    può essere: 12 (1 anno), 6, 3, 1 (per i mesi)
    symb_yahoo serve per aggiornare co n idati odierni"""
##    url_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?Symbol=%s&FileDownload=&C1=2&C2=&C5=1&C6=2000&C7=%d&C8=%d&C9=0&CE=0&CF=0&D3=0&D4=1&D5=2"#%(symbol,mese_corrente,anno_corrente)
##    today=datetime.datetime.today()
##    url=url_csv%(symbol,today.month,today.year)
    if per==6:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=%s&C1=1&C2=0&C3=6&C4=2&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    elif per==3:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=&C1=1&C2=0&C3=3&C4=2&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    elif per==1:
        ulr_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=IT:F&C1=0&C2=0&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    else:#suppongo un anno per qualsiasi altro valore di per
        url_csv="http://data.moneycentral.msn.com/scripts/chrtsrv.dll?symbol=%s&C1=1&C3=333&C4=0&D5=0&D2=0&D4=1&width=612&height=258&CE=0&filedownload="
    url=url_csv%(symbol)
    st_dati=urlopen(url).readlines()
    x=0
    while st_dati[x][:5]<>'DATE,':
        x+=1
    #x+1 indica la posizione dell'inizio delle quotazioni
    l=[[],array.array('f'),array.array('f'),array.array('f'),array.array('f'),array.array('f'),]
    for z in st_dati[x+1:]:
        app_st=string.replace(z,'\r\n','')
        elem=app_st.split(',')
        [mm,gg,aa]=map(int,elem[0].split('/'))
        l[0].append(datetime.datetime(aa,mm,gg))
        for y in range(1,6):
            l[y].append(float(elem[y]))
    #le quotazioni di msn non contengono quelle attuali quindi le cerco su yahoo
    if symb_yahoo:
        if symb_yahoo[-3:] in [".MI",".mi"]:
            #print 'mi'
            url="http://it.old.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv"%(symb_yahoo)
            sep=";"
            st_dati=urlopen(url).readlines()
            st_dati[0]=string.replace(st_dati[0],',','.')
        else:
            url="http://finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1t1c1ohgv&e=.csv"%(symb_yahoo)
            sep=","
            st_dati=urlopen(url).readlines()
        st_dati[0]=string.replace(st_dati[0],'\n','')
        st_dati[0]=string.replace(st_dati[0],'\r','')
        elem=st_dati[0].split(sep)
        elem[2]=string.replace(elem[2],'"','')
        [mm,gg,aa]=map(int,elem[2].split('/'))
        data=datetime.datetime(aa,mm,gg)
        if data<>l[0][0]:#se la data e' la stessa vuol dire che non davo aggiornare la quotazione
            l[0].insert(0,data)
            l[1].insert(0,float(elem[5]))
            l[2].insert(0,float(elem[6]))
            l[3].insert(0,float(elem[7]))
            l[4].insert(0,float(elem[1]))
            l[5].insert(0,float(elem[8]))
    #al momento riconverto la data in float in seguito lascero' datetime
    for x in range(0,len(l[0])):
        l[0][x]=datafl(l[0][x].strftime('%d/%m/%Y'))
    ##
    #msn fornisce quotazioni dalla piu' recente alla piu' remota
    for x in range (0,6):
        l[x].reverse()
    return(l)

def ftodatetime(f):
    """prende una data daily in float e la converte in datetime"""
    [a,m,g]=ftodate(f)
    return(datetime.datetime(a,m,g))


def ftodate(f):
    """prende una data in formato float e la converte in tupla aaaa,mm,gg"""
    s='%.0f'%f
    gg=int(s[-2:])
    mm=int(s[-4:-2])
    aa=int(s[:-4])+1900
##    if aa<100:
##        aa+=1900
##    else:
##        aa+=1900
    return(aa,mm,gg)

def datafl(dat,fmt="gg/mm/aaaa"):
    """prende una data in testo e la converte in float"""
    #print 'dat',dat
    if fmt in ("gg/mm/aaaa",):
        st=dat[8:]+dat[3:5]+dat[0:2]
    elif fmt in ("gg/mm/aa",):
        st=dat[6:]+dat[3:5]+dat[0:2]
    elif fmt in ("mm/gg/aaaa",):
        st=dat[8:]+dat[0:2]+dat[3:5]
    elif fmt in ('"mm/gg/aa"',):
        st=dat[6:]+dat[0:2]+dat[3:5]
    elif fmt in ("aa/mm/gg"):
        st=dat[:2]+dat[3:5]+dat[6:]
    elif fmt in ("aaaa/mm/gg"):
        st=dat[2:4]+dat[5:7]+dat[8:]
    elif fmt=='dt':#str(datetime)-> AAAA-MM-DD HH:MM:SS
        return(datafl(dat.split(' ')[0],fmt='aaaa/mm/gg'))
    if st[0]=='0':
        st='1'+st
    #print st
    fl=float(st)
    return fl

def troncadate_datetime(applista,d1=0,d2=0):
    #come trocadate ma e' per i dati con date_time nel vettore delle date
    #d1 e d2 sono datetime
    x=0
    #print 'applista',len(applista[0])
    lista=applista
    if d1:
        while lista[0][x]<d1:
            x+=1
        for i in range(0,6):
            lista[i]=lista[i][x:]
    if d2:
        x=0
        while (x<len(lista[0]))and(lista[0][x]<=d2):
            x+=1
        for i in range(0,6):
            lista[i]=lista[i][:x]
    #print 'tdt',len(lista[0])
    return(lista)

def troncadate(applista,msdata1=0,msdata2=0):
    """estrae solo le quotazioni tra le date comprese nell'intervallo dato,\n
    le date sono del tipo 1050815. Ritorna la lista troncata"""
    ###
    if (type(applista[0][0])==type(datetime.datetime.now())):
        if msdata1:
            aa,mm,gg=ftodate(msdata1)
            d1=datetime.datetime(aa,mm,gg)
            #print 'd1',d1
        else:
            d1=0
        if msdata2:
            aa,mm,gg=ftodate(msdata2)
            d2=datetime.datetime(aa,mm,gg)
            #print 'd2',d2
        else:
            d2=0
        lista=troncadate_datetime(applista,d1=d1,d2=d2)    
    ###
    else:
        x=0
        lista=copy.deepcopy(applista)
        if msdata1:
            while lista[0][x]<msdata1:
                x+=1
            for i in range(0,6):
                lista[i]=lista[i][x:]
        if msdata2:
            x=0
            while (x<len(lista[0]))and(lista[0][x]<=msdata2):
                x+=1
                #print len(lista[0]),x
            for i in range(0,6):
                lista[i]=lista[i][:x]
    return(lista)
        
def creamm(vett,g=21,pond=0):
    """calcola la media mobile di un vettore numerico a g giorni,
    ponderata se pond=1,exp se pond=2;ritorna la lista della mm"""

    def exmedexp(vettl):
        """calcola la mmexp di un intero vettore(g=len(vettl))"""
        #e' uguale alla media ponderata!!!!!!!???????
        #print 'exp----------------'
        if len(vettl)==1:
            if (vettl[0]==None)or(vettl[0]==''):
                return(0)
            else:
                return(vettl[0])
        else:
            return(vettl[-1]*(2.00/float(1+len(vettl)))+medexp(vettl[:-1])*(1-2.00/float(1+len(vettl))))

    def media(list,pond):
        if None in list:
            return(None)
        med=0
        if pond==1:
            #print'pond----------------'
            for x in range(0,len(list)):
                med=med+list[x]*(x+1)
            med=float(med)/float(sum(range(1,len(list)+1)))
            return (med)
        elif pond==0:
            med=float(sum(list))/float(len(list))
            return(med)
        elif pond==2:
            return(medexp(list))

    #print 'vett mm',vett
    if pond <>2:        
        mm=[]
        elem=[]
        for x in range(0,len(vett)):
            elem.append(vett[x])
            if x<g-1:
                mm.append(None)
            else:
                if vett[x]<>None:
                    mm.append(media(elem,pond))
                else:
                    mm.append(None)
                del elem[0]
        return(mm)
    elif pond==2:
        #controlla se il parametro g contiene i giorni o un float e in caso converti giorni in float
        if g>=1:
            #print g
            g=2.0/float(g+1)
            #print 'corretto per media exp----------------',g
        ###
        #print 'vett exp',vett[0]
        mm=[vett[0],]
        for x in range(1,len(vett)):
            if (vett[x]<>None)and(mm[x-1]<>None):
                mm.append(float(vett[x])*float(g)+mm[x-1]*(1.0-float(g)))
            else:
                mm.append(vett[x])
        return(mm)

def creabollinger(vett,g=21):
    bolsup=[]
    bolinf=[]
    elem=[]
    for x in range(0,len(vett)):
        elem.append(vett[x])
        if x<g-1:
            bolsup.append(None)
            bolinf.append(None)
        else:
            if vett[x]<>None:
                media=statist.media(elem)
                sigma=pow(statist.varianza(elem),0.5)
                bolsup.append(media+2.0*sigma)
                bolinf.append(media-2.0*sigma)
            del elem[0]
    return(bolsup,bolinf)

def creappw(vett,g=11):
    "pivot point weighting, media mobile ponderata con valori negativi a 2/3 della serie, Kaufmann 73"""
    ini=g-int(round(float(g)/3.0,0))
    weight=[]
    tot=0
    for x in range(0,g):
        weight.append(ini)
        tot+=ini
        ini-=1        
    ppw=[]
    for x in range(0,len(vett)):
        if x<g-1:
            ppw.append(None)
        else:
            prod=0
            for y in range(0,g):
                prod+=(weight[y]*vett[x-y])
            ppw.append(prod/tot)
    return(ppw)

def creavol(vettc,vetth,vettl,g=5,k=3):
    """Volatility System, Kaufmann 96, giorni g fattore k(consigliato 3)"""
    vol=[None,None]
    volsup=[None,None]
    volinf=[None,None]
    D=[]
    for x in range(1,len(vettc)-1):
        D.append(max(abs(vetth[x]-vettc[x-1]),abs(vetth[x]-vettl[x]),abs(vettl[x]-vettc[x-1])))
        if x < (g-1):
            vol.append(None)
            volsup.append(None)
            volinf.append(None)
        else:
            ult=sum(D)/float(g-1)
            vol.append(ult)
            volsup.append(vettc[x]+float(k)*ult)
            volinf.append(vettc[x]-float(k)*ult)
            del D[0]
    return(volsup,volinf,vol)

def creandb(vettc,vetth,vettl,g=5):
    """N-Day Breakout, KAufmann 101, giorni g"""
    pos=0
    ndb=[]
    for x in range(0,len(vettc)):
        if x<g:
            ndb.append(pos)
        else:
            if vetth[x]>max(vetth[x-g:x])and(vettc[x]>vettc[x-1]):
                pos=1
            elif vettl[x]<min(vettl[x-g:x])and(vettc[x]<vettc[x-1]):
                pos=-1
            ndb.append(pos)
    return(ndb)

def creaado(vettc,vetth,vettl,vetto,exp=0.3):
    """A/D Oscillator, Kauffmann 140, exp fatttore mmexp (usare 1 per non mediare)"""
    drf=[]
    for x in range(0,len(vettc)):
        bp=vetth[x]-vetto[x]
        sp=vettc[x]-vettl[x]
        diff=vetth[x]-vettl[x]
        if diff<=0.000001:
            diff=0.0001
        if x>0:
            ult=(bp+sp)/(2.0*(diff))
            ultvet=drf[-1]
            drf.append((ult*exp)+((1-exp)*ultvet))
        else:
            drf.append((bp+sp)/(2.0*(diff)))
    return(drf)

def creakama(vettc,n=10,fast=2,slow=30):
    """KAMA, Kauffman 436, periodo n, media veloce fast 2, media lenta slow 10"""
    vetterr=[]
    kama=[]
    fastest=2.0/(float(fast)+1.0)
    slowest=2.0/(float(slow)+1.0)
    for x in range(0,len(vettc)):
        if x>=1:
            vetterr.append(abs(vettc[x]-vettc[x-1]))
        #vetterr.append
        if x<n-1:
            kama.append(None)
        elif x==n-1:
            kama.append(vettc[x])
        else:
            er=abs(vettc[x]-vettc[x-n+1])/sum(vetterr)
            ultk=kama[-1]
            sc=pow((er*(fastest-slowest)+slowest),2)
            kama.append(ultk+sc*(vettc[x]-ultk))
            del vetterr[0]
    return(kama)
            
def creavidya(vettc,gexp=9,vol_short=9,vol_long=30):
    """Vidya, Kaufmann 438, periodo media exp gexp, volatilita' breve vol_short,
    volatilita' lunga vol_long"""
    s=2.0/(float(gexp)+1.0)
    vidya=[]
    rif=max(gexp,vol_long)
    for x in range(0,len(vettc)):
        if x < rif-2:
            vidya.append(None)
        elif x==rif-2:
            vidya.append(vettc[x])
        else:
            varl=statist.varianza(vettc[x-vol_long+1:])
            vars=statist.varianza(vettc[x-vol_short+1:])
            k=pow(vars,0.5)/pow(varl,0.5)
            ultvidya=vidya[-1]
            vidya.append(k*s*vettc[x]+(1.0-k*s)*ultvidya)
    return(vidya)    

def creamacd(vett,g1=12,g2=26,g3=9):
    """dato un vettore ritorna il macd(mmexp_g1-mmexp_g2) e la sua media mobile a g3
    bande consigliate smoothed:60-40, non smoothed: 80-20"""
    med1=creamm(vett,g=g1,pond=2)
    med2=creamm(vett,g=g2,pond=2)
    macd=[]
    fatti=0
    for x in range(0,len(med1)):
        if (med1[x]<>None)and(med2[x]<>None):
            macd.append(med1[x]-med2[x])
        else:
            macd.append(None)
        fatti+=1
        #print fatti,'fatti'
    mmmacd=creamm(macd,g=g3,pond=2)
    return(macd,mmmacd)

def creapo(vett,g1=12,g2=26,g3=9,pond=2):
    """dato un vettore ritorna il price osci(mm_g1-mm_g2) e la sua media mobile a g3"""
    med1=creamm(vett,g=g1,pond=pond)
    med2=creamm(vett,g=g2,pond=pond)
    macd=[]
    fatti=0
##    print med1,'med1',
##    input('num')
##    print med2,'med2',
##    input('num')
    for x in range(0,len(med1)):
        if (med1[x]<>None)and(med2[x]<>None):
            macd.append(med1[x]-med2[x])
            #print 'd',
        else:
            macd.append(None)
        fatti+=1
        #print fatti,'fatti'
    #print macd[90],'macd'
    if g3:
        mmmacd=creamm(macd,g=g3,pond=pond)
    else:
        mmmacd=[]
    #print 'lib',macd,'lib'
    return(macd,mmmacd)

def creastoc(vett,g=21,gmm=3):
    """dato un vettore ritorna lo stocastico a g giorni e la sua media mobile a gmm"""
    elem=[]
    stoc=[]
    for x in range(0,len(vett)):
        elem.append(vett[x])
        if x<g-1:
            stoc.append(None)
        else:
            maxel=max(elem)
            minel=min(elem)
            if (maxel-minel):
                stoc.append((vett[x]-minel)/(maxel-minel))
            else:
                stoc.append(1)
            del elem[0]
    mmstoc=creamm(stoc,g=gmm)
    return(stoc,mmstoc)

def crearw(vett,g=21):
    """dato un vettore ritorna la %R di William a g giorni"""
    elem=[]
    rw=[]
    for x in range(0,len(vett)):
        elem.append(vett[x])
        if x<g-1:
            rw.append(None)
        else:
            maxel=max(elem)
            minel=min(elem)
            if (maxel-minel):
                rw.append(((maxel-vett[x])/(maxel-minel))*(-100))
            else:
                rw.append(-100)
            del elem[0]
    return(rw)

def crearsi(vett,g=8):
    """dato un vettore ritorna l'rsi a g giorni"""
    #testato,differisce di poco da quello di at2 perche' li' e' considerata la var %
    elem=[]
    rsi=[]
    for x in range(0,len(vett)):
        elem.append(vett[x])
        if x<g:
            rsi.append(None)
        else:
            u=0
            d=0
            for y in range(1,g+1):
                var=elem[y]-elem[y-1]
                if var>=0:
                    u+=var
                else:
                    d-=var
            if d==0:
                rsi.append(100.00)
            else:
                rsi.append(100.00-(100.00/(1.00+u/d)))
            del elem[0]
    return(rsi)

def crearoc(vett,g=10):
    """dato un vettore crea il roc a g giorni"""
    roc=[]
    for x in range(0,len(vett)):
        if x < g:
            roc.append(None)
        else:
            roc.append(100.00*(vett[x]-vett[x-g])/vett[x-g])
    return(roc)

def creasrr(vett,g1=5,g2=10):
    """dato un vettore ne crea lo stocastic relative roc a g1_g2 giorni
    g1 : g short , g2 : g long"""
    srr=[]
    vettmax=[]
    for x in range(0,len(vett)):        
        if x>=g2-1:
            somma=vett[x]/vett[x-g2+1]+vett[x]/vett[x-g1+1]-2
            vettmax.append(abs(somma))
            #print 'aggiunto'
            #print len(vettmax)
        if x<(2*(g1-1)+g2):
            srr.append(None)
        else:
            try:
                app=somma/max(vettmax)
            except:
                srr.append(1)
            else:
                srr.append(app)
            #print len(vettmax)
            del vettmax[0]
            #print 'eliminato'
    return(srr)
            

def creaobv(vclose,vvol,inizio=0):
    vobv=[]
    for x in range(0,len(vvol)):
        if x>inizio:
            if vclose[x]<vclose[x-1]:
                vobv.append(vobv[-1]-vvol[x])
            else:
                vobv.append(vobv[-1]+vvol[x])
        elif x==inizio:
            vobv.append(0.0)
        else:
            vobv.append(None)
    return(vobv)

def creapcicl(vett,g=21,pond=0):
    """dato un vettore ritorna la pista ciclica a g giorni"""
    mm=creamm(vett,g=g,pond=pond)
    pcicl=[]
    for x in range(0,len(vett)):
        if (vett[x]<>None)and(mm[x]<>None):
            pcicl.append((vett[x]-mm[x])/mm[x]*100.00)
        else:
            pcicl.append(None)
    return(pcicl)

def creacoppock(close1,date1,trigger=0):
    """Calcola il coppock index dati i dati di chiusura,ritorna un array, per le date partire da 254+200"""
    #per le date verificare len ci
    #per non modificare i dati in input
    close=copy.deepcopy(close1)
    date=copy.deepcopy(date1)
    ###
    if len(close)<454:
        print 'impossibile calcolare il Coppock Index per insufficenza di dati'
        return(0,0,0)
    else:
        mm=creamm(close,g=20)
        var=[]
        for x in range(254,len(close)):
            var.append(((mm[x]-close[x-254])/close[x-254])*100)
            #if x==254:
             #   print mm[x],close[x-254]
        ci=[]
        for y in range(200,len(var)):
            app=0.0
            for x in range(0,11):
                app+=(1.0-(float(x)/10))*var[y-(x*20)]
            ci.append(app)
        date=date[-(len(ci)):]
##        #per la tesi:        
##        mm=mm[-(len(ci)):]
##        var=var[-(len(ci)):]
##        print 'len',len(ci),len(var),len(date)
##        fd=open('coppock.txt','w')
##        for x in range(0,len(ci)):
##            fd.write('%.0f\t%f\t%f\t%f\t%.5f\n'%(date[x],mm[x],close[x+200],var[x],ci[x]))
##        fd.close()
##        ##fine tesi
        if trigger:
            return(date,ci,creamm(ci,g=trigger))
        else:
            return(date,ci)
        
def creameisels(vett,gg=10):
    """ritorna l'indice di meisels dati un vettore e i giorni di calcolo"""
    meis=[]
    for x in range(0,len(vett)):
        if x>=gg:
            ups=0
            downs=0
            for y in range(0,gg):
                if vett[x-y]<vett[x-y-1]:
                    downs+=1
                else:
                    ups+=1
            meis.append((float(ups-downs)/float(gg))*100.0)            
        else:
            meis.append(None)
    return(meis)

def creacci(vettclose,vettmax,vettmin,n=21):
    """ritorna il vettore cci dati close,max, min e n"""
    pivot=[]
    for x in range(0,len(vettclose)):
        pivot.append((vettclose[x]+vettmax[x]+vettmin[x])/3.0)
    mms=creamm(pivot,g=n)
    varabs=[]
    for x in range(0,len(pivot)):
        if mms[x]==None:
            varabs.append(None)
        else:
            md=0.0
            for y in range(0,n):
                md+=abs(mms[x]-pivot[x-y])
            md/=float(n)
            if md<>0.0:
                varabs.append(md)
            else:
                varabs.append(0.0001)
    #print 'len p m va',len(pivot),len(mms),len(varabs)
    cci=[]
    for x in range(0,len(pivot)):
        if varabs[x]<>None:
            cci.append((pivot[x]-mms[x])/(0.015*varabs[x]))
            #per la tesi
            #print pivot[x],'\t',mms[x],'\t',cci[x]
            #pivot[x]-mms[x],abs(pivot[x]-mms[x]),0.015*abs(pivot[x]-mms[x]),(pivot[x]-mms[x])/(0.015*abs(pivot[x]-mms[x]))
        else:
            cci.append(None)
##    for x in range(len(cci)-100,len(cci)):
##        print cci[x], pivot[x],mms[x]
        
    return(cci)

def crea_regular(vettmax,vettmin,vettclose,vettopen,n=20):
    """ritorna il vettore della regolarita'"""
    #serve per stabilire se l'andamento di un titolo segue un andamento regolare
    #assegnando un punteggio in base alla posizione dei massimi e minimi e chiusure
    #in andamento crescente o decrescente
    
    def def_trend(vettmax,vettmin):
        """stabilisce se un trend in base a 2 quotazioni
            ritorna 1,-1,0 se trend pos, neg o incerto"""
        if (vettmax[1]>=vettmax[0])and(vettmin[1]>=vettmin[0]):
            return(1)
        elif (vettmax[1]<=vettmax[0])and(vettmin[1]<=vettmin[0]):
            return(-1)
        else:
            return(0)
        
    def punteggio(trend,vett_h,vett_l,c,o):
        """determina il punteggio di regolarita' della'ultima candela"""
        punti=0.0
        if trend==1:
            if vett_h[1]>=vett_h[0]:
                punti+=1.0
            else:
                punti-=1.0
            if vett_l[1]>=vett_l[0]:
                punti+=1.0
            else:
                punti-=1.0
            if c>=o:
                punti+=0.5
            else:
                punti-=0.5
        if trend==-1:
            if vett_h[1]<=vett_h[0]:
                punti+=1.0
            else:
                punti-=1.0
            if vett_l[1]<=vett_l[0]:
                punti+=1.0
            else:
                punti-=1.0
            if c<o:
                punti+=0.5
            else:
                punti-=0.5
        return(punti)
        
    vett_regular=[]
    max_reg=float(n)*2.5
    trend=0
    app_regular=[]
    for x in range(0,len(vettmax)):
        #le prime 2 candele servono per determinare il trend
        if x>=2:
            trend=def_trend(vettmax[x-2:x],vettmin[x-2:x])
            app_regular.append(punteggio(trend,[vettmax[x-1],vettmax[x]],
                                         [vettmin[x-1],vettmin[x]],
                                         vettclose[x],vettopen[x]))
        if x>=n+1:
            #print app_regular
            vett_regular.append(float(sum(app_regular))/max_reg)
            del app_regular[0]
        else:
            vett_regular.append(None)
    return(vett_regular)

def creasar(vmax,vmin):
    """ritorna il vettore sar dati i vettori di max e min"""
    
    ls=1
    af=0.0
    max=0.0
    min=vmax[0]*2.0
    sar=[(vmax[0]+vmin[0])/2.0*0.96,]
    for x in range(0,len(vmax)):
        if ls:
            #long
            if vmin[x]<min:
                min=vmin[x]
            if vmax[x]>max:
                af+=0.02
                max=vmax[x]            
            elif abs(af)<0.000001:
                af=0.02                    
            if af>0.2:
                af=0.2
            if (vmin[x]>=sar[x]):
                app=sar[x]+(max-sar[x])*af
                ###
                lower=vmin[x]
                if x>=1:
                    if vmin[x-1]<lower:
                        lower=vmin[x-1]
                ###
                if app>lower:
                    sar.append(lower)
                else:
                    sar.append(app)
            else:#vai short
                min=vmax[x]*2.0
                ls=0
                sar.append(max)
                max=0.0
                af=0.0
        else:
            #short
            if vmax[x]>max:
                max=vmax[x]
            if vmin[x]<min:
                af+=0.02
                min=vmin[x]            
            elif abs(af)<0.000001:
                af=0.02                    
            if af>0.2:
                af=0.2
            if (vmax[x]<=sar[x]):                
                app=sar[x]-(sar[x]-min)*af
                ###
                higth=vmax[x]
                if x>=1:
                    if vmax[x-1]>higth:
                        higth=vmax[x-1]
                ###
                if app<higth:
                    sar.append(higth)
                else:
                    sar.append(app)
            else:#vai long
                max=0.0
                ls=1
                sar.append(min)
                min=vmax[x]*2.0
                af=0.0
    return(sar[1:])

def creadmi(vclose,vmax,vmin,g=21,pond=2,adx=0):
    """crea i vettori +di, -di, adx del dmi"""
    #calcolo i dm + e - e tr
    pdm=[None,]
    ndm=[None,]
    tr=[None,]
    for x in range (1,len(vmax)):
        papp=0
        napp=0
        if vmax[x]>vmax[x-1]:
            papp=vmax[x]-vmax[x-1]
        if vmin[x]<vmin[x-1]:
            napp=vmin[x-1]-vmin[x]
        if papp>=napp:
            napp=0
        else:
            papp=0
        #controllo per correttezza
        if (abs(napp)<0.0000001) and (abs(papp)<0.0000001):
            #papp=vmax[x-1]*0.001
            papp=0.00000001
            napp=0
        pdm.append(papp)
        ndm.append(napp)
        #tr
        #per errori della base dati trma puo' essere zero quindi si suppone
        #un incremento del 0.1% del max rispetto alla chiusura precedente
        apptr=max(vmax[x]-vmin[x],abs(vmax[x]-vclose[x-1]),abs(vclose[x-1]-vmin[x]))
        if apptr==0:
            apptr=vclose[x-1]*0.001
        tr.append(apptr)
    #medie mobili
    pdmma=creamm(pdm,g=g,pond=pond)
    ndmma=creamm(ndm,g=g,pond=pond)
    trma=creamm(tr,g=g,pond=pond)
    #pdi e ndi
    pdi=[]
    ndi=[]
    for x in range(0,len(trma)):
##        if trma[x]==0:
##            print trma
##            print 'x',x
##            print 'trma',trma[x]
##            for y in range(0,g):
##                print 'tr',tr[x-y]
##            print 'vmax',vmax[x]
##            print 'vmin',vmin[x]
        if pdmma[x]<>None:
            #print 'trma',trma[x]
            pdi.append(pdmma[x]/trma[x])
            ndi.append(ndmma[x]/trma[x])
        else:
            pdi.append(None)
            ndi.append(None)
    if adx==0:
        return(pdi,ndi)
    else:
        #dx
        dx=[]
        for x in range(0,len(ndi)):
##            if (pdi[x]==0) and (ndi[x]==0):
##                print 'x',x
            if ndi[x]<>None:
                dx.append(abs(pdi[x]-ndi[x])/(pdi[x]+ndi[x]))
            else:
                dx.append(None)
        #adx
        adx=creamm(dx,g=g,pond=pond)
        #print 'in dmi:',len(vclose),len(dx),len(adx)
        return(pdi,ndi,dx,adx)

def creapend(vett,g=5,):#mm_exp=1):
    """restituisce la pendenza (b) della retta interpolante delle ultime g quotazioni"""
    vett_app=[]
    x=0
    while vett[x]==None:#se passo un vettore con None iniziale aggiungo None
        vett_app.append(None)
        x+=1
    vclose=vett[x:]
    pend=[]
    for x in range(0,g-1):
        pend.append(None)
    asc=range(0,g)
    for x in range(g-1,len(vclose)):
        pend.append(statist.a_b(asc,vclose[x-g+1:x+1])[1])
    #print 'len pend=',len(pend)
##    if mm_exp>1:
##        pend=creamm(pend,g=mm_exp,pond=2)
    return(vett_app+pend)

def creapendo(vclose,g1=3,g2=8,gmm=5):
    """simile al po ma e' dato dall'incrocio di 2 pendenze,
    una mm come trigger e la pendenza del pendo"""
    #utilizzo
    #1: compra se pendo > mm_pendo
    #2: compra se pend_pendo > 0
    #3: compra se entrambe le precedenti
    #4: shorta nei casi opposti
    pend1=creapend(vclose,g=g1)
    pend2=creapend(vclose,g=g2)
    diff=[]
    for x in range(0,len(pend2)):
        if pend2[x]<>None:
            #print pend1[x],pend2[x]
            diff.append(pend1[x]-pend2[x])
        else:
            diff.append(None)
    mm=creamm(diff,g=gmm,pond=0)
    pp=creapend(diff,g=gmm)
    return(diff,mm,pp)

    
def creacv(vclose,g=5):
    """crea il vettore campo di variazione g giorni"""
    cv=[]
    for x in range(0,len(vclose)):
        if x >=g:
            med,var=statist.media_var(vclose[x-g+1:x+1])
            cv.append(var/med)
        else:
            cv.append(None)
    return(cv)

def creavp(vmax,vmin):
    """crea il vettore delle variazioni percentuali max-min di ogni gg"""
    vp=[]
    for x in range(0,len(vmax)):
        vp.append((vmax[x]/vmin[x]-1.0)*100.0)
    return(vp)

def creavol_ud(close,vol,g=30):
    #calcola il rapporto di un periodo di g giorni tra il numero di gg
    #in cui variazioni positive della chiusura si accompagnano a incrementi di volume
    #e il numero di giorni in cui variazioni negative si accompagnano a incrementi di volume
    #utile per individuare fasi di tendenza
    vol_ud=[]
    for x in range(0,len(vol)):
        if x>g-1:
            if (close[x]>close[x-1])and(vol[x]>vol[x-1]):
                up+=1
            elif (close[x]<=close[x-1])and(vol[x]>vol[x-1]):
                down+=1
            if (close[x-g]>close[x-g-1])and(vol[x-g]>vol[x-g-1]):
                up-=1
            elif (close[x-g]<=close[x-g-1])and(vol[x-g]>vol[x-g-1]):
                down-=1
            somma=up+down
            if somma>0:
                vol_ud.append((float(up)-float(down))/float(somma))
            else:
                vol_ud.append(0.0)
        elif x==g-1:
            up=0
            down=0
            for y in range(1,x):
                if (close[y]>close[y-1])and(vol[y]>vol[y-1]):
                    up+=1
                elif (close[y]<=close[y-1])and(vol[y]>vol[y-1]):
                    down+=1
            somma=up+down
            if somma>0:
                vol_ud.append((float(up)-float(down))/float(somma))
            else:
                vol_ud.append(0.0)
        elif x<g-1:
            vol_ud.append(None)
    return(vol_ud)

def creavol_ud_val(close,vol,g=30):
    #calcola il rapporto "tra il valore" di un periodo di g giorni tra il numero di gg
    #in cui variazioni positive della chiusura si accompagnano a incrementi di volume
    #e il numero di giorni in cui variazioni negative si accompagnano a incrementi di volume
    #utile per individuare fasi di tendenza
    vol_ud=[None,]
    up=[]
    down=[]
    for x in range(1,len(vol)):
        if (close[x]>close[x-1])and(vol[x]>vol[x-1]):
            up.append((close[x]-close[x-1])*(vol[x]-vol[x-1]))
        elif (close[x]<close[x-1])and(vol[x]>vol[x-1]):
            down.append((close[x-1]-close[x])*(vol[x]-vol[x-1]))
        if x>g:
            sup=sum(up)
            sdo=sum(down)
            s=sup+sdo
            #print sup,sdo,s
            if s>0:
                vol_ud.append((sup-sdo)/s)
            else:
                vol_ud.append(0)
            if (close[x-g]>close[x-g-1])and(vol[x-g]>vol[x-g-1]):
                del up[0]
            elif (close[x-g]<close[x-g-1])and(vol[x-g]>vol[x-g-1]):
                del down[0]
        else:
            vol_ud.append(None)
        #print close[x],vol[x]
        #print up
        #print down
        #raw_input('ts')
    return(vol_ud)

def creapfe(close,g=10,gme=5):
    #polarized fractal efficency giorni g e mmexp a gme
    unitario=[]
    pfe=[]
    for x in range(1,len(close)):
        unitario.append(pow((pow(close[x]-close[x-1],2)+1.0),0.5))
        if x>=g:
            tot=pow(pow(close[x]-close[x-g],2)+pow(g,2),0.5)
            elem=tot/sum(unitario)
            #print x,unitario,tot,sum(unitario),elem
            if close[x]<close[x-g]:
                elem=-elem
            pfe.append(elem)
            del unitario[0]
    ema_pfe=[]
    for x in range(0,g):
        ema_pfe.append(None)
    #return(ema_pfe+pfe)
    ema_pfe=ema_pfe+creamm(pfe,g=gme,pond=2)
    return(ema_pfe)
    
def crean_candle(vmax,vmin,n=3):
    """opera sulla rottura delle n candele precedenti"""
    n_candle=[]
    for x in range(0,len(vmax)):
        if x>=n:
            if vmax[x]>max(vmax[x-n:x]):
                n_candle.append(min(vmin[x-n:x]))
            elif vmin[x]<min(vmin[x-n:x]):
                n_candle.append(max(vmax[x-n:x]))
            else:
                if n_candle[-1]>=max(vmax[x-n:x]):
                    n_candle.append(max(vmax[x-n:x]))
                else:
                    n_candle.append(min(vmin[x-n:x]))
        else:
            n_candle.append(None)
    return(n_candle)

def crean_candle_c(vmax,vmin,n=3):
    """opera sulla rottura delle n candele precedenti,costruisce i canali max/min"""
    n_candle_up=[]
    n_candle_do=[]
    for x in range(0,len(vmax)):
        if x>=n:
            n_candle_up.append(max(vmax[x-n:x]))
            n_candle_do.append(min(vmin[x-n:x]))
        else:
            n_candle_up.append(None)
            n_candle_do.append(None)
    return(n_candle_up,n_candle_do)

def crean_candle_prova(vmax,vmin,n=3):
    """opera sulla rottura delle n candele precedenti"""
    n_candle=[]
    for x in range(0,len(vmax)):
        if x>=n-1:
            if vmax[x]>max(vmax[x-n+1:x+1]):
                n_candle.append(min(vmin[x-n+1:x+1]))
            elif vmin[x]<min(vmin[x-n+1:x+1]):
                n_candle.append(max(vmax[x-n+1:x+1]))
            else:
                if n_candle[-1]>=max(vmax[x-n+1:x+1]):
                    n_candle.append(max(vmax[x-n+1:x+1]))
                else:
                    n_candle.append(min(vmin[x-n+1:x+1]))
        else:
            n_candle.append(None)
    return(n_candle)

def creab_off(vopen,vmax,vmin,vclose,g=1):
    #"""blast_off di william"""
    c_o=[]
    h_l=[]
    b_off=[]
    for x in range(0,len(vclose)):
        c_o.append(abs(vclose[x]-vopen[x]))
        h_l.append(vmax[x]-vmin[x])
        if x>=g-1:
            den=sum(h_l)
            if den==0:
                den=0.0001
##            print x
##            print c_o
##            print h_l
            b_off.append(sum(c_o)/den)
            del c_o[0]
            del h_l[0]
        else:
            b_off.append(None)
    return(b_off)

def creaintervallo(vopen,vmax,vmin,g=1):
    #previsione dell'intervallo max min
    intervalli=[]
    vett_max=[]
    vett_min=[]
    for x in range(0,len(vopen)):
        intervalli.append(vmax[x]-vmin[x])
        if x>=g:
            int_prev=sum(intervalli[-g:])/float(g)
            vett_max.append(vopen[x]+int_prev/2.0)
            vett_min.append(vopen[x]-int_prev/2.0)
        else:
            vett_max.append(None)
            vett_min.append(None)
    print 'len int',len(vett_max),len(vett_min)
    return(vett_max,vett_min)

def creavar(l,g=5):
    """prende l e ritorna il vettore delle previsioni a 1 giorno con un modello di
    regressione lineare multipla a g giorni"""
    var=[]
    for x in range(0,len(l[4])):
        if x>g:
            try:
                reg=lm(l[4][x-g:x],[l[1][x-g-1:x-1],l[2][x-g-1:x-1],l[3][x-g-1:x-1],l[4][x-g-1:x-1],])
            except:
                var.append(None)
            else:
                #print reg
                b,a=reg[0],reg[1]                   
                var.append(float(a)+float(b.T*mat([l[1][x-1],l[2][x-1],l[3][x-1],l[4][x-1],]).T))
        else:
            var.append(None)            
    return(var)


#plot    
def lplot(ll):
    """prende una lista di liste da plottare,controlla che siano di uguale lunghezza,
    ritorna le liste di ascisse e ordinate depurate da valori None"""
    for x in range(0,len(ll)):
        if len(ll[0])<>len(ll[x]):
            #print 'in lplot 0'
            return([[],[]])
    lx=[]
    ly=[]
    for x in ll:
        ord=[]
        asc=[]
        cont=0
        for y in x:
            if y<>None:
                asc.append(cont)
                ord.append(y)
            cont+=1
        lx.append(asc)
        ly.append(ord)
    #print 'in lplot',len(lx),len(ly)
    return(lx,ly)

def lplotdate(vettdate,vett):
    """prende un vettore di date e uno da plottare e li sistema per il plottaggio,
    ritorna i 2 vettori sistemati"""
    if len(vettdate)<>len(vett):
        print 'errore, lunghezza dei vettori diversa'
        return([],[])
    else:
        plotdate=[]
        plotvett=[]
        for x in range(0,len(vett)):
            if vett[x]<>None:
                plotdate.append(vettdate[x])
                plotvett.append(vett[x])
        return(plotdate,plotvett)

    
def mplotdate(dvf,graf='plot2',locator=3,rot=45,clf=0,save=1):
    """dvf=[[date,vett,plotformat],[....]]; crea il grafico graf"""
    import time
    import datetime
    import matplotlib.matlab as mm
    import matplotlib.dates as md
    import matplotlib.ticker as mt
    import random

    for y in dvf:
        vettdate=[]        

        for x in range(0,len(y[0])):
            #print date[x],x
            app=ftodate(y[0][x])
            #print app
            vettdate.append(time.mktime(datetime.datetime(app[0],app[1],app[2]).timetuple()))
        conv=md.EpochConverter()
        #conv=md.num2epoch    
        ax=mm.subplot(111)
        if len(y)<3:
            f='b-'
        else:
            f=y[2]
        mm.plot_date(vettdate,y[1],conv,fmt=f)                          
        
    days=mt.DayLocator()
    weeks=mt.WeekdayLocator(1)
    mesi=mt.MonthLocator(locator)

    ax.xaxis.set_major_locator(mesi)
    formatter=mt.DateFormatter('%m/%y')
    formatminor=mt.DateFormatter('%m')
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_locator(mt.NullLocator())
    #ax.xaxis.set_minor_formatter(formatminor)
    #mm.show()
    mm.set( ax.get_xticklabels(), 'rotation', rot, 'horizontalalignment', 'right')
    #os.chdir('D:\\SURFER\\BORSA')
    ##vettdate=vettdate[20:]
    ##mm.plot(vettdate,xy[1][0])
    if save:
        mm.savefig(graf)
    if clf:
        mm.clf()

#lm = linear model : risolve con i minimi quadrati un sistema lineare,
# serve per fare una regressione lineare multipla o var, utilizza scipy
#esempio di uso e previsione
#regress=lm(vett,[ascisse,ascisse2])
#        [b,a]=regress[0:2]
#        err.append(regress[3][1])
#        prev.append(float(a)+float(b.T*mat([float(n+n_prev),float(pow((n+n_prev),2))]).T))
def lm(y,arr_arr,intercept=1):
    """
    y is a num observations array of independent variables: a list or array or mat.
    arr_arr : a list of lists or arrays
    int: set to zero if you don't want intercept (intercept is zero)
    
    Perform a multiple linear regression of y onto vectors in arr_arr. arr_arr is
    trasformed to matrix X. If int=1 a column of ones to generate the intercept
    is added to X.  
    
    return value B (array), intercept (number), residuals (array), stats (list)

    B: the regression coeffients;  Ypred = B.T * X.T
    residuals: array( y - Ypred.T)
    stats = Rsquared, F, p
    
    """

    # regression coeffs are given by (Xt*X)-1*Xt*y
    Y = mat(y)
    if intercept==1:
        arr_arr.append([1]*len(y))
    X = mat(arr_arr).T
    #print 'x',type(X),X
    #print 'y',type(y),y
    N = X.shape[0]
    Y.shape = N, 1
    Xt = X.T
    Xt_X_i = mat((Xt*X).I)
    B = Xt_X_i*Xt*Y

    Ypred = B.T * Xt
    #residuals = array(Y-Ypred.T)
    CF = N*mean(y,axis=0)**2     # correction factor

    SStotal = float(Y.T*Y-CF)
    SSregress =  float(B.T * Xt * Y - CF)
    SSerror =  SStotal - SSregress

    Rsquared = SSregress/SStotal

    dfTotal = N-1
    dfRegress = len(B)-1
    dfError = dfTotal - dfRegress
    try:
        #print 'controllo 0',SSregress,dfRegress,SSerror,dfError
##        if dfError==0:
##            dfError=0.00000000000001
        F = SSregress/dfRegress / (SSerror/dfError)
    except:
        F=0.00000000000001
        dfError=0.00000000000001
    prob = 1-fcdf(F, dfRegress, dfError)

    stats = Rsquared, F, prob
    
    if intercept==1:
        return B[:-1],B[-1]#,residuals, stats
    else:
        return B,0#,residuals, stats
    

#-----------candele
#funzioni di identificazione candele
def candle_hammer_up(lista,x):
    hammer=0
    var=lista[2][x]-lista[3][x]
    if (lista[1][x]>=lista[2][x]-var*0.2)and(lista[4][x]>=lista[3][x]+var*0.35):
        hammer=1
    elif (lista[1][x]>=lista[3][x]+var*0.35)and(lista[4][x]>=lista[2][x]-var*0.2):
        hammer=1
    elif (lista[1][x]>=lista[2][x]-var*0.33)and(lista[4][x]>=lista[2][x]-var*0.33):
        hammer=1
    return(hammer)

def candle_hammer_down(lista,x):
    hammer=0
    var=lista[2][x]-lista[3][x]
    if (lista[1][x]<=lista[3][x]+var*0.2)and(lista[4][x]<=lista[2][x]-var*0.35):
        hammer=1
    elif (lista[1][x]<=lista[2][x]-var*0.35)and(lista[4][x]<=lista[3][x]+var*0.2):
        hammer=1
    elif (lista[1][x]<=lista[3][x]+var*0.33)and(lista[4][x]<=lista[3][x]+var*0.33):
        hammer=1
    return(hammer)

def candle_hammer(lista,x):
    return(candle_hammer_up or candle_hammer_down)

def candle_topspin(lista,x):
    topspin=0
    var=lista[2][x]-lista[3][x]
    med=(lista[2][x]+lista[3][x])/2.0
    if med-var*0.2<=lista[1][x]<=med+var*0.2:
        if med-var*0.2<=lista[4][x]<=med+var*0.2:
            topspin=1
    return(topspin)

def candle_inside(lista,x):
    inside=0
    if x>=1:
        if lista[2][x-1]>=lista[2][x]:
            if lista[3][x-1]<=lista[3][x]:
                inside=1
    return(inside)
#########
