import datetime
import Tix 
import Pmw
import string
import stocklib
import pickle
import os
import os.path
import tkMessageBox
import tkColorChooser
from CBlivello import CBlivello
from CBsupres import CBsupres
import copy
from statist import media,varianza,coov

def centrafin(fin,master):
    fin.update_idletasks()
    app=fin.geometry()
    app=app[0:string.find(app,'+')+1]
    app=app+str((fin.winfo_screenwidth()-fin.winfo_width())/2)+'+'+str((fin.winfo_screenheight()-fin.winfo_height())/2)
    fin.geometry(app)
    fin.transient(master)
    fin.focus()
    fin.grab_set()
    fin.wait_window(fin)

def center(fin):
    fin.update_idletasks()
    app=fin.geometry()
    app=app[0:string.find(app,'+')+1]
    app=app+str((fin.winfo_screenwidth()-fin.winfo_width())/2)+'+'+str((fin.winfo_screenheight()-fin.winfo_height())/2)
    fin.geometry(app)

class Cbuff:
    def __init__(self):
        self.buff=[[],[],[],[],[],[]]

class Cimposttit:
    def __init__(self):
        #print 'IMPOSTTITOLI_____________________________'
        """Classe del file che contiene le informazioni per un singolo grafico"""
        self.W=1000
        self.H=150
        self.ndatavis=120
        self.bg='white'
        self.grafkeys=('identificativo','scala','nome','nome2','nome3',
                       'tipo','dati','opzioni','g1','g2','g3','colore','colore2','colore3')
        self.livkeys=('identificativo','scala','nome','quota','colore')
        self.graf={'identificativo':[0,1],
                   'scala':[1,1],
                   'nome':['quot','mm8'],
                   'nome2':['-','-'],
                   'nome3':['-','-'],
                   'tipo':['quot','mm'],
                   'dati':['close','close'],
                   'opzioni':['-','sempl'],
                   'g1':['-',8],
                   'g2':['-','-'],
                   'g3':['-','-'],
                   'colore':['blue','red'],
                   'colore2':['-','-'],
                   'colore3':['-','-'],}
        self.livello={'identificativo':[],'scala':[],'nome':[],'quota':[],'colore':[],'ord':[]}

class Csr:
    def __init__(self):
        self.srkeys=('id','scala','par','data1','p1',
                     'data2','p2','data3','p3','data4','p4',
                     'colore','inizio','fine')
        self.supres={'id':[],
                     'scala':[],
                     'par':[],
                     'data1':[],
                     'p1':[],
                     'data2':[],
                     'p2':[],
                     'data3':[],
                     'p3':[],
                     'data4':[],
                     'p4':[],
                     'colore':[],
                     'inizio':[],
                     'fine':[],
                     'asc':[],
                     'ord':[],
                     'asc-ini':[],
                     'asc-fin':[],
                     'ord-ini':[],
                     'ord-fin':[],
                     'b':[],}

class CBgrafici:
    def csetcb(self,x):
        #print 'set',x
        for y in self.dictcb.keys():
            if y <> 'identificativo':
                #print y,x
                #self.dictcb[y].selectitem(x) self.est.imp[y][x]
                self.dictcb[y]._entryfield.setvalue(str(self.est.imp.graf[y][x]))
    def commop(self,x):
        if x=='M':
            self.dictcb['identificativo'].configure(selectioncommand=self.csetcb)
            self.dictcb['identificativo'].selectitem(0)
            self.csetcb(0)
            pass
                
    def __init__(self,est):
        
        self.est=est
        self.win=Tix.Toplevel(est.win)
        self.win.title(self.est.titolo+'-Grafici')
        self.crea()
        centrafin(self.win,est.win)
        self.win.mainloop()
        
    def crea(self):
        self.w=Tix.ScrolledWindow(self.win,width=300,height=150,scrollbar='auto')
        self.w.grid(row=0,column=0,)
        #print dir(self.op)
        self.dictcb={}
        for x in range(0,len(self.est.imp.grafkeys)):
            if x <>0:
                if self.est.imp.grafkeys[x] in('tipo','dati','opzioni'):
                    scrollist=self.est.opzgraf[self.est.imp.grafkeys[x]]
                elif self.est.imp.grafkeys[x] in('colore','colore2','colore3'):
                    scrollist=self.est.opzgraf['colore']
                else:
                    scrollist=self.est.imp.graf[self.est.imp.grafkeys[x]]
                cb=Pmw.ComboBox(self.w.window,label_text=self.est.imp.grafkeys[x],labelpos='w',
                                scrolledlist_items=scrollist,history=0)
                if self.est.imp.grafkeys[x] in ('colore','colore2','colore3'):
                    cb._entryWidget.bind('<Button-1>',self.colore)
            else:
                cb=Pmw.ComboBox(self.w.window,label_text=self.est.imp.grafkeys[x],labelpos='w',
                                scrolledlist_items=self.est.imp.graf[self.est.imp.grafkeys[x]],
                                entryfield_entry_state='disabled',entryfield_entry_disabledbackground='white',
                                history=0)
            self.dictcb[self.est.imp.grafkeys[x]]=cb
            
            cb.grid(row=x+1,column=0,sticky='we')
        Tix.Button(self.w.window,text='OK',command=self.cbok).grid(row=x+3,column=0)
        self.op=Tix.OptionMenu(self.w.window,command=self.commop,)
        self.op.add_command('M',label='Modifica')
        self.op.add_command('N',label='Nuovo')
        self.op.add_command('E',label='Elimina')
        self.op.grid(row=0,column=0)

    def colore(self,ev):        
        col=tkColorChooser.Chooser(master=self.w,title='Scegli lo sfondo',
                                   initialcolor='black').show()
        
        ev.widget.configure(bg=col[1])
        ev.widget.delete(0,'end')
        ev.widget.insert(0,col[1])
        #centrafin(self.win)
        #self.win.focus()
        

    def chiudiimp(self):
        self.w.destroy()
        self.crea()


    def cbok(self):
        #print self.dictcb['identificativo'].get()
        if self.op.menubutton.cget('text')<>'Elimina':
            for x in self.est.imp.grafkeys:
                if x<> 'identificativo':
                    if x in ['g1','g2','g3','identificativo','scala']:
                        if self.dictcb[x].get()=='-':
                            app=0
                        else:
                            #print self.dictcb[x].get()
                            if not('.' in self.dictcb[x].get()):
                                app=int(self.dictcb[x].get())
                            else:
                                app=float(self.dictcb[x].get())
                        if self.op.menubutton.cget('text')=='Modifica':
                            self.est.imp.graf[x][int(self.dictcb['identificativo'].get())]=app
                        else:
                            self.est.imp.graf[x].append(app)
                    else:
                        if self.op.menubutton.cget('text')=='Modifica':
                            self.est.imp.graf[x][int(self.dictcb['identificativo'].get())]=self.dictcb[x].get()
                        else:
                            self.est.imp.graf[x].append(self.dictcb[x].get())
            if self.op.menubutton.cget('text')=='Nuovo':
                self.est.imp.graf['identificativo'].append(max(self.est.imp.graf['identificativo'])+1)
        else:
            if tkMessageBox.askokcancel('Attenzione','Vuoi eliminare la linea selezionata?',
                                        master=self.w):
                print 'elimina'
                ind=self.est.imp.graf['identificativo'].index(int(self.dictcb['identificativo'].get()))
                #print 'indice=',ind
                del self.est.imp.graf['identificativo'][ind]
                for x in range(ind,len(self.est.imp.graf['identificativo'])):
                    self.est.imp.graf['identificativo'][x]-=1
                for x in self.est.imp.grafkeys:
                    if x<> 'identificativo':
                        del self.est.imp.graf[x][ind]
            else:
                print 'non eliminare'
        self.est.creagraf()
        self.w.destroy()
        self.crea()
        self.win.destroy()
            
        


