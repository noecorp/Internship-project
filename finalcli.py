import xml.etree.ElementTree as et
import datetime
from random import randint
import socket
import sys
import pymysql as py
import tkinter as tk
from tkinter import *

tree= et.parse('file.xml')
root = tree.getroot()

DE={}
E={}
loginfo=[]

def extract2(bm,reciso):
    fields=[]
    for i in range(len(bm)):
       if bm[i]=='1':
           fields.append(str(i+1))
           

    recpanlen= int(reciso[36:38])
    recpan= reciso[38: 38+recpanlen]
    E['2']= recpan
    di=38+recpanlen
    
    recpc = reciso[di: 6+di]
    E['3']=recpc
    di+=6
    

    for child in root:
        if child.attrib['pc']==recpc and child.attrib['mti']=='0210':
            for x in child:
                if x.attrib['num'] in fields and x.attrib['num'] not in ['1','2','3']:
                    
                    if x.attrib['type']=='LLVAR':
                    
                        length=reciso[di:di+2]
                        di+=2
                        data=reciso[di:di+ int(length)]
                        di+=int(length)
                        E[x.attrib['num']]=data
         
                    elif x.attrib['type']=='LLLVAR':
                 
                        length=reciso[di:di+3]
                        di+=3
                        data=reciso[di:di+int(length)]
                        di+=int(length)
                        E[x.attrib['num']]=data
                        
                 
                    else:
                      
                        length= x.attrib['length']
                        data=reciso[di:di+int(length)]
                        di+=int(length)
                        E[x.attrib['num']]=data
    

def julian(x):
    if x[0]%4==0:
        if x[1]==1:
            day= str(x[2]+000)
            day= day.zfill(3)
        elif x[1]==2:
            day= str(x[2]+31)
            day= day.zfill(3)
        elif x[1]==3:
            day= str(x[2]+59)
            day= day.zfill(3)
        elif x[1]==4:
            day= str(x[2]+90)
            day= day.zfill(3)
        elif x[1]==5:
            day= str(x[2]+120)
            day= day.zfill(3)
        elif x[1]==6:
            day= str(x[2]+151)
            day= day.zfill(3)
        elif x[1]==7:
            day= str(x[2]+181)
            day= day.zfill(3)
        elif x[1]==8:
            day= str(x[2]+212)
            day= day.zfill(3)
        elif x[1]==9:
            day= str(x[2]+243)
            day= day.zfill(3)
        elif x[1]==10:
            day= str(x[2]+273)
            day= day.zfill(3)
        elif x[1]==11:
            day= str(x[2]+304)
            day= day.zfill(3)
        elif x[1]==12:
            day= str(x[2]+334)
            day= day.zfill(3)
    else:
        if x[1]==1:
            day= str(x[2]+000)
            day= day.zfill(3)
        elif x[1]==2:
            day= str(x[2]+31)
            day= day.zfill(3)
        elif x[1]==3:
            day= str(x[2]+60)
            day= day.zfill(3)
        elif x[1]==4:
            day= str(x[2]+91)
            day= day.zfill(3)
        elif x[1]==5:
            day= str(x[2]+121)
            day= day.zfill(3)
        elif x[1]==6:
            day= str(x[2]+152)
            day= day.zfill(3)
        elif x[1]==7:
            day= str(x[2]+182)
            day= day.zfill(3)
        elif x[1]==8:
            day= str(x[2]+213)
            day= day.zfill(3)
        elif x[1]==9:
            day= str(x[2]+244)
            day= day.zfill(3)
        elif x[1]==10:
            day= str(x[2]+274)
            day= day.zfill(3)
        elif x[1]==11:
            day= str(x[2]+305)
            day= day.zfill(3)
        elif x[1]==12:
            day= str(x[2]+335)
            day= day.zfill(3)
    return day

    

