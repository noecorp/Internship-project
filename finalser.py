import xml.etree.ElementTree as et
import datetime
from random import randint
from decimal import Decimal
import pymysql as py
import socket
import sys
import tkinter as tk
from tkinter import *

tree= et.parse('file.xml')
root = tree.getroot()

db = py.connect("172.18.1.62","root","Welcome@123","iso_project" )

cursor = db.cursor()

#global rescode
#reciso= "0200f23a448108e080000000000000020026067667550000210000854422000511151951575434151951051105116012010051100000000000813215575434registerABC000589776581    wxyz68,jubileehills    HyderabadTSIN356007mc000000150010090000000000100010040000"


D={}
E={}
loginfo=[]


def bitmap(pc,mti):
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
            
        
    return L,bmap




"""

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
    print(E)
"""

def extract(bm):
    fields=[]
    for i in range(len(bm)):
       if bm[i]=='1':
           fields.append(str(i+1))
    recpanlen= int(reciso[36:38])
    
    recpan= reciso[38: 38+recpanlen]
    
    D['2']= recpan
    di=38+recpanlen
    
    recpc = reciso[di: 6+di]
    D['3']=recpc
    di+=6
    

    for child in root:
        if child.attrib['pc']==recpc and child.attrib['mti']=='0200':
            for x in child:
                if x.attrib['num'] in fields and x.attrib['num'] not in ['1','2','3']:
                    
                    if x.attrib['type']=='LLVAR':
                    
                        length=reciso[di:di+2]
                        di+=2
                        data=reciso[di:di+ int(length)]
                        di+=int(length)
                        D[x.attrib['num']]=data
                        
         
                    elif x.attrib['type']=='LLLVAR':
                 
                        length=reciso[di:di+3]
                        di+=3
                        data=reciso[di:di+int(length)]
                        di+=int(length)
                        D[x.attrib['num']]=data
                        
                 
                    else:
                      
                        length= x.attrib['length']
                        data=reciso[di:di+int(length)]
                        di+=int(length)
                        D[x.attrib['num']]=data
                                   
    print(D)
    




def insertdb(D,E):
    x=cursor.execute("INSERT into fields(field11) values (%s)", (D['11']))
    db.commit()
    for i in range(128):
        if str(i) in D.keys():
            cursor.execute("Update fields set field"+str(i)+"= %s where field11=%s", (D[str(i)], D['11']))
            db.commit()
        if str(i) in E.keys():
            cursor.execute("Update fields set field"+str(i)+"= %s where field11=%s", (E[str(i)], E['11']))
            db.commit()
        
           
     

def validate(D):
     #global rescode
     if D['3'][-2:] in {'31','01','21','12','90'}:
          sql1="SELECT * from users where pan="+D['2'];
          cursor.execute(sql1)
          res1=cursor.fetchall()
          
          
          
          if len(res1)>0:
               details=res1[0]
               pan=details[0]; name=details[1]; aadhar=details[3]; balance=details[4]
               rescode='00'
               cursor.execute("SELECT pan from users where pan="+D['2'])
               res2=cursor.fetchone()
               if res2[0]<0:
                    rescode='14'
               if D['2'][-10:]!=aadhar:
                    rescode='X8'
               if D['3']=='000021':
                    if len(str(balance+float(D['4'][:-2] + '.' + D['4'][-2:])))>112:
                         rescode='13'
               if D['3']=='000001':
                    if balance<float(D['4'][:-2] + '.' + D['4'][-2:]):
                         rescode='13'
               
               y=D['42']
               sql2="SELECT mer_name,mer_add,mer_city,mer_state,mer_country from merchants where CAIC = %s";
               cursor.execute(sql2,y)
               res3=cursor.fetchall()
               if len(res3[0])>0:
                    merchant="".join(res3[0])
                    if merchant!= str(D['43']).replace(" ",""):
                         rescode='03'
               else:
                    rescode='03'
          
          else:
               rescode='14'
     else:
          rescode='12'
     print(rescode)
     return rescode 