class Cgraf:

    lines=[]
    vis=1
    opzgraf={'tipo':['quot','candle','ado','cci','coppock','dmi','kama','meis','mm','n_candle','n_candle_c','ndb','bollinger',
                     'pcicl','obv','pend','po','ppw','roc','rsi','r%','sar','stoc','srr','vidya',
                     'volat','volume','cv','b_off','vp','vol_ud','vol_ud_val','pfe','intervallo','var','pendo',
                     'regular',],
             'dati':['close','open','max','min','volume'],
             'opzioni':['sempl','pond','exp'],
             'colore':['white','black','red','green','blue','orange','grey','yellow','pink','brown']}

    def __init__(self,lista,fin,titolo='Capitalia',graf='quot-mm',file='std',num=1):#ldate,lvcn,W=800,H=600,title='Graf'):
        self.path=file
        self.num=num
        self.graf=graf
        self.titolo=titolo
        self.swcandle=-1
        self.punto=''
        ######modifica per adattare a txtintra e non intra
        print 's.num=',self.num
        print 'file',file
        if str(num)[-3:] in ('txt','Txt','TXT','.cq','.CQ'):
            self.filepathimage='imp/'+file+'/%s'%num
        elif '.db' in file:
            self.filepathimage='imp/'+file+'/%s'%num
        elif 'yahoo' in file:
            self.filepathimage='imp/'+file+'/%s'%num
        elif 'msn' in file:
            self.filepathimage='imp/'+file+'/%s'%num
            self.filepathimage=string.replace(self.filepathimage,':','_')
        else:
            self.filepathimage='imp/'+file+'/%d'%num
        ######    
        if (os.path.exists(self.filepathimage+'.imp')) or (file=='std'):
            if file<>'std':
                #print 'apre ',num
                fd=open(self.filepathimage+'.imp','rb')
            else:
                #print 'apre std'
                fd=open('imp/std.imp','rb')
            self.imp=pickle.load(fd)
            fd.close()
            if self.graf in self.imp.keys():
                self.imp=self.imp[graf]
            else:
                self.imp=Cimposttit()
        else:
            #print 'apre Cimposttit'
            #self.imp=Cimposttit()
            #print 'self.imp.W',self.imp.W
            fd=open('imp/std.imp','rb')
            self.imp=pickle.load(fd)
            fd.close()
            if graf in self.imp.keys():
                self.imp=self.imp[graf]
            else:
                self.imp=Cimposttit()

        #apre il file con sr
        if (os.path.exists(self.filepathimage+'.sr')):
            #print 'apre ',num
            fd=open(self.filepathimage+'.sr','rb')
            self.sr=pickle.load(fd)
            fd.close()
            if self.graf in self.sr.keys():
                self.sr=self.sr[graf]
            else:
                self.sr=Csr()
        else:
            self.sr=Csr()
        ###########
        self.W,self.H=self.imp.W,self.imp.H
        #eventuali trasformazioni temporali
        if string.find(self.graf,'#w')<>-1:
            self.l=self.trasforma(lista,opt='w')
        elif string.find(self.graf,'#m')<>-1:
            self.l=self.trasforma(lista,opt='m')
        else:
            self.l=lista
        #self.l=stocklib.troncadate(self.l,msdata1=1030601)
        
        self.win=Tix.Toplevel(fin)
        self.ndativis=Tix.IntVar()
        self.ndativis.set(self.imp.ndatavis)
        self.ultdatavis=Tix.StringVar()
        if type(self.l[0][0])==type(datetime.datetime.now()):
            self.ultdatavis.set(self.l[0][-1].strftime('%Y/%m/%d %H:%M'))
        else:
            self.ultdatavis.set('%.4f'%self.l[0][-1])
            
        self.cv=Tix.Canvas(self.win,width=self.W,height=self.H,bg=self.imp.bg)
        self.cv.grid(row=0,column=0,columnspan=6)

        self.endim=Tix.StringVar()
        self.endim.set('%dx%d'%(self.W,self.H))
        
                       
        
        Tix.Label(self.win,text='Ultima data visualizzata').grid(row=1,column=1)    
        en=Tix.Entry(self.win,textvariable=self.ultdatavis)
        en.grid(row=1,column=2)
        en.bind('<Return>',self.creagraf)
        Tix.Label(self.win,text='N. quotazioni visualizzate').grid(row=1,column=3)    
        en=Tix.Entry(self.win,textvariable=self.ndativis)
        en.grid(row=1,column=4)
        en.bind('<Return>',self.creagraf)
        en.bind('<Up>',self.incrvis)
        en.bind('<Shift-Up>',self.incrvis50)
        en.bind('<Down>',self.decrvis)
        en.bind('<Shift-Down>',self.decrvis50)
        en=Tix.Entry(self.win,textvariable=self.endim)
        en.grid(row=1,column=0)
        en.bind('<Return>',self.creagraf)
        Tix.Button(self.win,text='Grafici',command=self.Bgrafici).grid(row=2,column=0)
        Tix.Button(self.win,text='Livelli',command=self.Blivello).grid(row=2,column=1)
        Tix.Button(self.win,text='Sup-Res',command=self.Bsr).grid(row=2,column=2)
        Tix.Button(self.win,text='Salva',command=self.Bsalva).grid(row=2,column=3)
        Tix.Button(self.win,text='Salva SR',command=self.Bsalvasr).grid(row=2,column=4)
        en=Tix.Label(self.win,text='Sfondo',borderwidth=1,relief='sunken')
        en.grid(row=2,column=5)
        en.bind('<Button-1>',self.sfondo)        
        #print 'ultindex',self.ultimoindex
        self.win.title(titolo+' - '+graf)

        self.creagraf()
        
        self.win.mainloop()

    def incrvis(self,ev):
        """incrementa il numero di quotazioni visualizzate e decrementa la data di partenza, utile per simulazioni"""
        self.ndativis.set(self.ndativis.get()+1)
        ind=self.l[0].index(float(self.ultdatavis.get()))+1
        if ind < len(self.l[0]):
            self.ultdatavis.set('%.4f'%self.l[0][ind])
        self.creagraf()
    def incrvis50(self,ev):
        """incrementa il numero di quotazioni visualizzate e decrementa la data di partenza, utile per simulazioni"""
        self.ndativis.set(self.ndativis.get()+50)
        ind=self.l[0].index(float(self.ultdatavis.get()))+50
        if ind < len(self.l[0]):
            self.ultdatavis.set('%.4f'%self.l[0][ind])
        self.creagraf()
    def decrvis(self,ev):
        """incrementa il numero di quotazioni visualizzate e decrementa la data di partenza, utile per simulazioni"""
        self.ndativis.set(self.ndativis.get()-1)
        ind=self.l[0].index(float(self.ultdatavis.get()))-1
        if ind < len(self.l[0]):
            self.ultdatavis.set('%.4f'%self.l[0][ind])
        self.creagraf()
    def decrvis50(self,ev):
        """incrementa il numero di quotazioni visualizzate e decrementa la data di partenza, utile per simulazioni"""
        self.ndativis.set(self.ndativis.get()-50)
        ind=self.l[0].index(float(self.ultdatavis.get()))-50
        if ind < len(self.l[0]):
            self.ultdatavis.set('%.4f'%self.l[0][ind])
        self.creagraf()
        
    def datatuple(self,d):
        std='%.0f'%d
        anno=int(std[:-4])+1900
        mese=int(std[-4:-2])
        giorno=int(std[-2:])
        return(anno,mese,giorno)

    def datetimefl(self,d):
        anno=float(d.year)-1900.0
        mese=float(d.month)
        giorno=float(d.day)
        dfl=anno*10000.0+mese*100.0+giorno
        return(dfl)

    def trasforma(self,lista,opt='w'):
        lw=[[],[],[],[],[],[]]
        ind=0
        day=datetime.timedelta(days=1)
        while ind<len(lista[0]):
            aa,mm,gg=self.datatuple(lista[0][ind])
            ini=datetime.date(aa,mm,gg)
            #print ini
            if opt=='w':
                while datetime.date.weekday(ini)<>6:
                    ini+=day
            elif opt=='m':
                mese=ini.month
                while ini.month==mese:
                    ini+=day
                ini-=day
            #print ini
            dt=lista[0][ind]
            op=lista[1][ind]
            max=0
            min=999999999999999999999999999999999999
            vol=0.0
            fin=self.datetimefl(ini)
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
        return(lw)            

    def Bsalva(self):
        if not(os.path.exists('imp/'+self.path)):
            os.mkdir('imp/'+self.path)
        if not (os.path.exists(self.filepathimage+'.imp')):
            print 'salvato 1'
            fd=open('imp/std.imp','rb')
            dict=pickle.load(fd)
            fd.close()
            #dict={}
            dict[self.graf]=self.imp
            fd=open(self.filepathimage+'.imp','wb')
            #print 'imp/'+self.path+'/%d.imp'%self.num
            pickle.dump(dict,fd)
            fd.close()
        else:
            print 'salvato 2'
            fd=open(self.filepathimage+'.imp','rb')
            dict=pickle.load(fd)
            fd.close()
            #print 'len',len(self.imp.graf['identificativo']),dict.keys()
            #dict[self.graf]=copy.deepcopy(self.imp)
            dict[self.graf]=self.imp
            fd=open(self.filepathimage+'.imp','wb')
            pickle.dump(dict,fd)
            fd.close()
            print 'salvato:','imp/'+self.path+'/%s.imp'%str(self.num)
            fd=open('imp/'+self.path+'/%s.imp'%string.replace(str(self.num),':','_'),'rb')
            dict=pickle.load(fd)
            fd.close()
            #print dict.keys(),len(dict[self.graf].graf['identificativo'])

    def puliscisr(self):
        for x in ['asc','ord','asc-ini','asc-fin','ord-ini','ord-fin','b']:
            self.sr.supres[x]=[]
            
    def Bsalvasr(self):
        self.puliscisr()
        if not(os.path.exists('imp/'+self.path)):
            os.mkdir('imp/'+self.path)
        if not (os.path.exists('imp/'+self.path+'/%s.sr'%str(self.num))):
            print 'salvato 1'
            dict={}
            dict[self.graf]=self.sr
            fd=open('imp/'+self.path+'/%s.sr'%string.replace(str(self.num),':','_'),'wb')
            #print 'imp/'+self.path+'/%d.imp'%self.num
            pickle.dump(dict,fd)
            fd.close()
        else:
            print 'salvato 2'
            fd=open('imp/'+self.path+'/%s.sr'%str(self.num),'rb')
            dict=pickle.load(fd)
            fd.close()
            #print 'len',len(self.imp.graf['identificativo']),dict.keys()
            #dict[self.graf]=copy.deepcopy(self.imp)
            dict[self.graf]=self.sr
            fd=open('imp/'+self.path+'/%s.sr'%str(self.num),'wb')
            pickle.dump(dict,fd)
            fd.close()