def construct(pc,mti):
     D={}
     L=[]
     T=[]
     for child in root:
          if child.attrib['pc']==pc and child.attrib['mti']==mti:
               for x in child:
                    L.append(x.attrib['num'])
     for i in range(128):
          if str(i+1) in L:
               
               D[str(i+1)]= entries[i].get()
     
     iso="0200"
     for child in root:
          if child.attrib['pc']==pc and child.attrib['mti']=='0200':
               for x in child:
                    if x.attrib['num'] in D.keys(): #and x.attrib['num']!='111':
                         if x.attrib['type']=='LLVAR':
                              length= len(D[x.attrib['num']])
                              iso+=str(length).zfill(2)
                              iso+=D[x.attrib['num']]
                         elif x.attrib['type']=='LLLVAR':
                              length= len(D[x.attrib['num']])
                              iso+=str(length).zfill(3)
                              iso+=D[x.attrib['num']]
                         else:
                              length= x.attrib['length']
                              iso+=D[x.attrib['num']].zfill(int(length))
     print(iso)
     loginfo.append("|| "+str(datetime.datetime.now())+" Constructed the request ISO..")
     message=iso
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_address = ('localhost', 80)
     sock.connect(server_address)
     try:
          message = message.encode()
          sock.sendall(message)
          loginfo.append("|| "+str(datetime.datetime.now())+" Sent request ISO to client..")
          amount_received = 0
          amount_expected = len(message)
          data = sock.recv(650)
          amount_received += len(data)
          print(str(data)[2:-1])
          loginfo.append("|| "+str(datetime.datetime.now())+" Received response ISO..")
          reciso=str(data)[2:-1]
          recbm=reciso[4:36]
          recbm=bin(int(recbm,16))
          
          extract2(bm=recbm[2:],reciso=reciso)
     finally:
          print('closing socket')
          sock.close()
          
          for i in range(128):
              if str(i) in E.keys() and str(i)!='1':
                  entries2[i-1].configure(state='normal')
                  entries2[i-1].delete(0,END)
                  entries2[i-1].insert(0, E[str(i)])
                  entries2[i-1].configure(state='disabled')
              else:
                  entries2[i-1].configure(state='disabled')
          loginfo.append("|| "+str(datetime.datetime.now())+" Displayed request ISO..")
          for i in loginfo:
              log.insert(END,i)

          
          
          



def sendiso():
     func = v.get()
     
     if func==1:
          construct(pc='000031', mti='0200')
     elif func==2:
          construct(pc='000021', mti='0200')
     elif func==3:
          construct(pc='000001', mti='0200')
     elif func==4:
          construct(pc='000090', mti='0200')
     else:
          construct(pc='000012', mti='0200')
     