def data_elements(pc,rescode):
    L2,bmap=bitmap(pc=pc,mti='0210')
    dlist2 = ""
    

    for i in L2:
        if i in D.keys():
        
            if i=='2':
                dlist2+=str(len(D['2'])).zfill(2)
                dlist2+=D['2']
            if i=='3':
                dlist2+=pc        
            if i=='4':
                dlist2+=D['4']
                dec = D['4'][:-2] + '.' + D['4'][-2:]
                print(dec)
                E['4']=D['4']
            if i=='5':
                dlist2+=D['5']
            if i=='6':
                dlist2+=D['6']
            if i=='7':
                dlist2+=D['7']
            if i=='8':
                dlist2+=D['8']
            if i=='9':
                dlist2+=D['9']
            if i=='10':
                dlist2+=D['10']       
            if i=='11':
                #assigned by bank switch, system trace audit number
                dlist2+=D['11']
            if i=='12':
                dlist2+=D['12']
            if i=='13':
                dlist2+=D['13']
            if i=='14':
                dlist2+=D['14']
            if i=='15':
                #using curret date
                dlist2+=D['15']
            if i=='16':
                dlist2+=D['16']
            if i=='17':
                dlist2+=D['17']
            if i=='18':
                dlist2+=D['18']
            if i=='19':
                dlist2+=D['19']
            if i=='20':
                dlist2+=D['20']
            if i=='21':
                dlist2+=D['21']
            if i=='22':
                dlist2+=D['22']
            if i=='23':
                dlist2+=D['23']
            if i=='24':
                dlist2+=D['24']
            if i=='25':
                dlist2+=D['25']
            if i=='26':
                dlist2+=D['26']
            if i=='27':
                dlist2+=D['7']
            if i=='28':
                dlist2+=D['28']
            if i=='29':
                dlist2+=D['29']
            if i=='30':
                dlist2+=D['30']
            if i=='31':
                dlist2+=D['31']
            if i=='32':
                dlist2+= str(len(D['32'])).zfill(2)
                dlist2+=D['32']
            if i=='33':
                dlist2+= str(len(D['33'])).zfill(2)
                dlist2+=D['33']
            if i=='34':
                dlist2+= str(len(D['34'])).zfill(2)
                dlist2+=D['34']
            if i=='35':
                dlist2+= str(len(D['35'])).zfill(2)
                dlist2+=D['35']
            if i=='36':
                dlist2+= str(len(D['36'])).zfill(3)
                dlist2+=D['36']
            if i=='37':
                dlist2+=D['37']
            if i=='40':
                dlist2+=D['40']
            if i=='41' :
                dlist2+="register"
            if i=='42':
                #Account no. to be derived from database
                dlist2+=D['42'] #from database         
            if i=='43':
                #address and name to be derived from database
                dlist2+=D['43']
            if i=='44':
                dlist2+=str(len(D['44'])).zfill(2)
                dlist2+=D['44']
            if i=='45':
                dlist2+=str(len(D['45'])).zfill(2)
                dlist2+=D['45']
            if i=='46':
                dlist2+=str(len(D['46'])).zfill(3)
                dlist2+=D['46']
            if i=='47':
                dlist2+=str(len(D['47'])).zfill(3)
                dlist2+=D['47']
            if i=='48':
                dlist2+=str(len(D['48'])).zfill(3)
                dlist2+=D['48']
            if i=='49':
                dlist2+=D['49']
            if i=='50':
                dlist2+=D['50']
            if i=='51':
                dlist2+=D['51']
            if i=='52':
                dlist2+=D['52']
            if i=='53':
                dlist2+=D['53']
            if i=='55':
                dlist2+=str(len(D['55'])).zfill(3)
                dlist2+=D['55']
            if i=='56':
                dlist2+=str(len(D['56'])).zfill(3)
                dlist2+=D['56']
            if i=='57':
                dlist2+=str(len(D['57'])).zfill(3)
                dlist2+=D['57']
            if i=='58':
                dlist2+=str(len(D['58'])).zfill(3)
                dlist2+=D['58']
            if i=='59':
                dlist2+=str(len(D['59'])).zfill(3)
                dlist2+=D['59']
            if i=='60':
                dlist2+=str(len(D['60'])).zfill(3)
                dlist2+=D['60']
            if i=='61':
                dlist2+=str(len(D['61'])).zfill(3)
                dlist2+=D['61']
            if i=='62':
                dlist2+=str(len(D['62'])).zfill(3)
                dlist2+=D['62']
            if i=='63':
                dlist2+=str(len(D['62'])).zfill(3)
                dlist2+=D['63']
            for k in range(64,99):
                if i==str(k):
                    dlist2+=D[str(i)]
            if i=='99':
                dlist2+=str(len(D['99'])).zfill(2)
                dlist2+=D['99']
            if i=='100':
                dlist2+=str(len(D['100'])).zfill(2)
                dlist2+=D['100']
            if i=='101':
                dlist2+=str(len(D['101'])).zfill(2)
                dlist2+=D['101']
            if i=='102':
                dlist2+=str(len(D['102'])).zfill(2)
                dlist2+=D['102']
            if i=='103':
                dlist2+=str(len(D['103'])).zfill(2)
                dlist2+=D['103']    
            for k in range(104,120):
                if i==str(k):
                    dlist2+=str(len(D[str(i)])).zfill(3)
                    dlist2+=D[str(i)]                
            if i=='120':
                if rescode!='00':
                     balance=0
                else:
                     cursor.execute("SELECT balance from users where pan="+D['2'])
                     resx=cursor.fetchone()
                     balance=resx[0]
                     print(balance)
                
                bal = str(format(bal,'.2f')).replace(".","")
                print(bal)
                dlist2+="38100100207002003UID00500210006350" + bal.zfill(350)
            for i in range(121,129):
                if i==str(k):
                    dlist2+=str(len(D[str(i)])).zfill(3)
                    dlist2+=D[str(i)]

        if i not in D.keys():
            if i=='38':
                #assigned by cbs,  Authorization Identification Response 
                dlist2+=str(randint(0,999999)).zfill(6) #if taken from database, extend .zfills(6)
            if i=='39':
                dlist2+=rescode
            if i=='54':
                if rescode!='00':
                     balance=0
                else:
                     cursor.execute("SELECT balance from users where pan="+D['2'])
                     resx=cursor.fetchone()
                     balance=resx[0]
                     print(balance)
                
                if pc=='000001':
                    if rescode=='00':
                        balance=balance-float(dec)
                    if len(str(balance))<=112:
                        l=len(str(balance))+8
                        l=str(l)
                        l=l.zfill(3)
                    dlist2+=l
                    bal=balance
                    balance = str(format(balance,'.2f')).replace(".","")
                    dlist2=dlist2+'0000356D'+balance
                    cursor.execute("update users set balance=%s where pan=%s",(bal,D['2']))
                
                elif pc=='000021':
                    if rescode=='00':
                        balance=balance+float(dec)
                    if len(str(balance))<=112:
                        l=len(str(balance))+8
                        l=str(l)
                        l=l.zfill(3)
                    dlist2+=l
                    bal=balance
                    print(bal)
                    balance = str(format(balance,'.2f')).replace(".","")
                    dlist2=dlist2+'0000356C'+balance
                    cursor.execute("update users set balance=%s where pan=%s",(bal,D['2']))
                    cursor.execute("SELECT balance from users where pan="+D['2'])
                    resx=cursor.fetchone()
                    balancex=resx[0]
                    print(balancex)
                    db.commit()
                    
                else:
                    if len(str(balance))<=112:
                        l=len(str(balance))+8
                        l=str(l)
                        l=l.zfill(3)
                    dlist2+=l
                    bal=balance
                    balance = str(format(balance,'.2f')).replace(".","")
                    dlist2=dlist2+'00003560'+balance
                    #cursor.execute("update users set balance=%s where pan=%s",(bal,D['2']))
                
            
    dlist2=str(hex(int(bmap,2)))[2:]+dlist2
    dlist2='0210'+dlist2
    return dlist2


