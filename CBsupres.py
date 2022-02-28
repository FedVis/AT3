import Tix
import Pmw
import tkMessageBox
import tkColorChooser
import string

def centrafin(fin,master):
    fin.update_idletasks()
    app=fin.geometry()
    app=app[0:string.find(app,'+')+1]
    app=app+str((fin.winfo_screenwidth()-fin.winfo_width())/2)+'+'+str((fin.winfo_screenheight()-fin.winfo_height())/2)
    fin.geometry(app)
    #fin.transient(master)
    fin.focus()
    #fin.grab_set()
    fin.wait_window(fin)

class CBsupres:
    def csetcb(self,x):
        #print 'set',x
        for y in self.dictcb.keys():
            if y <> 'id':
                #print y,x
                #self.dictcb[y].selectitem(x) self.est.sr[y][x]
                self.dictcb[y]._entryfield.setvalue(str(self.est.sr.supres[y][x]))
    def commop(self,x):
        if x=='M':
            self.dictcb['id'].configure(selectioncommand=self.csetcb)
            if len(self.est.sr.supres['id'])>=1:
                self.dictcb['id'].selectitem(0)
                self.csetcb(0)
                
    def __init__(self,est):
        
        self.est=est
        self.win=Tix.Toplevel(est.win)
        self.win.title('Supporti-Resistenze')
        self.crea()
        centrafin(self.win,est.win)
        self.win.mainloop()
        
    def crea(self):
        self.w=Tix.ScrolledWindow(self.win,width=300,height=150,scrollbar='auto')
        self.w.grid(row=0,column=0,)
        #print dir(self.op)
        self.dictcb={}
        for x in range(0,len(self.est.sr.srkeys)):
            if x <>0:
                if self.est.sr.srkeys[x] in('colore',):
                    scrollist=self.est.opzgraf['colore']
                else:
                    scrollist=self.est.sr.supres[self.est.sr.srkeys[x]]
                cb=Pmw.ComboBox(self.w.window,label_text=self.est.sr.srkeys[x],labelpos='w',
                                scrolledlist_items=scrollist,history=0)
                if self.est.sr.srkeys[x] in ('colore',):
                    cb._entryWidget.bind('<Button-1>',self.colore)
                if self.est.sr.srkeys[x] in ('data1','data2','data3','data4','p1','p2','p3','p4','inizio','fine'):
                    cb._entryWidget.bind('<Button-1>',self.evpunto)
            else:
                cb=Pmw.ComboBox(self.w.window,label_text=self.est.sr.srkeys[x],labelpos='w',
                                scrolledlist_items=self.est.sr.supres[self.est.sr.srkeys[x]],
                                entryfield_entry_state='disabled',entryfield_entry_disabledbackground='white',
                                history=0)
            self.dictcb[self.est.sr.srkeys[x]]=cb
            
            cb.grid(row=x+1,column=0,sticky='we')
        Tix.Button(self.w.window,text='OK',command=self.cbok).grid(row=x+3,column=0)
        self.op=Tix.OptionMenu(self.w.window,command=self.commop,)
        self.op.add_command('M',label='Modifica')
        self.op.add_command('N',label='Nuovo')
        self.op.add_command('E',label='Elimina')
        self.op.grid(row=0,column=0)

    def colore(self,ev):        
        col=tkColorChooser.Chooser(self.w,title='Scegli lo sfondo',
                                   initialcolor='black').show()
        
        ev.widget.configure(bg=col[1])
        ev.widget.delete(0,'end')
        ev.widget.insert(0,col[1])
        #centrafin(self.win)
        #self.win.focus()
        

    def chiudiimp(self):
        self.w.destroy()
        self.crea()

    def evpunto(self,ev):
        ev.widget.delete(0,'end')
        ev.widget.insert(0,self.est.punto)    


    def cbok(self):
        #print self.dictcb['id'].get()
        if (self.op.menubutton.cget('text')=='Modifica') and (len(self.est.sr.supres['id'])==0):
            self.op.menubutton.configure(text='Nuovo')
        if self.op.menubutton.cget('text')<>'Elimina':
            for x in self.est.sr.srkeys:
                if x<> 'id':
                    if x in ['id','scala',]:
                        if self.dictcb[x].get()=='':
                            app=0
                        else:
                            #print self.dictcb[x].get()
                            app=int(self.dictcb[x].get())
                        if (self.op.menubutton.cget('text')=='Modifica'):
                            self.est.sr.supres[x][int(self.dictcb['id'].get())]=app
                        else:
                            self.est.sr.supres[x].append(app)
                    else:
                        if (self.op.menubutton.cget('text')=='Modifica'):
                            self.est.sr.supres[x][int(self.dictcb['id'].get())]=self.dictcb[x].get()
                        else:
                            self.est.sr.supres[x].append(self.dictcb[x].get())
            if self.op.menubutton.cget('text')=='Nuovo':
                if len(self.est.sr.supres['id'])>0:
                    self.est.sr.supres['id'].append(max(self.est.sr.supres['id'])+1)
                else:
                    self.est.sr.supres['id'].append(0)
                #self.est.sr.supres['ord'].append(0)
        else:
            if tkMessageBox.askokcancel('Attenzione','Vuoi eliminare la linea selezionata?'):
                #print 'elimina'
                ind=self.est.sr.supres['id'].index(int(self.dictcb['id'].get()))
                #print 'indice=',ind
                del self.est.sr.supres['id'][ind]
                for x in range(ind,len(self.est.sr.supres['id'])):
                    self.est.sr.supres['id'][x]-=1
                for x in self.est.sr.srkeys:
                    if x<> 'id':
                        del self.est.sr.supres[x][ind]
            else:
                pass
                #print 'non eliminare'
        self.est.creagraf()
        self.w.destroy()
        self.crea()
        self.win.destroy()
