#!/usr/local/bin/python

import Tkinter as Tk
import Pmw
import os
import pickle
import copy
import string
from m2ipy import m2i
from struct import *

class correl:
    
    def center(self,wid):
        self.fin.update_idletasks()
        app=wid.geometry()
        app=app[0:string.find(app,'+')+1]
        app=app+str((wid.winfo_screenwidth()-wid.winfo_width())/2)+'+'+str((wid.winfo_screenheight()-wid.winfo_height())/2)
        wid.geometry(app)
        
    def __init__(self,root):
        fd=open('preferiti.txt','r')
        self.pref=fd.readlines()
        fd.close()
        for x in range(0,len(self.pref)):
            self.pref[x]=string.replace(self.pref[x],'\n','')
            self.pref[x]=string.replace(self.pref[x],'\r','')
        self.fin=Tk.Toplevel(root)
        self.fin.title=('Correlazione')
        Tk.Label(self.fin,text='Archivio').grid(row=0,column=0)
        Tk.Label(self.fin,text='Preferiti').grid(row=0,column=1)
        self.sv1=Tk.StringVar()
        Pmw.ComboBox(self.fin,scrolledlist_items=self.pref,
                     entryfield_entry_textvariable=self.sv1,
                     entryfield_entry_state='disabled',
                     selectioncommand=lambda e: self.creacb(1)).grid(row=1,column=0)
        self.sv2=Tk.StringVar()
        Pmw.ComboBox(self.fin,scrolledlist_items=self.pref,
                     entryfield_entry_textvariable=self.sv2,
                     entryfield_entry_state='disabled',
                     selectioncommand=lambda e: self.creacb(2)).grid(row=2,column=0)
        self.sv3=Tk.StringVar()
        self.cb1=Pmw.ComboBox(self.fin,scrolledlist_items=[],
                              entryfield_entry_textvariable=self.sv3,
                              entryfield_entry_state='disabled')
        self.cb1.grid(row=1,column=1)
        self.sv4=Tk.StringVar()
        self.cb2=Pmw.ComboBox(self.fin,scrolledlist_items=[],
                              entryfield_entry_textvariable=self.sv4,
                              entryfield_entry_state='disabled')
        self.cb2.grid(row=2,column=1)
        Tk.Label(self.fin,text='Da').grid(row=3,column=0)
        Tk.Label(self.fin,text='A').grid(row=3,column=1)
        self.sv5=Tk.StringVar()
        self.cb3=Pmw.ComboBox(self.fin,scrolledlist_items=[],
                              entryfield_entry_textvariable=self.sv5,
                              entryfield_entry_state='disabled')
        self.cb3.grid(row=4,column=0)
        self.sv6=Tk.StringVar()
        self.cb4=Pmw.ComboBox(self.fin,scrolledlist_items=[],
                              entryfield_entry_textvariable=self.sv6,
                              entryfield_entry_state='disabled')
        self.cb4.grid(row=4,column=1)
        Tk.Label(self.fin,text='Scarto').grid(row=5,column=0)
        self.sv7=Tk.IntVar()
        self.sv7.set(0)
        Pmw.Counter(self.fin,entry_textvariable=self.sv7,datatype='integer',entryfield_validate = {'validator' : 'integer','min': 0}).grid(row=5,column=1)
        
        Tk.Button(self.fin,text='Calcola',underline=0,command=self.calcola).grid(row=6,column=0,columnspan=2)
        Tk.Label(self.fin,text='Correlazione:').grid(row=7,column=0,columnspan=2)
        self.sv8=Tk.StringVar()
        self.sv8.set('da calcolare')
        Tk.Label(self.fin,textvariable=self.sv8).grid(row=8,column=0,columnspan=2)
        self.center(self.fin)
        self.fin.transient(root)
        self.fin.focus()
        self.fin.grab_set()
        self.fin.wait_window(self.fin)
        
    def fdata(self,fl):
        app=str(fl)
        l=string.find(app,'.')
        if l==-1:
            l=len(app)-1
        fd=app[l-2:l]+'/'+app[l-4:l-2]+'/'+app[l-6:l-4]
        return fd                

    def creacb(self,n):
        if n==1:
            self.svcart=self.sv1
            self.cb1.destroy()
            fd=open(self.sv1.get()+'/pref.txt','r')
            app=fd.readlines()
            fd.close()
            for x in range(0,len(app)):
                app[x]=string.replace(app[x],'\n','')
                app[x]=string.replace(app[x],'\r','')
            self.cb1=Pmw.ComboBox(self.fin,scrolledlist_items=app,
                                  entryfield_entry_textvariable=self.sv3,
                                  entryfield_entry_state='disabled',
                                  selectioncommand=lambda e: self.creanum(n))
            self.cb1.grid(row=1,column=1)
        else:
            self.svcart=self.sv2
            self.cb2.destroy()
            fd=open(self.sv2.get()+'/pref.txt','r')
            app=fd.readlines()
            fd.close()
            for x in range(0,len(app)):
                app[x]=string.replace(app[x],'\n','')
                app[x]=string.replace(app[x],'\r','')
            self.cb2=Pmw.ComboBox(self.fin,scrolledlist_items=app,
                                  entryfield_entry_textvariable=self.sv4,
                                  entryfield_entry_state='disabled',
                                  selectioncommand=lambda e: self.creanum(n))
            self.cb2.grid(row=2,column=1)
        

    def creanum(self,n):
        if n==1:
            self.num=self.sv3.get()[:string.find(self.sv3.get(),'-')]
            self.svcart=self.sv1
            self.l1=self.crealist()
            print 'num1',self.num
        else:
            self.num=self.sv4.get()[:string.find(self.sv4.get(),'-')]
            self.svcart=self.sv2
            self.l2=self.crealist()
            print 'num2',self.num
            #print 'l2',self.l2[len(self.l2)-10:]
        if (self.sv4.get()<>'') and (self.sv3.get()<>''):
            print self.l1[0][0], self.datafl(self.l1[0][0])
            print self.l2[0][0], self.datafl(self.l2[0][0])
            if self.datafl(self.l1[0][0])>=self.datafl(self.l2[0][0]):
                ini=self.datafl(self.l1[0][0])
            else:
                ini=self.datafl(self.l2[0][0])
            if self.datafl(self.l1[len(self.l1)-1][0])<=self.datafl(self.l2[len(self.l2)-1][0]):
                fin=self.datafl(self.l1[len(self.l1)-1][0])
            else:
                fin=self.datafl(self.l2[len(self.l2)-1][0])
            self.date=[]
            ######
            for x in range(0,len(self.l1)):
                if (self.datafl(self.l1[x][0])>fin):
                    break
                if (self.datafl(self.l1[x][0])>=ini)and(self.datafl(self.l1[x][0])<=fin):
                    self.date.append(self.l1[x][0])
            ########

            self.cb3.destroy()
            self.cb3=Pmw.ComboBox(self.fin,scrolledlist_items=self.date,
                                  entryfield_entry_textvariable=self.sv5,
                                  entryfield_entry_state='disabled')
            self.cb3.grid(row=4,column=0)
            self.cb4.destroy()
            self.cb4=Pmw.ComboBox(self.fin,scrolledlist_items=self.date,
                                  entryfield_entry_textvariable=self.sv6,
                                  entryfield_entry_state='disabled')
            self.cb4.grid(row=4,column=1)
            self.sv5.set(self.date[0])
            self.sv6.set(self.date[len(self.date)-1])

            
    def calcola(self):
        if (self.sv5.get()=='')or(self.sv6.get()==''):
            return(0)
        vettdate=[]
        vettx=[]
        vetty=[]
        list2=[]
        for x in self.l2:
            list2.append(x[0])
        c=0
        for x in range(0,len(self.l1)):
            if self.datafl(self.l1[x][0])>=self.datafl(self.sv5.get()):
                ini=x
                break
        while (ini<len(self.l1)) and (self.datafl(self.l1[ini][0])<=self.datafl(self.sv6.get())):
            if c==self.sv7.get():
                if self.l1[ini-c][0] in list2:
                    vettdate.append(self.l1[ini][0])
                    vettx.append(self.l1[ini][4])
                    vetty.append(self.l2[list2.index(self.l1[ini-c][0])][4])        
            else:
                c+=1
            ini+=1
        print 'vettdate',vettdate[len(vettx)-1]
        print 'vettx',vettx[len(vettx)-1]
        print 'vetty',vetty[len(vettx)-1]
        medx=0.0
        medy=0.0
        for x in range(0,len(vettx)):
            medx+=vettx[x]
            medy+=vetty[x]
        medx=medx/float(len(vettx))
        medy=medy/float(len(vetty))
        print 'medx',medx
        print 'medy',medy
        varx=0
        vary=0
        cov=0
        for x in range(0,len(vettx)):
            varx=varx+(vettx[x]-medx)*(vettx[x]-medx)
            vary=vary+(vetty[x]-medy)*(vetty[x]-medy)
            cov=cov+(vetty[x]-medy)*(vettx[x]-medx)

        varx=varx/float(len(vettx))
        vary=vary/float(len(vetty))        
        cov=cov/float(len(vettx))
        print 'varx',varx,'vary',vary,'cov',cov
        corr=cov/(pow(varx,0.5)*pow(vary,0.5))
        print 'corr',corr
        print 'contati',len(vettx)
        self.sv8.set(str(corr))

    def datafl(self,dat):
        #print 'dat',dat
        if int(dat[6:])<6:
            st='2'+dat[6:]+dat[3:5]+dat[0:2]
        else:
            st='1'+dat[6:]+dat[3:5]+dat[0:2]
        fl=float(st)
        return fl


    def crealist(self):
        print 'crealist'
        
        def datafl(dat):
            st=dat[6:]+dat[3:5]+dat[0:2]
            fl=float(st)
            return fl
            
        fd=open(self.svcart.get()+'/F'+self.num+'.DAT','rb')
        buf=fd.read()
        fd.close()
        v=unpack('HH',buf[0:4])
        #print ' max rec: %d , last rec: %d'%(v[0],v[1])
        i=28
        list=[]
        while i<len(buf):
            v=unpack('fffffff',buf[i:i+28])
            l=[]
            l.append(self.fdata(m2i(v[0])))
            for x in range(1,6):
                l.append(m2i(v[x]))                
            list.append(l)
            i+=28
        #aggiornamenti
        try:
            fd=open(self.svcart.get()+'/pref.txt','rb')
        except:
            pass
        else:
            #print 'in aggiornamenti'
            buf=fd.readlines()
            fd.close()
            sw=0
            for x in buf:
                if x[:string.find(x,'-')]==self.num:
                    sol=x[string.find(x,'\t')+1:string.find(x,'\n')-1]
                    sw=1
                    break
            if sw:
                #print 'titolo nei preferiti'
                agg=os.listdir('./agg')
                agg.sort()
                if len(agg)>15:
                    for x in range(0,5):
                        os.remove('./agg/'+agg[x])
                rif=l[0]
                agg=os.listdir('./agg')
                agg.sort()
                for x in agg:
                    #print 'rif=',rif
                    if datafl(self.fdata(float(x)))<=datafl(rif):
                        continue
                    fd=open('./agg/'+x,'rb')
                    matr=pickle.load(fd)
                    fd.close()
                    sw1=0
                    for y in matr:
                        #print '-%s-,-%s-'%(y[0],sol)
                        if y[0]==sol:
                            #print'uguali!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                            l=copy.deepcopy(y)
                            l[0]=self.fdata(float(x))
                            sw1=1
                            break
                    if sw1:
                        list.append(l)
        return(list)
        



if __name__ == '__main__':
    root=Tk.Tk()
    root.title('Root')
    correl(root)
    root.mainloop()