def connectclient():
    #log.insert(INSERT, "(1) Waiting for connections..\n")
    global reciso
    global reciso2
    global recbm
    global recbm2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 80)
    sock.bind(server_address)
    sock.listen(1)
    loginfo.append("|| "+str(datetime.datetime.now())+" Waiting for connections..")
    while True:
        connection, client_address = sock.accept()
        loginfo.append("|| "+str(datetime.datetime.now())+" Connected with a client..")
        try:
            data = connection.recv(500)
            reciso = str(data)[2:-1]
            print(reciso)
            loginfo.append("|| "+str(datetime.datetime.now())+" Received request ISO..")
            recbm = reciso[4:36]
            recbm = bin(int(recbm,16))
            extract(recbm[2:])
            code=validate(D)
            loginfo.append("|| "+str(datetime.datetime.now())+" Validated the request ISO..")
            data2= data_elements(pc=D['3'],rescode=code)
            loginfo.append("|| "+str(datetime.datetime.now())+" Constructed the response ISO..")
            reciso2=data2
            recbm2=reciso2[4:36]
            recbm2=bin(int(recbm2,16))
            extract2(bm=recbm2[2:],reciso=reciso2)
            data2=data2.encode()
            insertdb(D=D,E=E)
            loginfo.append("|| "+str(datetime.datetime.now())+" Appended all the fields/details of transaction in the database..")
            if data:
                connection.sendall(data2)
                loginfo.append("|| "+str(datetime.datetime.now())+" Sent response ISO to client..")
                connection.close()
                break
            else:
                print('no data from', client_address)
                break
        finally:
            connection.close()
    for i in range(128):
                if str(i) in D.keys() and str(i)!= '1':
                    entries[i-1].configure(state='normal')
                    entries[i-1].delete(0,END)
                    entries[i-1].insert(0,D[str(i)])
                    entries[i-1].configure(state='disabled')
                else:
                    entries[i-1].configure(state='disabled')
    log.delete(1.0, END)
    for i in loginfo:
        log.insert(END,i)
            