##            print 'salvato:','imp/'+self.path+'/%d.imp'%self.num
##            fd=open('imp/'+self.path+'/%d.imp'%self.num,'rb')
##            dict=pickle.load(fd)
##            fd.close()
##            print dict.keys(),len(dict[self.graf].graf['identificativo'])
        
    def sfondo(self,ev):
        col=tkColorChooser.Chooser(self.win,title='Scegli lo sfondo',
                                   initialcolor='black').show()
        ev.widget.configure(bg=col[1])
        self.imp.bg=str(col[1])
        self.creagraf()
        #self.cv.configure(bg=col[1])

    def Bgrafici(self):
        w=CBgrafici(self)
##        win=Tix.Toplevel(self.win)
        
    def Blivello(self):
        w=CBlivello(self)

    def Bsr(self):
        w=CBsupres(self)
   

    def vischange(self,evento):
        if self.vis:
            self.vis=0
        else:
            self.vis=1
            self.ev(evento)

    def ev(self,evento):
        if self.vis:
            #print type(evento.x)
            ind=int(round(float(evento.x)/self.passo,0))
            if ind>self.ndativis.get()-1:
                ind=self.ndativis.get()-1

            #print 'data',self.ldate[self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1][ind],ind
            self.ballb[0].set('%.4f'%self.l[0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1][ind])
                        
            for x in range(0,len(self.lvcn)):
                #print self.lvcn[x][2],self.lvcn[x][0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1][ind]
                if self.lvcn[x][0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1][ind]<>None:
                    self.ballb[x+1].set('%.4f'%self.lvcn[x][0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1][ind])
                else:
                    self.ballb[x+1].set('-')
            self.cv.delete(self.segno)
            self.segno=self.cv.create_line(self.asc[ind],0,self.asc[ind],self.H,fill='grey')
            #trova il punto del cursore
            try:
                self.svbscala[1].set('%.4f'%(self.appmaxmin[self.svbscala[0].get()][1]+(self.H-evento.y)*((self.appmaxmin[self.svbscala[0].get()][0]-self.appmaxmin[self.svbscala[0].get()][1])/self.H)))
            except:
                pass
            ###
            #lb=Tix.Label(self.cv,text='ciao')
            if self.stop_balloon:
                self.balloon.place(x=evento.x-self.balloon.winfo_reqwidth()-30,y=evento.y+20)
                self.balloon.update_idletasks()
            #print self.balloon.winfo_reqwidth()

    def creaasc(self):
        self.asc=[]
        self.passo=float(self.W)/float(self.ndativis.get())
        for x in range(0,self.ndativis.get()):
            self.asc.append(self.passo*float(x))
        #sr
        indicezero=self.ultimoindex-self.ndativis.get()+1
        for x in range(0,len(self.sr.supres['id'])):
            asc=[]
            for k in ['data1','data2','data3','data4']:
                #print 'k',self.sr.supres[k][x]
                if self.sr.supres[k][x]<>'':
                    asc.append((self.l[0].index(float(self.sr.supres[k][x]))-indicezero)*self.passo)
            self.sr.supres['asc'].append(asc)
            if self.sr.supres['inizio'][x]<>'':
                ini=(self.l[0].index(float(self.sr.supres['inizio'][x]))-indicezero)
                if ini<=0:
                    self.sr.supres['asc-ini'].append(0.0)
                else:
                    self.sr.supres['asc-ini'].append(ini*self.passo)
            else:
                self.sr.supres['asc-ini'].append(0.0)
            if self.sr.supres['fine'][x]<>'':
                fin=(self.l[0].index(float(self.sr.supres['fine'][x]))-indicezero)
                if ini<=0:
                    self.sr.supres['asc-fin'].append(0)
                else:
                    self.sr.supres['asc-fin'].append(fin*self.passo)
            else:
                self.sr.supres['asc-fin'].append(float(self.W))
                
        #sr


    def depuravol(self,ini):
        app=max(self.l[5][ini:])
        #print 'max=',app
        voldep=[]
        for x in self.l[5]:
            voldep.append(float(x)/float(app))
        return(voldep)

    def crealvcn(self):

        #print 'crealvcn'
        
        #lvcn e' la lista di liste contenenti il vettore da plottare,il colore e il nome.in origine
        #era passato come input ma adesso viene costruito internamente in base ai parametri passati e le info.
        #contenute nel file delle impostazioni e contiene anche il numero della scala da usare nel grafico
        self.lvcn=[]
            
        for x in range(0,len(self.imp.graf['scala'])):

            app=[]
            nome=self.imp.graf['nome'][x]
            colore=self.imp.graf['colore'][x]
            scala=self.imp.graf['scala'][x]

            if self.imp.graf['dati'][x]=='close':
                dati=self.l[4]
            elif self.imp.graf['dati'][x]=='open':
                dati=self.l[1]
            elif self.imp.graf['dati'][x]=='max':
                dati=self.l[2]
            elif self.imp.graf['dati'][x]=='min':
                dati=self.l[3]

            if self.imp.graf['tipo'][x] in ['mm','pcicl','po']:
                #print 'mm'
                if self.imp.graf['opzioni'][x]=='sempl':
                    opz=0
                elif self.imp.graf['opzioni'][x]=='pond':
                    opz=1
                elif self.imp.graf['opzioni'][x]=='exp':
                    opz=2

            if self.imp.graf['tipo'][x]=='quot':
                vett=dati
            elif self.imp.graf['tipo'][x]=='mm':
                vett=stocklib.creamm(dati,g=self.imp.graf['g1'][x],pond=opz)
            elif self.imp.graf['tipo'][x]=='ppw':
                vett=stocklib.creappw(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='ndb':
                vett=stocklib.creandb(self.l[4],self.l[2],self.l[3],g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='ado':
                vett=stocklib.creaado(self.l[4],self.l[2],self.l[3],self.l[1],exp=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='kama':
                vett=stocklib.creakama(dati,n=self.imp.graf['g1'][x],slow=self.imp.graf['g2'][x],
                                       fast=self.imp.graf['g3'][x])
            elif self.imp.graf['tipo'][x]=='vidya':
                vett=stocklib.creavidya(dati,gexp=self.imp.graf['g1'][x],vol_short=self.imp.graf['g2'][x],
                                        vol_long=self.imp.graf['g3'][x])    
            elif self.imp.graf['tipo'][x]=='rsi':
                vett=stocklib.crearsi(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='cv':
                vett=stocklib.creacv(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='meis':
                vett=stocklib.creameisels(dati,gg=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='cci':
                vett=stocklib.creacci(self.l[4],self.l[2],self.l[3],n=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='regular':
                vett=stocklib.crea_regular(self.l[2],self.l[3],self.l[4],self.l[1],n=self.imp.graf['g1'][x])            
            elif self.imp.graf['tipo'][x]=='n_candle':
                vett=stocklib.crean_candle(self.l[2],self.l[3],n=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='b_off':
                vett=stocklib.creab_off(self.l[1],self.l[2],self.l[3],self.l[4],g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='vp':
                vett=stocklib.creavp(self.l[2],self.l[3])
            elif self.imp.graf['tipo'][x]=='vol_ud':
                vett=stocklib.creavol_ud(self.l[4],self.l[5],g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='vol_ud_val':
                vett=stocklib.creavol_ud_val(self.l[4],self.l[5],g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='pfe':
                vett=stocklib.creapfe(dati,g=self.imp.graf['g1'][x],gme=self.imp.graf['g2'][x])
            elif self.imp.graf['tipo'][x]=='roc':
                vett=stocklib.crearoc(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='roc':
                vett=stocklib.crearoc(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='srr':
                vett=stocklib.creasrr(dati,g1=self.imp.graf['g1'][x],g2=self.imp.graf['g2'][x])
            elif self.imp.graf['tipo'][x]=='var':
                vett=stocklib.creavar(self.l,g=self.imp.graf['g1'][x])    
            elif self.imp.graf['tipo'][x]=='pend':
                #print'pend graf'
                vett=stocklib.creapend(dati,g=self.imp.graf['g1'][x])
            elif self.imp.graf['tipo'][x]=='pcicl':
                vett=stocklib.creapcicl(dati,g=self.imp.graf['g1'][x],pond=opz)
            elif self.imp.graf['tipo'][x]=='sar':
                vett=stocklib.creasar(self.l[2],self.l[3])
            elif self.imp.graf['tipo'][x]=='coppock':
                vett=stocklib.creacoppock(self.l[4],self.l[0])[1]
            elif self.imp.graf['tipo'][x]=='obv':
                
                self.ultimoindex=self.l[0].index(float(self.ultdatavis.get()))
                if self.ultimoindex< self.ndativis.get()+1:
                    self.ultimoindex=self.ndativis.get()-1                    
                    
                ini=self.ultimoindex-self.ndativis.get()
                if ini<0:
                    ini=0
                vett=stocklib.creaobv(self.l[4],self.depuravol(ini),inizio=ini)
                
            elif self.imp.graf['tipo'][x]=='intervallo':
                vett=stocklib.creaintervallo(self.l[1],self.l[2],self.l[3],g=self.imp.graf['g1'][x])
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)
                
            elif self.imp.graf['tipo'][x]=='po':
                #print 'creapo'
                vett=stocklib.creapo(dati,g1=self.imp.graf['g1'][x],g2=self.imp.graf['g2'][x],
                                     g3=self.imp.graf['g3'][x],pond=opz)
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)

            elif self.imp.graf['tipo'][x]=='pendo':
                #print 'creapo'
                vett=stocklib.creapendo(dati,g1=self.imp.graf['g1'][x],g2=self.imp.graf['g2'][x],
                                     gmm=self.imp.graf['g3'][x])
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)
                app=[vett[2],self.imp.graf['colore3'][x],self.imp.graf['nome3'][x],scala]
                self.lvcn.append(app)

            elif self.imp.graf['tipo'][x]=='n_candle_c':
                vett=stocklib.crean_candle_c(self.l[2],self.l[3],n=self.imp.graf['g1'][x])
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)
                print 'cc'
                print self.lvcn[-2]
                print self.lvcn[-1]

            elif self.imp.graf['tipo'][x]=='volat':
                vett=stocklib.creavol(self.l[4],self.l[2],self.l[3],g=self.imp.graf['g1'][x],
                                      k=self.imp.graf['g2'][x])
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)

            elif self.imp.graf['tipo'][x]=='r%':
                vett=stocklib.crearw(self.l[4],g=self.imp.graf['g1'][x])
            
            elif self.imp.graf['tipo'][x]=='stoc':
                vett=stocklib.creastoc(dati,g=self.imp.graf['g1'][x],gmm=self.imp.graf['g2'][x])
                #print 'stoc',vett[0]
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)
                
            elif self.imp.graf['tipo'][x]=='bollinger':
                vett=stocklib.creabollinger(dati,g=self.imp.graf['g1'][x])
                #print 'stoc',vett[0]
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app) 

            elif self.imp.graf['tipo'][x]=='dmi':
                vett=stocklib.creadmi(self.l[4],self.l[2],self.l[3],g=self.imp.graf['g1'][x],adx=1)
                app=[vett[0],colore,nome,scala]
                self.lvcn.append(app)
                app=[vett[1],self.imp.graf['colore2'][x],self.imp.graf['nome2'][x],scala]
                self.lvcn.append(app)
                app=[vett[3],self.imp.graf['colore3'][x],self.imp.graf['nome3'][x],scala]
                self.lvcn.append(app)
##                for x in range(1,5):
##                    print vett[0][-x],vett[1][-x],vett[3][-x]
                
            elif self.imp.graf['tipo'][x]=='candle':
                self.lvcn.append([self.l[1],self.imp.graf['colore'][x],'candle-open',scala])
                self.lvcn.append([self.l[2],self.imp.graf['colore2'][x],'candle-max',scala])
                self.lvcn.append([self.l[3],self.imp.graf['colore'][x],'candle-min',scala])
                self.lvcn.append([self.l[4],self.imp.graf['colore2'][x],'candle-close',scala])

            elif self.imp.graf['tipo'][x]=='volume':
                vett=self.l[5]
                nome='volume'
                     
            else:
                print 'else'
                pass
            if self.imp.graf['tipo'][x] not in['stoc','po','dmi','candle','bollinger','volat','intervallo','pendo','n_candle_c']:
                app=[vett,colore,nome,scala]
                self.lvcn.append(app)
            
        #creo balloon
        self.balloon=Tix.Frame(self.cv,bg=self.imp.bg)
        self.balloon.place(x=self.W+10,y=self.H+10)
        
        self.ballb=[]
        self.ballb.append(Tix.StringVar())
        self.ballb[0].set('')
        applb=Tix.Label(self.balloon,text='data: ',)
        applb.grid(row=1,column=0)
        self.stop_balloon=1
        applb.bind('<Button-1>',self.ferma_balloon)
        applb=Tix.Label(self.balloon,textvariable=self.ballb[0])
        applb.grid(row=1,column=1)
        applb.bind('<Button-1>',self.salvapunto)
        for x in range(0,len(self.lvcn)):
            Tix.Label(self.balloon,fg=self.lvcn[x][1],
                      text=self.lvcn[x][2],bg=self.imp.bg).grid(row=x+2,column=0)
            self.ballb.append(Tix.StringVar())
            self.ballb[x+1].set('')
            applb=Tix.Label(self.balloon,fg=self.lvcn[x][1],textvariable=self.ballb[x+1],bg=self.imp.bg)
            applb.grid(row=x+2,column=1)
            applb.bind('<Button-1>',self.salvapunto)
        self.svbscala=[Tix.StringVar(),Tix.StringVar()]
        for x in self.svbscala:
            x.set('1')
        applb=Tix.Entry(self.balloon,textvariable=self.svbscala[0],width=4)
        applb.grid(row=0,column=0)
        applb=Tix.Label(self.balloon,textvariable=self.svbscala[1])
        applb.grid(row=0,column=1)
        applb.bind('<Button-1>',self.salvapunto)
        #fine creazione balloon

    def ferma_balloon(self,ev):
        if self.stop_balloon==1:
            self.stop_balloon=0
            ev.widget.configure(bg='red')
        else:
            self.stop_balloon=1
            ev.widget.configure(bg='white')

    def salvapunto(self,ev):
        self.punto=ev.widget.cget('text')
        #print 'punto',self.punto

    def creaord(self):
        #print 'creaord'
        self.ord=[]
        for x in self.lvcn:
            self.ord.append(0)
        scala=1
        #vedi dopo
        self.appmaxmin={}
        #####
        while scala in self.imp.graf['scala']:
            #print 'scala',scala
            appmax=0
            appmin=9999999999999999999999999999
            #print 'len lvcn',len(self.lvcn)
            for x in self.lvcn:
                #print 'len',len(x[0])
                #print x[0]
                if x[3]==scala:
                    #print '1',x[2],
                    app=max(x[0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1])
                    if app>appmax:
                        appmax=app
                        #print 'max',app,
                    for z in x[0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1]:
                        if z <>None:
                            if z<appmin:
                                appmin=z
            
            
            #livelli - trova max e min                 
            for x in range(0,len(self.imp.livello['identificativo'])):
                if self.imp.livello['scala'][x]==scala:
                    if float(self.imp.livello['quota'][x])>appmax:
                        appmax=float(self.imp.livello['quota'][x])
                    elif float(self.imp.livello['quota'][x])<appmin:
                        appmin=float(self.imp.livello['quota'][x])
            #livelli

            appmax+=((appmax-appmin)*0.05)
            
            #impostati per calcolare il valore del punto selezionato
            self.appmaxmin[str(scala)]=appmax,appmin
            ######
            
            for x in self.lvcn:
                if x[3]==scala:
                    #print 'scala',scala,appmax,appmin
                    #print '2',x[2],
                    ord=[]
                    for y in x[0][self.ultimoindex-self.ndativis.get()+1:self.ultimoindex+1]:
                        if (y<>None):
                            #print x[3],y,appmax,appmin
                            #try:
                            ord.append(((float(y)-float(appmax))*float(self.H))/(float(appmin)-float(appmax)))
                            #except:
                            #    ord.append(self.H)
        
                        else: 
                            ord.append(None)
                    self.ord[self.lvcn.index(x)]=ord
            
            #livelli
            for x in range(0,len(self.imp.livello['identificativo'])):
                if self.imp.livello['scala'][x]==scala:
                    #print 'quota',x,float(self.imp.livello['quota'][x])
                    self.imp.livello['ord'][x]=((float(self.imp.livello['quota'][x])-float(appmax))*float(self.H))/(float(appmin)-float(appmax))
                    #print 'ord1 livello',((float(self.imp.livello['quota'][x])-float(appmax))*float(self.H))/(float(appmin)-float(appmax))
                    #print 'ord livello',self.imp.livello['ord'][x]
            #livelli-fine
            #sr
            for x in range(0,len(self.sr.supres['id'])):
                if self.sr.supres['scala'][x]==scala:
                    ord=[]
                    for y in ['p1','p2','p3','p4']:
                        if self.sr.supres[y][x]<>'':
                            #print 'sr ord',((float(self.sr.supres[y][x])-float(appmax))*float(self.H))
                            ord.append(((float(self.sr.supres[y][x])-float(appmax))*float(self.H))/(float(appmin)-float(appmax)))
                    self.sr.supres['ord'].append(ord)
            #print 'calcola media e m e q'
            for x in range(0,len(self.sr.supres['id'])):
                if self.sr.supres['par'][x]=='':
                    #print 'calcola 1'
                    medy=media(self.sr.supres['ord'][x])
                    medx=media(self.sr.supres['asc'][x])
                    varx=varianza(self.sr.supres['asc'][x])
                    coovxy=coov(self.sr.supres['asc'][x],self.sr.supres['ord'][x])
                    self.sr.supres['ord-ini'].append(medy+(coovxy/varx)*(self.sr.supres['asc-ini'][x]-medx))
                    self.sr.supres['ord-fin'].append(medy+(coovxy/varx)*(self.sr.supres['asc-fin'][x]-medx))
                    self.sr.supres['b'].append(coovxy/varx)
                else:
                    self.sr.supres['ord-ini'].append([])
                    self.sr.supres['ord-fin'].append([])
            for x in range(0,len(self.sr.supres['id'])):
                if self.sr.supres['par'][x]<>'':
                    b=self.sr.supres['b'][int(self.sr.supres['par'][x])]
                    a=self.sr.supres['ord'][x][0]-b*self.sr.supres['asc'][x][0]
                    self.sr.supres['ord-ini'][x]=a+b*self.sr.supres['asc-ini'][x]
                    self.sr.supres['ord-fin'][x]=a+b*self.sr.supres['asc-fin'][x]
                    #calcolare parallela passante per un punto
                             
            #sr-fine
            scala+=1
##        print 'ord:'
##        for x in self.ord:
##            print x[0],x[-1]

    def crealinee(self):
        #print 'crealinee'
        #print 'len',len(self.l[0]),len(self.asc),len(self.ord[0]),len(self.ord[1])
        self.lines=[]
        #print 'len ord',len(self.ord)
        self.swcandle=-1
        swvol=-1
        for x in range(0,len(self.ord)):

            if self.lvcn[x][2] not in ('candle-open','candle-close','candle-max','candle-min','volume'):                
            
                linea=[]
                
                for y in range(0,len(self.ord[x])):
                    if self.ord[x][y]<>None:
                        linea.append(self.asc[y])
                        linea.append(self.ord[x][y])
                #print 'len linea',len(linea),'linea',self.lvcn[x][2]
                self.lines.append(self.cv.create_line(linea,fill=self.lvcn[x][1]))
                #raw_input('premits')
                
            else:
                if (self.swcandle==-1) and (self.lvcn[x][2]<>'volume'):
                    #############
                    self.swcandle=x
                    
                if self.lvcn[x][2]=='volume':
                    swvol==[x]
                    for y in range(0,len(self.ord[x])):
                        linea=[self.asc[y],self.ord[x][y],self.asc[y],self.H]

                        self.lines.append(self.cv.create_line(linea,fill=self.lvcn[x][1]))
                        
                        
        if self.swcandle<>-1:
            
            for y in range(0,len(self.ord[self.swcandle])):
                linea=[]
                linea=[self.asc[y],self.ord[self.swcandle][y]]
                linea.append(self.asc[y])
                linea.append(self.ord[self.swcandle+3][y])
                if abs(linea[3]-linea[1])<1:
                    linea[3]=linea[1]-1
                if self.ord[self.swcandle+3][y]<self.ord[self.swcandle][y]:
                    col=self.lvcn[self.swcandle][1]
                else:
                    col=self.lvcn[self.swcandle+1][1]
                self.lines.append(self.cv.create_line(linea,fill=col,width=5))
                linea=[]
                linea=[self.asc[y],self.ord[self.swcandle+1][y]]
                linea.append(self.asc[y])
                linea.append(self.ord[self.swcandle+2][y])
                self.lines.append(self.cv.create_line(linea,fill=col))
                
                
                    
            
        #livelli
        for x in range(0,len(self.imp.livello['identificativo'])):
            #print 'crealiv',0,self.imp.livello['ord'][x],self.W,self.imp.livello['ord'][x]
            self.lines.append(self.cv.create_line([0,self.imp.livello['ord'][x],
                                                   self.W,self.imp.livello['ord'][x]],
                                                  fill=self.imp.livello['colore'][x]))
            self.cv.create_text(float(self.W/10),self.imp.livello['ord'][x]+5,
                                text=self.imp.livello['nome'][x],
                                fill=self.imp.livello['colore'][x])
        #livelli-fine
        #sr
        for x in range(0,len(self.sr.supres['id'])):
            self.lines.append(self.cv.create_line([self.sr.supres['asc-ini'][x],
                                                   self.sr.supres['ord-ini'][x],
                                                   self.sr.supres['asc-fin'][x],
                                                   self.sr.supres['ord-fin'][x],],
                                                   fill=self.sr.supres['colore'][x]))
        #resetta le asc e ord
        self.puliscisr()
        #sr-fine
            
                              
                                            

    def creagraf(self,*args):
        #print 'creagraf()'
        self.cv.destroy()
        self.cv=Tix.Canvas(self.win,width=self.W,height=self.H,bg=self.imp.bg)
        self.cv.grid(row=0,column=0,columnspan=6)
        self.crealvcn()
        try:
            app=self.endim.get()
            #print 'app',app
            self.imp.W=self.W=int(app[:string.find(app,'x')])
            self.imp.H=self.H=int(app[string.find(app,'x')+1:])
            self.cv.configure(width=self.W,height=self.H)
            #print 1
            if self.ndativis.get()>self.l[0].index(float(self.ultdatavis.get()))+1:
                self.ndativis.set(self.l[0].index(float(self.ultdatavis.get()))+1)
            self.imp.ndatavis=int(self.ndativis.get())
            #print 2
            self.ultimoindex=self.l[0].index(float(self.ultdatavis.get()))
        except:
            print 'data inesistente o dimensioni non corrette'
        else:
            if self.ultimoindex< self.ndativis.get()+1:
                self.ultimoindex=self.ndativis.get()-1

            for x in self.lines:
                self.cv.delete(x)
            self.lines=[]
            self.creaasc()
            self.creaord()
            self.crealinee()
            
        self.segno=self.cv.create_line(0,0,0,self.H)
        self.cv.bind('<Motion>',self.ev)
        self.cv.bind('<Button-1>',self.vischange)

class Ctitgraf:
    """classe che permette la gestione tutti i grafici di un titolo"""

    def cblist(self):
        #print 'cblist'
        if os.path.exists('imp/'+self.pathimage+'/%s.imp'%str(self.num)):
            #print 'apre:',num
            fd=open('imp/'+self.pathimage+'/%s.imp'%str(self.num),'rb')
            self.imp=pickle.load(fd)
            fd.close()
            #print self.imp.keys(),len(self.imp[self.imp.keys()[0]].graf['identificativo'])            
        elif 'std.imp' in os.listdir('imp'):
            #print 'apre std'
            fd=open('imp/std.imp','rb')
            self.imp=pickle.load(fd)
            fd.close()
        self.cb.slistbox.listbox.delete(0,'end')
        app=self.imp.keys()
        if len(app)>1:
            app.sort()
        for x in app:
            self.cb.append_history(x)

    def fdata(self,fl):
        #serve per gli aggiornamenti
        app=str(fl)
        l=string.find(app,'.')
        if l==-1:
            l=len(app)-1
        fd=app[l-2:l]+'/'+app[l-4:l-2]+'/'+app[l-6:l-4]
        return fd

    def datafl(self,dat):
        #serve per gli aggiornamenti
        st=dat[6:]+dat[3:5]+dat[0:2]
        if st[0]=='0':
            st='1'+st
        fl=float(st)
        return fl
    
    def __init__(self,fin,pathdat='/mnt/c/surfer/Borsa/dati/al',
                 num=226,tit="Capitalia",tipofile=0):
        #tipofile: 0=metastock, 1=txtintra, 2=txt, 3=db_sqlite3
        print 'tipofile=',tipofile
        self.num=num
        self.tit=tit
        if tipofile==0:
            self.l=stocklib.aprifile(pathdat+'/F%d.dat'%num)
        elif tipofile==1:
            self.l=stocklib.aprifiletxtintra(pathdat+'/'+num)
        elif tipofile==2:
            self.l=stocklib.aprifiletxt(pathdat+'/'+num,datafmt='mm/gg/aaaa',sep='\t',dec=',',ord=[1,2,3,4,5])
        elif tipofile==3:
            self.l=stocklib.stock_db(pathdat,tit)
            #adatto la data da datetime a msformat
            for x in range(0,len(self.l[0])):
                self.l[0][x]=float('1'+self.l[0][x].strftime('%y%m%d.%H%M'))
            ###
        elif tipofile=='yahoo':
            #self.l=stocklib.apriyahoo(tit)
            ###per apriyahoo3
            self.l=stocklib.apriyahoo3(tit)
            #self.l[0]=map(stocklib.datetimetof,self.l[0])
            #adatto la data da datetime a msformat
            for x in range(0,len(self.l[0])):
                self.l[0][x]=float('1'+self.l[0][x].strftime('%y%m%d.%H%M'))
            ###
            ###
        elif tipofile=='msn':
            app_msn=tit.split(',')
            self.l=stocklib.aprimsn(app_msn[0],app_msn[1])
        print 'prima data: ',self.l[0][0]
        print 'ultima data: ',self.l[0][-1]
        if os.name=='posix':
            #linux
            pathimage=pathdat[string.find(pathdat,'/',1):]
        else:
            #windows
            pathimage=string.replace(pathdat,':','')
            pathimage='-'+string.replace(pathimage,'\\','/')
        pathimage=string.replace(pathimage,'/','-')
        self.pathimage=pathimage
        print "self.pathimage",self.pathimage
        #aggiornamenti#
        try:
            print self.pathimage+'/pref.txt'
            fd=open('imp/'+self.pathimage+'/pref.txt','rb')
        except:
            print 'non agg'
            pass
        else:
            #print 'in aggiornamenti'
            buf=fd.readlines()
            fd.close()
            sw=0
            for x in buf:
                if x[:string.find(x,'-')]==str(self.num):
                    sol=x[string.find(x,'\t')+1:string.find(x,'\n')]
                    sol=string.replace(sol,'\r','')
                    sw=1
                    break
            if sw:
                #print 'titolo nei preferiti'
                agg=os.listdir('./agg')
                agg.sort()
                if len(agg)>50:
                    for x in range(0,5):
                        os.remove('./agg/'+agg[x])
                rif=self.l[0][-1]
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
                            self.l[k].append(l[k])
        #fine aggiornamenti#
        num=str(num)                    
        if os.path.exists('imp/'+pathimage+'/%s.imp'%num):
            #print 'apre:',num
            fd=open('imp/'+pathimage+'/%s.imp'%num,'rb')
            self.imp=pickle.load(fd)
            fd.close()
            #print self.imp.keys(),len(self.imp[self.imp.keys()[0]].graf['identificativo'])
            
        elif 'std.imp' in os.listdir('imp'):
            #print 'apre std'
            fd=open('imp/std.imp','rb')
            self.imp=pickle.load(fd)
            fd.close()
        else:
            #print 'apre crea'
            self.imp={}
            self.imp['quot-mm']=Cimposttit()
            self.imp['quot-mm2']=Cimposttit()
        self.win=Tix.Toplevel(fin)
        self.win.title(tit)
        self.opt= Tix.OptionMenu(self.win)
        self.opt.add_command('V', label='Visualizza')
        self.opt.add_command('N', label='Nuovo')
        self.opt.add_command('E', label='Elimina')
        self.opt.grid(row=0,column=0)
        self.cb = Tix.ComboBox(self.win, label='Grafico', editable=1, history=1,
                               anchor=Tix.E,listcmd=self.cblist)
        self.cblist()
        #print app
        self.cb.pick(0)        
        self.cb.grid(row=1,column=0)        
        #self.cb.slistbox.delete(0,'end')
        #print 'sl\n',dir(self.cb.slistbox.listbox)
        #print dir(self.cb)
        Tix.Button(self.win,text='OK',command=self.comok).grid(row=2,column=0)
        self.ultimoclose=self.l[4][-1]
        Tix.Button(self.win,text='Ripristina Close',command=self.ripclose).grid(row=3,column=0)
        self.svclose=Tix.StringVar()
        self.svclose.set('%.3f'%self.l[4][-1])
        encl=Tix.Entry(self.win,textvariable=self.svclose)
        encl.grid(row=4,column=0)
        Tix.Button(self.win,text='Esporta dati in txt',command=self.B_exp_txt_3).grid(row=5,column=0)
        self.exp_txt=Tix.StringVar()
        self.exp_txt.set('dati.txt')
        encl=Tix.Entry(self.win,textvariable=self.exp_txt)
        encl.grid(row=6,column=0)
        center(self.win)
        self.win.mainloop()

    def B_exp_txt(self):
        fd=open(self.exp_txt.get(),'w')
        for x in range(0,len(self.l[0])):
            for y in range(0,len(self.l)):
                fd.write('%.4f\t'%self.l[y][x])
            fd.write('\n')
        fd.close()

    def B_exp_txt_2(self):#esporta per lettura in qtstalker
        fd=open(self.exp_txt.get(),'w')
        for x in range(0,len(self.l[0])):
            for y in range(0,len(self.l)):
                fd.write('%.4f\t'%self.l[y][x])
            fd.write('\n')
        fd.close()

    def B_exp_txt_3(self):#esporta compatibile con db
        fd=open(self.exp_txt.get(),'w')
        for x in range(0,len(self.l[0])):
            aa,mm,gg=stocklib.ftodate(self.l[0][x])
            fd.write('%s\t'%datetime.datetime(aa,mm,gg))
            for y in range(1,len(self.l)):
                fd.write('%.4f\t'%self.l[y][x])
            fd.write('\n')
        fd.close()

    def impcl(self):
        try:
            app=float(self.svclose.get())
        except:
            self.l[4][-1]=self.ultimoclose
            self.svclose.set('%.3f'%self.ultimoclose)
        else:
            self.l[4][-1]=app
        
    def ripclose(self):
        self.l[4][-1]=self.ultimoclose
        self.svclose.set('%.3f'%self.ultimoclose)

    def comok(self):
        self.impcl()
        if self.opt.menubutton.cget('text') in ['Visualizza','Nuovo']:
            #self.cb.entry.delete(0,Tix.END)
            #if self.opt.menubutton.cget('text') =='Nuovo':
            #    self.cdlist()
            graf=Cgraf(self.l,self.win,file=self.pathimage,
                       titolo=self.tit,graf=self.cb.entry.get(),num=self.num)
        else:
            fd=open('imp/'+self.pathimage+'/%s.imp'%str(self.num),'rb')
            self.imp=pickle.load(fd)
            fd.close()
            if self.cb.entry.get() in self.imp.keys():
                del self.imp[self.cb.entry.get()]
                fd=open('imp/'+self.pathimage+'/%s.imp'%str(self.num),'wb')
                pickle.dump(self.imp,fd)
                fd.close()
                self.cb.entry.delete(0,Tix.END)
            self.opt.menu.invoke(0)
            
            


############
if __name__=='__main__':
    fin=Tix.Tk()
    fin.title('inizio')
    app=Ctitgraf(fin)
    fin.mainloop()
    