def toload(pc,mti):
     L=[]
     T=[]
     for child in root:
          if child.attrib['pc']==pc and child.attrib['mti']==mti:
               for x in child:
                    L.append(x.attrib['num'])
     bmap=""
     for i in range(1,129):
          if str(i) in L:
               bmap+='1'
          else:
               bmap+='0'
     hbm=str(hex(int(bmap,2)))[2:]
     DE['1']= hbm
     numlist=L
     if '2' in  L:
          pan= '978658969302345467'
          DE['2']=pan
        
     if '3' in L:
          DE['3']=pc
        
     if '4' in L:
          if pc=='000031' or pc=='000090':
               amt='0000000000.00'
               amt = float(amt)
               amt = str(format(amt,'.2f')).replace(".","")
               DE['4']=amt.zfill(12)
           
          if pc=='000021' or pc=='000001':
              amt= '7689808.55'
              amt = float(amt)
              amt = str(format(amt,'.2f')).replace(".","")
              DE['4']=amt.zfill(12)
     if '7' in numlist:
          now = datetime.datetime.now()
          dt = (str(now.month).zfill(2)) + (str(now.day).zfill(2)) + (str(now.hour).zfill(2)) + (str(now.minute).zfill(2)) + (str(now.second).zfill(2))
          DE['7']=dt
     if '11' in numlist:
          x=str(randint(0,999999)).zfill(6)
          DE['11']=x
     if '12' in numlist:
          now = datetime.datetime.now()
          dt = (str(now.hour).zfill(2)) + (str(now.minute).zfill(2)) + (str(now.second).zfill(2))
          DE['12']=dt
     if '13' in numlist:
          now = datetime.datetime.now()
          dt = (str(now.month).zfill(2)) + (str(now.day).zfill(2))
          DE['13']=dt
     if '15' in numlist:
          now = datetime.datetime.now()
          dt = (str(now.month).zfill(2)) + (str(now.day).zfill(2))
          DE['15']=dt
     if '18' in numlist:
          DE['18']="6012"
     if '22' in numlist:
        #we are taking manual PAN input and pin entry mode is unspecified- app based
          DE['22']="010"
     if '25' in numlist:
          DE['25']="05"
     if '32' in numlist:
        #assigned by NPCI, Acquiring Institution Identification Code
          DE['32']="00000000000" #if taken from database, extend .zfills(11)
     if '37' in numlist:
        #assigned by bank switch, system trace audit number
          now = datetime.datetime.now()
          list1=[now.year, now.month, now.day]
          day=julian(list1)
          year = str(now.year)
          year= year[3]
          dt= year+day+ (str(now.hour).zfill(2)) + x
          DE['37']=dt
     if '38' in numlist:
        #assigned by cbs,  Authorization Identification Response 
          DE['38']=str(randint(0,999999)).zfill(6) #if taken from database, extend .zfills(6)
     if '41' in numlist:
          DE['41']="register"
     if '42' in numlist:
        #to be derived from database
          DE['42']="ABC000589776581" #from database 
        
     if '43' in numlist:
        #address and name to be derived from database
          mername = 'merchant1' #from database
          meradd= 'jubileehills' #from database
          first = mername + meradd
          first = first.rjust(23)
          city= 'Hyderabad' #from database
          city = city.rjust(13)
          state = 'TS' # from database
          country = 'IN' #from database
          final = first + city + state + country
          DE['43']=final
     if '49' in numlist:
          DE['49']="356"
     if '111' in numlist:
          DE['111']="jyyfytfuyehidei3eo455dgdegdh3uei887"
     if '120' in numlist:
          DE['120']="01700100207002003UID" #sample data
     if '123' in numlist:
          DE['123']="mc00000" #sample data
     if '126' in numlist:
          DE['126']="001009000000000" #sample data
     if '127' in numlist:
          DE['127']="0010040000" #sample data
     
     for i in range(128):
          if str(i) in L:
               entries[i-1].delete(0,END)
               entries[i-1].insert(0, DE[str(i)])




def display(pc,mti):
    L=[]
    T=[]
    for child in root:
        if child.attrib['pc']==pc and child.attrib['mti']==mti:
            for x in child:
                L.append(x.attrib['num'])
    
    for i in range(128):
         if str(i+1) in L:
              entries[i].configure(state='normal')
         else:
              entries[i].configure(state='disabled') 
    


def loaddata():
     func = v.get()
     if func==1:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Loaded data for Balance enquiry request")
          toload(pc='000031', mti='0200')
     elif func==2:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Loaded data for Cash deposit request")
          toload(pc='000021', mti='0200')
     elif func==3:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Loaded data for Cash withdrawal request")
          toload(pc='000001', mti='0200')
     elif func==4:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Loaded data for Mini statement request")
          toload(pc='000090', mti='0200')
     else:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Loaded data for user authentication request")
          toload(pc='000012', mti='0200')
     




def show():
     func = v.get()
     if func==1:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Enabled entries for Balance enquiry request")
          display(pc='000031', mti='0200')
     elif func==2:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Enabled entries for Cash deposit request")
          display(pc='000021', mti='0200')
     elif func==3:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Enabled entries for Cash withdrawal request")
          display(pc='000001', mti='0200')
     elif func==4:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Enabled entries for Mini statement request")
          display(pc='000090', mti='0200')
     else:
          log.insert(INSERT, "|| "+str(datetime.datetime.now())+" Enabled entries for user authentication request")
          display(pc='000012', mti='0200')