cover = Tk()
cover.title("Server Side")
cover.configure(background="#f1dc80")
last= Frame(cover, bg="#f1dc80")
last.place(x=2, y=120)
last.pack(side=BOTTOM)
log= Text(last,height=12, width= 170, wrap=WORD)
log.pack()
frame = Frame(cover, bg= "#c08e36", height="0.5c", width = "15c" )
frame.place(x=380, y=15)
frame.pack_propagate(False)
v=IntVar()
v.set(1)

lb1= Label(frame, text="SERVER, DATA RECEIVED FROM CLIENT", bg= "#c08e36")
lb1.pack()


frame2= Frame(cover, bg="#f1dc80", height="8c", width="40c")
frame2.place(x=5, y=55)
frame2.pack_propagate(False)

entries = []

k=1
for i in range(16):
     for j in range(16):
          lab='DE'+str(int((k+1)/2))
          k=k+1
          if j%2==0:
               lb1= Label(frame2, text=lab, bg="#f1dc80")
               lb1.grid(row=i+1, column=j, pady=2)
          else:
               en = Entry(frame2)
               en.grid(row=i+1, column=j, pady=2)
               entries.append(en)

for entry in entries:
     entry.configure(state='disabled')
     #entry.insert(0,"try2")
     #print(entry.get())

button1= Button(frame2,text="Accept clients and send response ISO", command=connectclient).grid(row=129,column=7, pady=5, columnspan=4)
#button1= Button(frame2,text="send response ISO").grid(row=129,column=9, pady=8, columnspan=2)

cover.mainloop()
