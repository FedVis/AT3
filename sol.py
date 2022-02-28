import urllib
import string
import pickle
import time

def aggindici():
    print 'agg indici'
    fd=urllib.urlopen('http://newsecambi.soldionline.it/get_data/aggiorna_titoli_popup.txt') 
    buf=fd.read()
    fd.close()

def aggsol():
    print'sol.py'
    l1=[]
    for x in (range(19,28)):#+[4]):
        fd=urllib.urlopen('http://quotazioni.soldionline.it/sezioni/quotazioni_web/index.php?SUBFUNCTION=quotazioni.php&REALTIME=&id_menu_2=2&id_menu_4=&p=30&m='+str(x))
        buf=fd.read()
        fd.close()
        i=string.find(buf,'Tabella Quotazioni')
        ifin=string.find(buf,'</TABLE>',i)
        print 'aggriorna',x
        while (i<ifin)and(i<>-1):
            l=['t','o','h','l','c','v']
            i1=string.find(buf,'</a></TD>',i)
            i2=string.rfind(buf,'>',i,i1)
            print 'titolo:',buf[i2+1:i1],i2,i1
            l[0]=buf[i2+1:i1]
            iii=string.find(buf,':',i1)
            print buf[iii-2:iii+3],' ',
            i=string.find(buf,'</TD>',i1+10)
            i1=string.find(buf,'</TD>',i+5)
            i2=string.rfind(buf,'>',i,i1)
            print '"%s"'%buf[i2+1:i1],buf[i2],buf[i1]
            l[4]=float(string.replace(buf[i2+1:i1],',','.'))
            i1=string.find(buf,'</TD>',i1+5)
            i1=string.find(buf,'</TD>',i1+5)
            i1=string.find(buf,'</TD>',i1+5)
            i1=string.find(buf,'</TD>',i1+5)
            i2=string.rfind(buf,'>',i,i1)
            stapp=string.replace(buf[i2+1:i1],'.','')
            l[5]=float(string.replace(stapp,'-','0'))
            i1=string.find(buf,'</TD>',i1+5)
            i2=string.rfind(buf,'>',i,i1)
            l[1]=float(string.replace(buf[i2+1:i1],',','.'))
            i1=string.find(buf,'</TD>',i1+5)
            i2=string.rfind(buf,'>',i,i1)
            l[2]=float(string.replace(buf[i2+1:i1],',','.'))
            i1=string.find(buf,'</TD>',i1+5)
            i2=string.rfind(buf,'>',i,i1)
            l[3]=float(string.replace(buf[i2+1:i1],',','.'))
            i=string.find(buf,'<TR',i1)
            l1.append(l)
            #print 'record',l
    #######prende gli indici
    fd=urllib.urlopen('http://www.borsaitalia.it/bitApp/quotes.bit?target=DisplayIndex1Lev')
    buf=fd.read()
    fd.close()
    i=string.find(buf,'continua-->')
    i1=string.find(buf,'hours-->',i)
    buf=buf[i:i1]
    #print 'buf',buf
    i=string.find(buf,'href',0)
    #print 'i',i
    while i<>-1:
        i=string.find(buf,'>',i)
        ifin=string.find(buf,'</a>',i)
        l=['t',0,0,0,'c',0]
        l[0]=buf[i+1:ifin]
        i=ifin
        for x in range(0,3):
            i=string.find(buf,'class',i+1)
        i=string.find(buf,'>',i)
        ifin=string.find(buf,'<',i)
        #print i,ifin,buf[i:ifin+1]
        l[3]=float(string.replace(buf[i+1:ifin],'.',''))
        i=string.find(buf,'class',ifin)
        i=string.find(buf,'>',i)
        ifin=string.find(buf,'<',i)
        #print i,ifin,buf[i:ifin+1]
        l[2]=float(string.replace(buf[i+1:ifin],'.',''))
        i=string.find(buf,'class',ifin)
        i=string.find(buf,'>',i)
        ifin=string.find(buf,'<',i)
        #print i,ifin,buf[i:ifin+1]
        l[1]=float(string.replace(buf[i+1:ifin],'.',''))
        i=string.find(buf,'class',ifin)
        i=string.find(buf,'>',i)
        ifin=string.find(buf,'<',i)
        #print i,ifin,buf[i:ifin+1]
        l[4]=float(string.replace(buf[i+1:ifin],'.',''))
        print l
        l1.append(l)
        i=string.find(buf,'href',ifin)
    print'fine aggiorna indici'
    #######
    dat=time.localtime()
    file='1'+str(dat[0])[2:]
    if dat[1]>=10:
        file+=str(dat[1])
    else:
        file+='0'+str(dat[1])
    if dat[2]>=10:
        file+=str(dat[2])
    else:
        file+='0'+str(dat[2])
    fd=open('./agg/'+file,'wb')
    pickle.dump(l1,fd,1)
    fd.close()
    print 'fine aggiornamento .\\agg\\'+file
##    for x in l1:
##        for y in x:
##            if y=='':
##                print '-',
##            else:
##                print y,
##        print

#aggsol()