cover = Tk()
cover.title("Client Side")
cover.configure(background="#c4c9f9")
last= Frame(cover, bg="#c4c9f9")
last.place(x=2, y=120)
last.pack(side=BOTTOM)
log= Text(last,height=12, width= 170, wrap=WORD)
log.pack()
frame = Frame(cover, bg= "#859994", height="1c", width = "15c" )
frame.place(x=350, y=5)
frame.pack_propagate(False)
v=IntVar()
v.set(1)

rb1= Radiobutton(frame, command= show, text="Balance Enquiry", variable=v, value=1,bg= "#859994", padx='0.3c')
rb1.pack(side=LEFT)
rb2 = Radiobutton(frame, command= show, text="Deposit", variable=v, value=2,bg= "#859994", padx='0.2c')
rb2.pack(side=LEFT)
rb3 = Radiobutton(frame, command= show, text="Withdraw", variable=v, value=3, bg= "#859994", padx='0.2c')
rb3.pack(side=LEFT)
rb4 = Radiobutton(frame, command= show, text="Mini Statement", variable=v, value=4, bg= "#859994", padx='0.2c')
rb4.pack(side=LEFT)
rb5 = Radiobutton(frame, command= show, text="Authenticate User", variable=v, value=5, bg= "#859994", padx='0.2c')
rb5.pack(side=LEFT)

frame2= Frame(cover, bg="#ccd7a8", height=500, width=600)
frame2.place(x=5, y=60)
frame2.pack
head1=Label(frame2, text="REQUEST",bg="#ccd7a8")
head1.pack(side=TOP)
canvas=Canvas(frame2,bg="#ccd7a8",width=600,height=400,scrollregion=(0,0,1300,500))
hbar=Scrollbar(frame2,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame2,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=600,height=400)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)
sframe=Frame(canvas,bg="#ccd7a8")
canvas.create_window((0,0), window=sframe, anchor='nw')

entries = []

k=1
for i in range(16):
     for j in range(16):
          lab='DE'+str(int((k+1)/2))
          k=k+1
          if j%2==0:
               lb1= Label(sframe, text=lab, bg="#ccd7a8")
               lb1.grid(row=i+1, column=j, pady=1)
          else:
               en = Entry(sframe)
               en.grid(row=i+1, column=j, pady=1)
               entries.append(en)


for entry in entries:
     entry.configure(state='disabled')
     #entry.insert(0,"try2")
     #print(entry.get())



button1= Button(sframe,text="Load data", command=loaddata).grid(row=129,column=2, pady=5)
button1= Button(sframe,text="send ISO", command=sendiso).grid(row=129,column=4, pady=5)

frame3= Frame(cover, bg="#b9e7a8", height=400, width=600)
frame3.place(x=700, y=60)
frame3.pack
head2=Label(frame3, text="RESPONSE",bg="#b9e7a8")
head2.pack(side=TOP)
canvas2=Canvas(frame3,bg='#b9e7a8',width=600,height=400,scrollregion=(0,0,1300,500))
hbar=Scrollbar(frame3,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas2.xview)
vbar=Scrollbar(frame3,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas2.yview)
canvas2.config(width=600,height=400)
canvas2.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas2.pack(side=LEFT,expand=True,fill=BOTH)
sframe2=Frame(canvas2, bg="#b9e7a8")
canvas2.create_window((0,0), window=sframe2, anchor='nw')

entries2 = []

h=1
for i in range(16):
     for j in range(16):
          lab='DE'+str(int((h+1)/2))
          h=h+1
          if j%2==0:
               lb1= Label(sframe2, text=lab, bg="#b9e7a8")
               lb1.grid(row=i+1, column=j, pady=1)
          else:
               en = Entry(sframe2)
               en.grid(row=i+1, column=j, pady=1)
               entries2.append(en)

for entry in entries2:
    entry.configure(state='disabled') 


cover.mainloop()
