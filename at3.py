import Tix
import Tix as Tkinter
#import Tkinter
import Pmw
import string
import tkMessageBox
from m2ipy import m2i
from struct import *
import copy
import pickle
import sol
import sol_rt
import os
import os.path
import correlazione
import stocklib
#import encodings
from Graf2 import Ctitgraf
class Cbuff:
    def __init__(self):
        self.buff=[[],[],[],[],[],[]]

class App:

    def correl(self):
        correlazione.correl(self.Win)

    def exit(self):
        self.Win.destroy()
        #self.Win.quit()

    def fdata(self,fl):
        app=str(fl)
        l=string.find(app,'.')
        if l==-1:
            l=len(app)-1
        fd=app[l-2:l]+'/'+app[l-4:l-2]+'/'+app[l-6:l-4]
        return fd
    
    def center(self,wid):
        self.Win.update_idletasks()
        app=wid.geometry()
        app=app[0:string.find(app,'+')+1]
        app=app+str((wid.winfo_screenwidth()-wid.winfo_width())/2)+'+'+str((wid.winfo_screenheight()-wid.winfo_height())/2)
        wid.geometry(app)

    def apritxtintra(self,path,ind):
        """apre una cartella file di testo intraday"""
        self.titolo=''
        self.num=''
        if ind:
            self.fin.destroy()
        if not(os.path.exists(path)):
            tkMessageBox.showwarning("Attenzione","impossibile trovare un archivio nella cartella:\n"+path)
        else:
            self.svcart.set(path)
            if os.name=='posix':
                #linux
                pathimage=path[string.find(path,'/',1):]
            else:
                #windows
                pathimage=string.replace(path,':','')
                pathimage='-'+string.replace(pathimage,'\\','/')
            pathimage=string.replace(pathimage,'/','-')
            self.pathimage='imp/'+pathimage
            appdir=os.listdir(path)
            list=[]
            for i in os.listdir(path):
                if i[-3:] in ('txt','TXT','Txt','.cq','.CQ'):
                    D1={'num':i,'tipo':'I','nome':i,'first':'','last':'','format':'','simb':''}
                    list.append(D1)
            for x in self.sf2.winfo_children():
                x.destroy()
            i=0
            #print 'len list', len(list)
            
            for x in list:
                lb=Tkinter.Label(self.sf2,text=str(x['num'])+'- '+x['simb']+' '+x['nome'],
                              anchor='w',bg='white',borderwidth=1,relief='sunken',)
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona)
                lb.bind('<Double-1>',self.graf)
                i+=1
            self.listapref()

    def apri_db(self,path,ind):
        """apre un db sqlite3"""
        self.titolo=''
        self.num=''
        if ind:
            self.fin.destroy()
        if not(os.path.exists(path)):
            tkMessageBox.showwarning("Attenzione","impossibile trovare un archivio nella cartella:\n"+path)
        else:
            self.svcart.set(path)
            if os.name=='posix':
                #linux
                pathimage=path[string.find(path,'/',1):]
            else:
                #windows
                pathimage=string.replace(path,':','')
                pathimage='-'+string.replace(pathimage,'\\','/')
            pathimage=string.replace(pathimage,'/','-')
            self.pathimage='imp/'+pathimage
            #appdir=os.listdir(path)
            list=[]
            app_db=stocklib.apridb(path)
            for i in range(0,len(app_db)):
                D1={'num':i,'tipo':'db','nome':app_db[i]['symb'],'first':'','last':'','format':'','simb':app_db[i]['symb']}
                list.append(D1)
            for x in self.sf2.winfo_children():
                x.destroy()
            i=0
            #print 'len list', len(list)
            
            for x in list:
                lb=Tkinter.Label(self.sf2,text=str(x['num'])+'- '+x['simb']+' '+x['nome'],
                              anchor='w',bg='white',borderwidth=1,relief='sunken',)
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona)
                lb.bind('<Double-1>',self.graf)
                i+=1
            self.listapref()
        
    def apri(self,path,ind):
        """apre una cartella con archivio MetaStock"""
        if (self.tipofile==1)or(self.tipofile==2):
            #se il file e' txtintra rimando a aprifiletxtintra
            self.apritxtintra(path,ind)
            return()
        elif (self.tipofile==3):#db sqlite3
            self.apri_db(path,ind)
            return()
        self.titolo=''
        self.num=''
        if ind:
            self.fin.destroy()
        ###yahoo
        if path=='yahoo':
            self.listapref_yahoo()
            return()
        ###msn
        if path=='msn':
            self.listapref_msn()
            return()
        ###
        try:
            fd=open(path+'/MASTER','rb')
        except:
            tkMessageBox.showwarning("Attenzione","impossibile trovare un archivio nella cartella:\n"+path)
        else:
            self.svcart.set(path)
            if os.name=='posix':
                #linux
                pathimage=path[string.find(path,'/',1):]
            else:
                #windows
                pathimage=string.replace(path,':','')
                pathimage='-'+string.replace(pathimage,'\\','/')
            pathimage=string.replace(pathimage,'/','-')
            self.pathimage='imp/'+pathimage
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
                v=unpack('ffc2s14s',buf[(78+i*53):(103+i*53)])
                D1['first']=self.fdata(m2i(v[0]))
                D1['last']=self.fdata(m2i(v[1]))
                D1['format']=v[2]
                D1['simb']=v[4]
                list.append(D1)
            for x in self.sf2.winfo_children():
                x.destroy()
            i=0
            #print 'len list', len(list)
            for x in list:
                lb=Tkinter.Label(self.sf2,text=str(x['num'])+'- '+x['simb']+' '+x['nome'],
                              anchor='w',bg='white',borderwidth=1,relief='sunken')
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona)
                lb.bind('<Double-Button-1>',self.graf)
                i+=1
            self.listapref()

    def copyright(self):
        tkMessageBox.showwarning("Copyright","Attenzione, questo programma e' di proprieta' di \nFederico Visconti (cod.fis.:VSCFRC77C20H501W),\n\
l'uso, la commercializzazione e la copia sono vietate se non espressamente\nautorizzate dallo stesso. I trasgressori possono essere puniti a norma di legge")

    def listapref_yahoo(self):
        self.pathimage='./imp/yahoo'
        for x in self.sf1.winfo_children():
            x.destroy()
        try:
            print 'listapref',self.pathimage+'/pref.txt'
            fd=open(self.pathimage+'/pref.txt','r')
        except:
            print 'except --------------'
        else:
            buf=fd.readlines()
            fd.close()
            i=0
            for x in buf:
                st=string.replace(x,'\n','')
                st=string.replace(st,'\r','')
                lb=Tkinter.Label(self.sf1,text=st,anchor='w',bg='white',borderwidth=1,relief='sunken')
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona1)
                lb.bind('<Double-Button-1>',self.graf)
                i+=1
            self.matrsol=copy.deepcopy(buf)
            self.svsol.set('')

    def listapref_msn(self):
        self.pathimage='./imp/msn'
        for x in self.sf1.winfo_children():
            x.destroy()
        try:
            print 'listapref',self.pathimage+'/pref.txt'
            fd=open(self.pathimage+'/pref.txt','r')
        except:
            print 'except --------------'
        else:
            buf=fd.readlines()
            fd.close()
            i=0
            for x in buf:
                st=string.replace(x,'\n','')
                st=string.replace(st,'\r','')
                lb=Tkinter.Label(self.sf1,text=st,anchor='w',bg='white',borderwidth=1,relief='sunken')
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona1)
                lb.bind('<Double-Button-1>',self.graf)
                i+=1
            self.matrsol=copy.deepcopy(buf)
            self.svsol.set('')
    
                
    def listapref(self):
        for x in self.sf1.winfo_children():
            x.destroy()
        try:
            print 'listapref',self.pathimage+'/pref.txt'
            fd=open(self.pathimage+'/pref.txt','r')
        except:
            pass
        else:
            buf=fd.readlines()
            fd.close()
            i=0
            for x in buf:
                st=string.replace(x,'\n','')
                st=string.replace(st,'\r','')
                ind=string.find(st,'\t')
                if ind==-1:
                    lb=Tkinter.Label(self.sf1,text=st,anchor='w',bg='white',borderwidth=1,relief='sunken')
                else:
                    lb=Tkinter.Label(self.sf1,text=st[:ind],anchor='w',bg='white',borderwidth=1,relief='sunken')
                lb.grid(row=i,column=0,sticky='we')
                lb.bind('<1>',self.seleziona1)
                lb.bind('<Double-Button-1>',self.graf)
                i+=1
            self.matrsol=copy.deepcopy(buf)
            self.svsol.set('')

    def vocesol(self,event):
        for x in self.matrsol:
            print x
        cont=0
        for x in self.matrsol:
            if x[:string.find(x,'-')]==self.num:
                print 'vero1'
                ind=string.find(x,'\t')
                if ind<>-1:
                    print 'vero2'
                    if self.svsol.get()<>x[ind+2:]:
                        print 'vero3'
                        print 'cont=',cont
                        self.matrsol[cont]=x[:ind+1]+self.svsol.get()+'\n'
                        print 'x1: ',x
                        fd=open(self.pathimage+'/pref.txt','w')
                        for y in self.matrsol:
                            fd.write(y)
                            print y
                        fd.close()
                        self.listapref()
                        break

                else:
                    print 'vero11'
                    if self.svsol.get()<>'':
                        print 'vero12'
                        st=string.replace(x,'\n','\t')
                        st=string.replace(st,'\r','')
                        self.matrsol[cont]=st+self.svsol.get()+'\n'
                        print 'x2: ',x
                        fd=open(self.pathimage+'/pref.txt','w')
                        for y in self.matrsol:
                            fd.write(y)
                        fd.close()
                        self.listapref()
                        break
            cont+=1

    def seleziona(self,event):                         
        for x in self.sf1.winfo_children():
                x.configure(bg='white')
        for x in self.sf2.winfo_children():
            x.configure(bg='white')
        event.widget.configure(bg='blue')
        st=event.widget.cget('text')
        self.titolo=st
        i=string.find(st,'-')
        self.num=st[0:i]
        self.svsol.set('')
        self.ensol.configure(entryfield_entry_state='disabled')

    def seleziona1(self,event):
        self.seleziona(event)
        sw=1
        for x in self.matrsol:
            ind=string.find(x,event.widget.cget('text'))
            ind1=string.find(x,'\t')
            if (ind<>-1)and(ind1<>-1):
                self.svsol.set(string.replace(x[ind1+1:len(x)-1],'\r',''))
                sw=0
                break
        if sw:
            self.svsol.set('')
        self.ensol.configure(entryfield_entry_state='normal')
        
    
    def mapri(self):
        self.tipofile=0
        self.fin=Tkinter.Toplevel(self.Win)
        self.fin.title('Apri archivio')
        Tkinter.Label(self.fin,text='inserisci il percorso della cartella da aprire').grid()
        en=Tkinter.Entry(self.fin)
        en.grid(row=1)
        Tkinter.Button(self.fin,text='Ok',command=lambda: self.apri(en.get(),1)).grid(row=2)
        self.center(self.fin)
        self.fin.transient(self.Win)
        self.fin.focus()
        self.fin.grab_set()
        self.fin.wait_window(self.fin)

    def mapritxtintra(self):
        self.tipofile=1
        self.fin=Tkinter.Toplevel(self.Win)
        self.fin.title('Apri archivio')
        Tkinter.Label(self.fin,text='inserisci il percorso della cartella da aprire').grid()
        en=Tkinter.Entry(self.fin)
        en.grid(row=1)
        Tkinter.Button(self.fin,text='Ok',command=lambda: self.apritxtintra(en.get(),1)).grid(row=2)
        self.center(self.fin)
        self.fin.transient(self.Win)
        self.fin.focus()
        self.fin.grab_set()
        self.fin.wait_window(self.fin)

    def mapri_db(self):
        self.tipofile=3
        self.fin=Tkinter.Toplevel(self.Win)
        self.fin.title('Apri db')
        Tkinter.Label(self.fin,text='inserisci il percorso del db da aprire').grid()
        en=Tkinter.Entry(self.fin)
        en.grid(row=1)
        Tkinter.Button(self.fin,text='Ok',command=lambda: self.apri_db(en.get(),1)).grid(row=2)
        self.center(self.fin)
        self.fin.transient(self.Win)
        self.fin.focus()
        self.fin.grab_set()
        self.fin.wait_window(self.fin)

    def mapritxt_matrix2(self):
        self.tipofile=2
        self.fin=Tkinter.Toplevel(self.Win)
        self.fin.title('Apri archivio')
        Tkinter.Label(self.fin,text='inserisci il percorso della cartella da aprire').grid()
        en=Tkinter.Entry(self.fin)
        en.grid(row=1)
        Tkinter.Button(self.fin,text='Ok',command=lambda: self.apritxtintra(en.get(),1)).grid(row=2)
        self.center(self.fin)
        self.fin.transient(self.Win)
        self.fin.focus()
        self.fin.grab_set()
        self.fin.wait_window(self.fin)

        
    def apripref(self,st):
        if self.ivmpref.get():
            self.svcart.set(st)
            if os.name=='posix':
                #linux
                pathimage=st[string.find(st,'/',1):]
            else:
                print 'windows'
                print 'st',st
                pathimage=string.replace(st,':','')
                print pathimage
                pathimage='-'+string.replace(pathimage,'\\','/')
                print pathimage
            pathimage=string.replace(pathimage,'/','-')
            #print 'img',self.pathimage
            self.pathimage='imp/'+pathimage
            self.apri(st,0)
        else:
            fd=open('preferiti.txt','r')
            app=fd.readlines()
            fd.close()
            fd=open('preferiti.txt','w')
            for x in app:
                if x<>(st+'\n'):
                    fd.write(x)
            fd.close()
            self.ivmpref.set(1)
            self.creampref()
        

    def aggpref(self):
        fd=open('preferiti.txt','a')
        fd.write(self.svcart.get()+'\n')
        fd.close()
        self.creampref()

    def creampref(self):
        def addc(p):
            if p<>'':
                st=string.replace(p,'\n','')
                st=string.replace(st,'\r','')
                print st
                self.mpref.add_command(label=st,command=lambda:self.apripref('%s'%st))
        self.menu.delete(2)
        self.mpref.destroy()
        self.mpref=Tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Preferiti",menu=self.mpref,underline=0)
        self.mpref.add_radiobutton(label='Visualizza',value=1,variable=self.ivmpref)
        self.mpref.add_radiobutton(label='Elimina',value=0,variable=self.ivmpref)
        self.mpref.add_command(label="Tabella indicatori",command=self.tabelle)
        self.mpref.add_separator()
        fd=open('preferiti.txt','r')
        app=fd.readlines()
        fd.close()
        print 'app:',app
        for x in range(0,len(app)):
            addc(app[x])

    def graf(self,*args):
        ###
        if self.svcart.get()=='yahoo':
            print 'self.titolo yahoo:',self.titolo
            if os.name=='posix':
                app_path="./yahoo"
            else:
                app_path='yahoo'
            vis=Ctitgraf(self.Win,pathdat=app_path,#self.svcart.get(),
                         num=self.titolo,tit=self.titolo,#num=-1
                         tipofile='yahoo')

        elif self.svcart.get()=='msn':
            print 'self.titolo msn:',self.titolo
            if os.name=='posix':
                app_path="./msn"
            else:
                app_path='msn'
            vis=Ctitgraf(self.Win,pathdat=app_path,#self.svcart.get(),
                         num=self.titolo,tit=self.titolo,#num=-1
                         tipofile='msn')            
        ###
        else:
            def estraitit(st):
                x=6
                while st[x]<>' ':
                    x+=1
                while st[x]==' ':
                    x+=1
                y=-1
                while st[y]==' ':
                    y-=1
                if y==-1:
                    y=len(st)
                else:
                    y+=1
                return st[x:y]
            print 'graf'
            print 'cartella',self.svcart.get()
            print 'numero',self.num
            print 'titolo:',estraitit(self.titolo)+'#'
            print 'completo:',self.titolo
            if self.tipofile==0:
                appnum=int(self.num)
            elif self.tipofile in [1,2,3]:
                appnum=self.num
            vis=Ctitgraf(self.Win,pathdat=self.svcart.get(),
                         num=appnum,tit=estraitit(self.titolo),
                         tipofile=self.tipofile)
  
    def agg(self):
        try:
            fd=open(self.pathimage+'/pref.txt','a')
        except:
            if not os.path.exists(self.pathimage):
                os.mkdir(self.pathimage)
            fd=open(self.pathimage+'/pref.txt','w')
            fd.write(self.titolo+'\n')
            fd.close()
        else:
            fd.write(self.titolo+'\n')
            fd.close()
        self.listapref()

    def rim(self):
        fd=open(self.pathimage+'/pref.txt','r')
        buf=fd.readlines()
        fd.close()
        fd=open(self.pathimage+'/pref.txt','w')
        for x in buf:
            if x[:10] <>self.titolo[:10]:
                fd.write(x)
        fd.close()
        self.listapref()

    def agggiorn(self):
        sol.aggsol()
        
    def agggiorn_rt(self):
        sol_rt.aggsol()

    def creapathimage(self,st):
        if os.name=='posix':
            #linux
            pathimage=st[string.find(st,'/',1):]
        else:
            #print 'windows'
            #print 'st',st
            pathimage=string.replace(st,':','')
            #print pathimage
            pathimage='-'+string.replace(pathimage,'\\','/')
            #print pathimage
        pathimage=string.replace(pathimage,'/','-')
        return(pathimage)
    
    def datafl(self,dat):
        #serve per gli aggiornamenti
        st=dat[6:]+dat[3:5]+dat[0:2]
        if st[0]=='0':
            st='1'+st
        fl=float(st)
        return fl

    def tabelle(self):
        #########
        def estrainumtit(st1):
            ind=string.find(st1,'\t')
            st=st1[:ind]
            x=6
            while st[x]<>' ':
                x+=1
            while st[x]==' ':
                x+=1
            y=-1
            while st[y]==' ':
                y-=1
            if y==-1:
                y=len(st)
            else:
                y+=1
            tit=st[x:y]
            num=st[:string.find(st,'-')]
            vsol=st1[ind+1:]
            vsol=string.replace(vsol,'\n','')
            vsol=string.replace(vsol,'\r','')
            if ind==-1:
                tit=string.replace(tit,'\n','')
                tit=string.replace(tit,'\r','')
                return(num,tit,0)
            else:
                return(num,tit,vsol)
        ############
                   
        fd=open('preferiti.txt','r')
        preferiti=fd.readlines()
        fd.close()
        fd1=open('imp/tab.txt')
        tab=fd1.readlines()
        fd1.close()
        htm1='''<html>
<head>
  <meta http-equiv="content-type"
 content="text/html; charset=ISO-8859-1">
  <title></title>
</head>
<body>
<table cellpadding="2" cellspacing="2" border="1"
 style="text-align: left; width: 100%;">
  <tbody>\n'''
        for j in preferiti:
            st=string.replace(j,'\n','')
            st=string.replace(st,'\r','')
            pathimage=self.creapathimage(st)
            try:
                fd=open('imp/'+pathimage+'/pref.txt','r')
                
            except:
                print 'errore'
                continue
            else:
                buf=fd.readlines()
                fd.close()
                for z in ['data','titolo','quot']:
                    htm1+='<td>%s</td>\n'%z
                for z in tab:
                    htm1+='<td>%s</td>\n'%z
                htm1+='</tr>\n<tr>\n'
                
                print 'imp/'+pathimage+'/pref.txt'
                for y in buf:
                    print estrainumtit(y)
                    num,tit,sol=estrainumtit(y)
                    lstock=stocklib.aprifile(st+'/f%s.dat'%num)
                    #print 'prima data: ',lstock[0][0]
                    #print 'in aggiornamenti'
                    
                    sw=1
                    if sol<>0:
                        if sw:
                            #print 'titolo nei preferiti'
                            agg=os.listdir('./agg')
                            agg.sort()
                            if len(agg)>50:
                                for x in range(0,5):
                                    os.remove('./agg/'+agg[x])
                            rif=lstock[0][-1]
            ##                for k in range(0,7):
            ##                    rif.append(self.l[k][-1])
                            agg=os.listdir('./agg')
                            agg.sort()
                            for x in agg:
                                if float(x)<=rif:
                                    continue
                                fd=open('./agg/'+x,'rb')
                                matr=pickle.load(fd)
                                fd.close()
                                #print 'eeeeeeeeeeeeeeeeeeeeeeeee'
                                sw1=0
                                for y in matr:
                                    #print 'confronto -%s-,-%s-'%(y[0],sol)
                                    if y[0]==sol:
                                        #print'uguali!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                                        l=copy.deepcopy(y)
                                        l[0]=self.fdata(float(x))
                                        sw1=1
                                        break
                                if sw1:
                                    l[0]=self.datafl(l[0])
                                    for k in range(0,6):
                                        lstock[k].append(l[k])
                    #fine aggiornamenti#
                    for k in range(0,6):
                        lstock[k]=lstock[k][-200:]
                    print lstock[0][0],lstock[0][-1]

                    for cont in range(-3,-1,1):
                        htm1+='<tr><td>%.0f</td><td>%s</td><td>%.4f</td>'%(lstock[0][cont+1],tit,lstock[4][cont+1])
                    
                        for z in tab:
                            if z[0]=='#':
                                continue
                            #scrivi su htm1 data e titolo
                            ind=ind0=string.find(z,'\t')
                            ind1=string.find(z,'\t',ind+1)
                            if ind1==-1:
                                g1=int(string.replace(z[ind+1:],'\n',''))
                            else:
                                g1=int(z[ind+1:ind1])
                                ind=ind1
                                ind1=string.find(z,'\t',ind+1)
                                if ind1==-1:
                                    g2=int(string.replace(z[ind+1:],'\n',''))
                                else:
                                    g2=int(z[ind+1:ind1])
                                    ind=ind1
                                    ind1=string.find(z,'\t',ind+1)
                                    if ind1 <> -1:
                                        g3=int(string.replace(z[ind+1:],'\n',''))
                                    
                            if z[:ind0]=='mm':
                                app=stocklib.creamm(lstock[4],g=g1)
                                if (lstock[4][cont]<=app[cont])and(lstock[4][cont+1]>app[cont+1]):
                                    col='0, 102, 0'
                                elif (lstock[4][cont]>=app[cont])and(lstock[4][cont+1]<app[cont+1]):
                                    col='255, 0, 0'
                                else:
                                    col='255,255,255'
                                val=app[cont+1]
                            elif z[:ind0]=='cci':
                                app=stocklib.creacci(lstock[4],lstock[2],lstock[3],n=g1)
                                if (app[cont]<=-100)and(app[cont+1]>-100):
                                    col='0, 102, 0'
                                elif (app[cont]>=100)and(app[cont+1]<100):
                                    col='255, 0, 0'
                                else:
                                    col='255,255,255'
                                val=app[cont+1]
                            elif z[:ind0]=='rsi':
                                app=stocklib.crearsi(lstock[4],g=g1)
                                if (app[cont]<=30)and(app[cont+1]>30):
                                    col='0, 102, 0'
                                elif (app[cont]>=70)and(app[cont+1]<70):
                                    col='255, 0, 0'
                                else:
                                    col='255,255,255'
                                val=app[cont+1]
                            elif z[:ind0]=='stoc':
                                app=stocklib.creastoc(lstock[4],g=g1,gmm=g2)
                                if (app[0][cont]<=app[1][cont])and(app[0][cont+1]>app[1][cont+1]):
                                    col='0, 102, 0'
                                elif (app[0][cont]>=app[1][cont])and(app[0][cont+1]<app[1][cont+1]):
                                    col='255, 0, 0'
                                else:
                                    col='255,255,255'
                                val=app[0][cont+1]
                                

                            g1=g2=g3=0
                            htm1+='<td style="background-color: rgb(%s)">%.4f</td>'%(col,val)

                        htm1+='</tr>\n'
        htm1+='</table>'
                        
        #print htm1
        fd=open('tabelle.html','w')
        fd.write(htm1)
        fd.close()
        import thread
        import webbrowser
        th=thread.start_new_thread(self.vistabelle,())                    

    def vistabelle(self):
        import webbrowser
        webbrowser.open('tabelle.html')
        
    def __init__(self):
        self.Win=Tkinter.Tk()        
        ###
        self.cart='cartella'
        self.ivmpref=Tkinter.IntVar()
        self.ivmpref.set(1)
        self.svcart=Tkinter.StringVar()
        self.svsol=Tkinter.StringVar()
        self.svcart.set('Cartella')
        self.pathimage=('/imp')
        self.svinst=Tkinter.StringVar()
        self.svinst.set('')
        self.num=0
        self.list=[]
        self.titolo=''
        self.matrsol=[]
        self.tipofile=0 #indica il tipo di archivio che si sta utilizzando: 0=metastock,1=txtintraday
        cwd=os.getcwd()
        
        ###
        
        Pmw.initialise(self.Win)
        self.Win.title('AT3 - Analisi Tecnica')
        self.Win.protocol("WM_DELETE_WINDOW",self.exit)
        self.menu=Tkinter.Menu(self.Win)
        self.Win.config(menu=self.menu)
        self.mfile=Tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.mfile,underline=0)
        self.mfile.add_command(label="Apri",command=self.mapri)
        self.mfile.add_command(label="Apri txt intr",command=self.mapritxtintra)
        self.mfile.add_command(label="Apri txt matrix_2",command=self.mapritxt_matrix2)
        self.mfile.add_command(label="Apri db",command=self.mapri_db)
        self.mfile.add_command(label="Aggiornamento giornaliero",command=self.agggiorn)
        self.mfile.add_command(label="Aggiornamento real time",command=self.agggiorn_rt)
        self.mfile.add_separator()
        self.mfile.add_command(label="Esci",command=self.exit)
        self.mpref=Tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Preferiti",menu=self.mpref,underline=0)
        self.creampref()
        self.menu.add_command(label="Copyright",command=self.copyright,underline=0)
        Tkinter.Label(self.Win,textvariable=self.svcart).grid(row=0,column=0)
        Tkinter.Button(self.Win,text='Aggiungi a preferiti',command=self.aggpref).grid(row=0,column=1)
        Tkinter.Label(self.Win,text='Esaminati').grid(row=1,column=0)
        Tkinter.Label(self.Win,text='Disponibili').grid(row=1,column=1)
        self.f1=Pmw.ScrolledFrame(self.Win,vscrollmode='static')
        self.f1.grid(row=2,column=0)
        self.f2=Pmw.ScrolledFrame(self.Win,vscrollmode='static')
        self.f2.grid(row=2,column=1)
        self.sf1=self.f1.interior()
        self.sf2=self.f2.interior()
        Tkinter.Button(self.Win,text='Rimuovi',underline=0,command=self.rim).grid(row=3,column=0)
        Tkinter.Button(self.Win,text='Aggiungi',underline=0,command=self.agg).grid(row=3,column=1)
        Tkinter.Button(self.Win,text='Aggiorna',underline=0,).grid(row=4,column=0)
        Tkinter.Button(self.Win,text='Grafico',underline=0,command=self.graf).grid(row=4,column=1)
        Tkinter.Label(self.Win,text='Voce abbinata a S.O.L.: ').grid(row=5,column=0)        
        Pmw.EntryField(self.Win,labelpos='w',label_text='Agg. Inst. : ',entry_textvariable=self.svinst).grid(row=6,column=1)
        Tkinter.Button(self.Win,text='Correlazione',underline=0,command=self.correl).grid(row=6,column=0)
##        self.ensol=Tkinter.Entry(self.Win,textvariable=self.svsol,state='disabled')
##        self.ensol.grid(row=5,column=1)
##        self.ensol.bind('<Return>',self.vocesol)
        #
        dir=os.listdir('./agg')
        dir.sort()
        dir.reverse()
        print dir
        print 'dir 0:',dir[0]
        fd=open('./agg/'+dir[0],'rb')
        matr=pickle.load(fd)
        fd.close()
        cblist=[]
        for x in matr:
            cblist.append(x[0])
        print 'ensol--------------------------'
        self.ensol=Pmw.ComboBox(self.Win,scrolledlist_items=cblist,entryfield_entry_textvariable=self.svsol,
                                entryfield_entry_state='disabled',selectioncommand=self.vocesol)
        self.ensol.grid(row=5,column=1)
        #
        self.center(self.Win)
        self.Win.minsize(self.Win.winfo_reqwidth(),self.Win.winfo_reqheight())
        self.Win.mainloop()

prog=App()
