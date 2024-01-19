 
from typing import List
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
import paramiko
import  ipaddress 
import random  
 
 
 
from ipaddress import IPv4Address
from time import sleep
from django.template import Context, loader
from django.http import HttpResponse
import time
import getpass
import logging
from datetime import datetime
from colorama import Fore
from .filters import RouteurFilter 
from .filters import ScriptFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate  , logout
from django.contrib.auth import login as mylogin
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from paramiko import SSHClient, AutoAddPolicy
import os
from openpyxl import Workbook
from openpyxl import load_workbook
from napalm import get_network_driver
import json
from flask_table import Table, Col
from django.contrib import messages

from time import sleep
import sys, os, string, threading
import paramiko 

def convert_bytes(size_in_bytes):
     return size_in_bytes/(1024*1024*1024)
 


cmdbh = "dis   int GigabitEthernet"
cmdno=" | no-more"
cmdtrunk="dis int "
cmd = "dis int brief Eth-Trunk | i up | exclude Eth-Trunk5 | no-more"
cmdbhsharingout="dis   int "
 

def update_something():
    print("I am a scheduled job")
    DEVICE_LIST =['10.51.2.' + str(n) for n in range(5,217)]
    for RTR in DEVICE_LIST:
        print ('\n #### Connecting to the device ' + RTR + '####\n' )
        if RTR=="10.51.2.205" or RTR=="10.51.2.103" or RTR=="10.51.2.60" or RTR=="10.51.2.57" or RTR=="10.51.2.58" or RTR=="10.51.2.66" or RTR=="10.51.2.68" or RTR=="10.51.2.71" or RTR=="10.51.2.33":
            DEVICE_LIST.index(RTR)+1
        else:

            try:
                
                
                
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username= 'ing_onap', password='Ingenierie@!23')
                stdin, stdout, stderr = session.exec_command("dis int brief Eth-Trunk | exclude Eth-Trunk5 | no-more | i up")
                output= []
                output = stdout.readlines()
                
                 
                list=[]
                
                
                sub_l = [i for i in output if i.startswith('Eth')]
                for i in sub_l:
                                    
                    
                    x=int(i.rfind("up"))
                    o=int(i.rfind("down"))
                    y=int(i.find("%"))
                     
                    if x!=-1:
                        z=i[x+2:y].strip()
                    if  o!=-1  : 
                        z=i[o+4:y].strip()

                    list.append(float(z))

                print(max(list))

                session.close()
                trafic=Trafic(routeur=RTR,percent=(max(list)),date=datetime.now())
                trafic.save()
            

                    
            except :
                
                DEVICE_LIST.index(RTR)+1
 

def del_something():
    trafic=Trafic.objects.all()
     
    trafic.all().delete()



def dim():
    dim=(Dimens.objects.all().values_list())
    list_result = [entry for entry in dim]
    for i in (list_result):
     try:    
        print(i[1])
        if i[1].count("-")==1  : 
            
             
                
                typeinterface100G=int((i[6]).find("100G"))
                typeinterfaceae=int((i[6]).find("ae"))
                typeinterfaceeth=int((i[6]).find("eth"))
                typeinterfaceEth=int((i[6]).find("Eth"))
                cmdshow="show interfaces "
                cmddis="dis int "
                cmdnomore=" | no-more "
                cmdB2B=cmdshow+i[6]+cmdnomore
                cmdBB=cmddis+i[6]+cmdnomore
                if typeinterface100G!=-1:
                    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdBB)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                        
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()
                    
                     
                    x1=int("".join(output).find("utility rate:"))
                    
                    y1=int("".join(output).find("%"))
                    z1="".join(output)[x1+13:y1].strip()
                            
                    session.close()  
                     
                  
                    if(float(z)>float(z1)):
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z),2)>=dimens.percent):
                            dimens.percent= round(float(z),2) 
                            print(dimens.percent)
                            dimens.save()
                    else:
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z1),2)>=dimens.percent):
                            dimens.percent= round(float(z1),2) 
                            print(dimens.percent)
                            dimens.save()
                        
                    time.sleep(3)
                
               
               
                 
      
                
               
                 
                if typeinterfaceae!=-1 :
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdB2B)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).find("Input rate     :"))
                    
                    y=int("".join(output).find("Logical"))
                    
                            
                    findG=int("".join(i[4]).find("G")) 
                    gcapp=float(i[4][:findG].strip())        
                    session.close()
                    TN1TN2="".join(output)[x:y].strip()
                                    
                    x1=int(TN1TN2.find(":"))
                    y1=int(TN1TN2.find("bps"))
                                        
                    x2=int(TN1TN2.rfind(":"))
                    y2=int(TN1TN2.rfind("bps"))
                    
                    gw1=float(TN1TN2[x1+1:y1].strip())  
                    gcap=convert_bytes(gw1)
               
                    gcapgcap1=float(gcap )

                    gw2=float(TN1TN2[x2+1:y2].strip())
                    gcap2=convert_bytes(gw2)
                   
                    gcapgcap2=float(gcap2 )


                    print(gcapgcap1)
                    print(gcapgcap2)
                    gw1Giga=round(gcapgcap1*100/gcapp,2)
                    gw2Giga=round(gcapgcap2*100/gcapp,2)
                    print(gw1Giga)
                    print(gw2Giga)
                    dimens=Dimens.objects.get(liaison=i[1])
                    print(dimens.percent)
                    if (gw1Giga>gw2Giga):
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(gw1Giga>=dimens.percent):
                            dimens.percent= gw1Giga
                            print(dimens.percent)
                            dimens.save()
                    else:
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(gw2Giga>=dimens.percent):
                            dimens.percent= gw2Giga 
                            print(dimens.percent)
                            dimens.save()
                    
                    time.sleep(3)
             
             
                
                 
          
                if typeinterfaceeth!=-1 or typeinterfaceEth!=-1:
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdBB)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                        
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()
                    
                     
                    x1=int("".join(output).find("utility rate:"))
                    
                    y1=int("".join(output).find("%"))
                    z1="".join(output)[x1+13:y1].strip()
                            
                    session.close()  
                     
                  
                    if(float(z)>float(z1)):
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z),2)>=dimens.percent):
                            dimens.percent= round(float(z),2) 
                            print(dimens.percent)
                            dimens.save()
                    else:
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z1),2)>=dimens.percent):
                            dimens.percent= round(float(z1),2) 
                            print(dimens.percent)
                            dimens.save()
                        
                    time.sleep(3)
                if typeinterfaceeth==-1 and typeinterfaceEth==-1 and typeinterfaceae==-1 and typeinterface100G==-1: 
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdB2B)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).find("Input rate     :"))
                    
                    y=int("".join(output).find("Active"))
                    
                            
                    findG=int("".join(i[4]).find("G")) 
                    gcapp=float(i[4][:findG].strip())        
                    time.sleep(20)
                    session.close()
                    TN1TN2="".join(output)[x:y].strip()
                                    
                    x1=int(TN1TN2.find(":"))
                    y1=int(TN1TN2.find("bps"))
                                        
                    x2=int(TN1TN2.rfind(":"))
                    y2=int(TN1TN2.rfind("bps"))
                    
                    gw1=float(TN1TN2[x1+1:y1].strip())  
                    gcap=convert_bytes(gw1)
                     
                    gcapgcap1=float(gcap )

                    gw2=float(TN1TN2[x2+1:y2].strip())
                    gcap2=convert_bytes(gw2)
                     
                    gcapgcap2=float(gcap2 )


                    print(gcapgcap1)
                    print(gcapgcap2)
                    gw1Giga=round(gcapgcap1*100/gcapp,2)
                    gw2Giga=round(gcapgcap2*100/gcapp,2)
                    print(gw1Giga)
                    print(gw2Giga)
                    if (gw1Giga>gw2Giga):
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(gw1Giga>=dimens.percent):
                            dimens.percent= gw1Giga
                            print(dimens.percent)
                            dimens.save()
                    else:
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(gw2Giga>=dimens.percent):
                            dimens.percent= gw2Giga 
                            print(dimens.percent)
                            dimens.save()  
                    
                     
        if i[1].count("-")==2:
            if (i[1]=="TUN_0091-ARI_0050-ARI_0097"):
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect('10.51.2.3', port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command("dis int eth7 | no-more")
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                        
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()
                    
                     
                    x1=int("".join(output).find("utility rate:"))
                    
                    y1=int("".join(output).find("%"))
                    z1="".join(output)[x1+13:y1].strip()
                            
                    session.close()  
                     
                  
                    if(float(z)>float(z1)):
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z),2)>=dimens.percent):
                            dimens.percent= round(float(z),2) 
                            print(dimens.percent)
                            dimens.save()
                    else:
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(round(float(z1),2)>=dimens.percent):
                            dimens.percent= round(float(z1),2) 
                            print(dimens.percent)
                            dimens.save()
                        
                    time.sleep(3)
            else:
                
                 
                    cherchinter=int(i[6].find("/"))
                    loop1inter=i[6][:cherchinter]
                    loop2inter= i[6][cherchinter+1:]
                    cmddis="dis int "
                    cmdnomore=" | no-more "
                        
                    cmdBB1=cmddis+loop1inter+cmdnomore
                    cmdBB2=cmddis+loop2inter+cmdnomore 
                    
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(i[2], username='ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = ssh.exec_command(cmdBB1)
                   
                    output = stdout.readlines()
                    x=int("".join(output).find("utility rate:"))
                        
                    y=int("".join(output).find("%"))
                                
                        
                        
                    z="".join(output)[x+13:y].strip() 
                    
                    
                     
                    ssh.close()
                    

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(i[2], username='ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = ssh.exec_command(cmdBB2)
                    output=stdout.readlines()
                    x1=int("".join(output).find("utility rate:"))
                        
                    y1=int("".join(output).find("%"))
                                
                        
                        
                    z1="".join(output)[x1+13:y1].strip()
                        
                    som=round((float(z)+float(z1)),2)
                    dimens=Dimens.objects.get(liaison=i[1])
                    print(dimens.percent)
                    if(som>=dimens.percent):
                            dimens.percent= som 
                            print(dimens.percent)
                            dimens.save() 
                         
                     
                     
                    ssh.close()   
                    
        if i[1].count("-")>2:
                if (i[1]=="SOU_0046-SOU_0069-SOU_0059-MON_0011-MON_0017-SOU_0065-SOU_0091") or (i[1]=="TUN_0005-NAB_0080-NAB_0009-NAB_0002-NAB_0037-NAB-NAB_0038-NAB_0052-TUN_0091"):
                     if (i[1]=="SOU_0046-SOU_0069-SOU_0059-MON_0011-MON_0017-SOU_0065-SOU_0091"):
                        session = paramiko.SSHClient()
                        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        session.connect('10.51.2.5', port=22, username= 'ing_onap', password='Ingenierie@!23')
                        stdin, stdout, stderr = session.exec_command("dis int eth3 | no-more")
                        output= []
                        output = stdout.readlines()
                        x=int("".join(output).rfind("rate:"))
                        
                        y=int("".join(output).rfind("%"))
                                
                        
                        
                        z="".join(output)[x+5:y].strip()
                        
                        session.close()

                        session = paramiko.SSHClient()
                        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        session.connect('10.51.2.7', port=22, username= 'ing_onap', password='Ingenierie@!23')
                        stdin, stdout, stderr = session.exec_command("dis int eth3 | no-more")
                        output= []
                        output = stdout.readlines()
                        x1=int("".join(output).rfind("rate:"))
                        
                        y1=int("".join(output).rfind("%"))
                                
                        
                        
                        z1="".join(output)[x1+5:y1].strip()
                        
                        som=round((float(z)+float(z1)),2)
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(som>=dimens.percent):
                            dimens.percent= som 
                            print(dimens.percent)
                            dimens.save() 
                        session.close()
                     if  (i[1]=="TUN_0005-NAB_0080-NAB_0009-NAB_0002-NAB_0037-NAB-NAB_0038-NAB_0052-TUN_0091"):
                        session = paramiko.SSHClient()
                        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        session.connect('10.51.2.2', port=22, username= 'ing_onap', password='Ingenierie@!23')
                        stdin, stdout, stderr = session.exec_command("dis int eth7 | no-more")
                        output= []
                        output = stdout.readlines()
                        x=int("".join(output).rfind("rate:"))
                        
                        y=int("".join(output).rfind("%"))
                                
                        
                        
                        z="".join(output)[x+5:y].strip()
                        
                        session.close()
                         

                        
                        session = paramiko.SSHClient()
                        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        session.connect('10.51.2.4', port=22, username= 'ing_onap', password='Ingenierie@!23')
                        stdin, stdout, stderr = session.exec_command("dis int eth7 | no-more")
                        output= []
                        output = stdout.readlines()
                        x1=int("".join(output).rfind("rate:"))
                        
                        y1=int("".join(output).rfind("%"))
                                
                        
                        
                        z1="".join(output)[x1+5:y1].strip()
                        
                        som=round((float(z)+float(z1)),2)
                        dimens=Dimens.objects.get(liaison=i[1])
                        print(dimens.percent)
                        if(som>=dimens.percent):
                            dimens.percent= som 
                            print(dimens.percent)
                            dimens.save() 
                        session.close()
                else:
                     

                    cherch=int(i[2].find("/"))
                    loop1=i[2][:cherch]
                    loop2= i[2][cherch+1:]
                    cherchinter=int(i[6].find("/"))
                    loop1inter=i[6][:cherchinter]
                    loop2inter= i[6][cherchinter+1:]
                    cmddis="dis int "
                    cmdnomore=" | no-more "
                    
                    cmdBB1=cmddis+loop1inter+cmdnomore
                    cmdBB2=cmddis+loop2inter+cmdnomore
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(loop1, username='ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = ssh.exec_command(cmdBB1)
                   
                    output = stdout.readlines()
                    x=int("".join(output).find("utility rate:"))
                        
                    y=int("".join(output).find("%"))
                                
                        
                        
                    z="".join(output)[x+13:y].strip() 
                    
                    
                     
                    ssh.close()
                    

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(loop2, username='ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = ssh.exec_command(cmdBB2)
                    output=stdout.readlines()
                    x1=int("".join(output).find("utility rate:"))
                        
                    y1=int("".join(output).find("%"))
                                
                        
                        
                    z1="".join(output)[x1+13:y1].strip()
                        
                    som=round((float(z)+float(z1)),2)
                    dimens=Dimens.objects.get(liaison=i[1])
                    print(dimens.percent)
                    if(som>=dimens.percent):
                            dimens.percent= som 
                            print(dimens.percent)
                            dimens.save() 
                         
                     
                     
                    ssh.close()   
     except:        
         (list_result).index(i)+1


def reset():
    print("supression de données")
    dim=Dimens.objects.all().values_list()
    for i in dim:
        dimens=Dimens.objects.get(liaison=i[1])
        dimens.percent=0
        dimens.save() 


def bh():
     
    bh_sharing=(Bh_sharing.objects.all().values_list())
    list_result = [entry for entry in bh_sharing]
    
    for i in (list_result):
      
            print(i[1])
            if (i[1]!="MX-KASBAH")  :     

                cmdcmd=cmdbhsharingout+i[4]+cmdno
                try:    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdcmd)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                    
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()
                     
                    print(float(z))
                    bh=Bh_sharing.objects.get(liaison=i[1])
                    print(bh.percent)
                    if(float(z)>=bh.percent):
                        bh.percent= float(z) 
                        print(bh.percent)
                        bh.save()
                    session.close()
                
                
                except:
                     (list_result).index(i)+1
            if (i[1]=="MX-KASBAH")  :
                try: 
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect('10.0.0.15', port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command("show interfaces ae10  | no-more ")
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).find("Input rate     :"))
                                        
                    y=int("".join(output).find("Logical"))
                                        
                                                
                    session.close()
                    TN1TN2="".join(output)[x:y].strip()
                                    
                    x1=int(TN1TN2.find(":"))
                    y1=int(TN1TN2.find("bps"))
                                        
                    x2=int(TN1TN2.rfind(":"))
                    y2=int(TN1TN2.rfind("bps"))
                                        
                    gw1=float(TN1TN2[x1+1:y1].strip())
                    gw2=float(TN1TN2[x2+1:y2].strip())
                    gw1Giga=round(gw1*100/21474836480,2)
                    gw2Giga=round(gw2*100/21474836480,2)
                    print(gw1Giga)
                    print(gw2Giga)
                    if (gw1Giga>gw2Giga):
                        
                            dimens=Bh_sharing.objects.get(liaison=i[1])
                            print(dimens.percent)
                            if(gw1Giga>=dimens.percent):
                                dimens.percent= gw1Giga
                                print(dimens.percent)
                                dimens.save()
                    else:
                            dimens=Bh_sharing.objects.get(liaison=i[1])
                            print(dimens.percent)
                            if(gw2Giga>=dimens.percent):
                                dimens.percent= gw2Giga 
                                print(dimens.percent)
                                dimens.save()
                 
                except:
                     (list_result).index(i)+1

def resetsharing():
    print("supression de données BH")
    bh=Bh_sharing.objects.all().values_list()
    for i in bh:
        bhs=Bh_sharing.objects.get(liaison=i[1])
        bhs.percent=0
        bhs.save() 



def fn_fo_fh():
     
    DEVICE_LIST =['10.51.2.' + str(n) for n in range(1,217)]
    for RTR in DEVICE_LIST:
        print ('\n #### Connecting to the device ' + RTR + '####\n' )
    
        if RTR=="10.51.2.205" or RTR=="10.51.2.103" or RTR=="10.51.2.60" or RTR=="10.51.2.57" or RTR=="10.51.2.58" or RTR=="10.51.2.66" or RTR=="10.51.2.68" or RTR=="10.51.2.71" or RTR=="10.51.2.33":
            DEVICE_LIST.index(RTR)+1
        else:

            try:
                
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username= 'ing_onap', password='Ingenierie@!23', look_for_keys=False, allow_agent=False)
                
                stdin, stdout, stderr = session.exec_command("dis int desc | i TO_FN_F |  no-more")
                output= []
            
                output = stdout.readlines()
                
                session.close()
                
                sub_l = [i for i in output if i.startswith('GE') ]
                for i in sub_l:
                    x=int(i.find("up"))
                    y=int(i.rfind("down"))
                    z=int(i.rfind("up"))
                    print("interface")
                    interface=i[:x].strip()
                    print(interface)
                    gb=int(interface.find("(10G)"))
                    print("description")
                    if y!=-1  :
                        desc=(i[y+4:]).strip()
                        print(desc)
                    else:
                        desc=(i[z+2:]).strip()

                        print(desc)
                    print("trafic")
                    if (gb==-1):
                        cmdcmd=cmdbh+interface[2:]+cmdno
                        fnfn=list(FN.objects.filter(description=desc,interface=interface,routeur=RTR))
                        if (len(fnfn)==0):
                        
                            session = paramiko.SSHClient()
                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            session.connect(RTR, port=22, username= 'ing_onap', password='Ingenierie@!23', look_for_keys=False, allow_agent=False)
                        
                            stdin, stdout, stderr = session.exec_command(cmdcmd)
                            output= []
                        
                            output = stdout.readlines()
                            x=int("".join(output).rfind("rate:"))
                                
                            y=int("".join(output).rfind("%"))
                                        
                                
                                
                            z="".join(output)[x+5:y].strip()
                            percent=round(float(z),2)
                            print(percent)
                            session.close()
                            fn=FN(description=desc,interface=interface,routeur=RTR,percent=percent,capa="1G",date=datetime.now())
                            fn.save()
                    else:
                        cmdcmd=cmdbh+interface[2:gb]+cmdno
                        fnfn=list(FN.objects.filter(description=desc,interface=interface[:gb],routeur=RTR))
                        if (len(fnfn)==0):
                        
                            session = paramiko.SSHClient()
                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            session.connect(RTR, port=22, username= 'ing_onap', password='Ingenierie@!23', look_for_keys=False, allow_agent=False)
                        
                            stdin, stdout, stderr = session.exec_command(cmdcmd)
                            output= []
                        
                            output = stdout.readlines()
                            x=int("".join(output).rfind("rate:"))
                                
                            y=int("".join(output).rfind("%"))
                                        
                                
                                
                            z="".join(output)[x+5:y].strip()
                            percent=round(float(z),2)
                            print(percent)
                            session.close()
                            fn=FN(description=desc,interface=interface[:gb],routeur=RTR,percent=percent,capa="10G",date=datetime.now())
                            fn.save()
            except :
                
                DEVICE_LIST.index(RTR)+1






def dimfn():
     
    fn_fo_fh=(FN.objects.all().values_list())
    list_result = [entry for entry in fn_fo_fh]
    
    for i in (list_result):
      
                print(i[1])
                
                interface=i[2]      
                cmdcmd=cmdbh+interface[2:]+cmdno
                try:    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[3], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdcmd)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                    
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()
                     
                    print(round(float(z),2))
                    fn=FN.objects.get(description=i[1])
                    print(fn.percent)
                    if(float(z)>=fn.percent):
                        fn.percent= float(z) 
                        print(fn.percent)
                        fn.save()
                    session.close()
                except:
                     (list_result).index(i)+1

def resetFN():
    print("supression de données FN")
     
    fn_fo_fh=(FN.objects.all().values_list())
    for i in fn_fo_fh:
        fnfn=FN.objects.get(description=i[1])
        fnfn.percent=0
        fnfn.save() 

def del_FN():
    fn_fo_fh=(FN.objects.all())
     
    fn_fo_fh.all().delete()



def dim_sw():
     
    Bhswitch=(Switch.objects.all().values_list())
    list_result = [entry for entry in Bhswitch]
    
    for i in (list_result):
      
                
            x=i[4].find("10.")
            loop=(i[4][x:]).strip()  
            
            
      
            cmdcmdtr=cmdtrunk+i[5]+cmdno    
            try:    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(loop, port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(cmdcmdtr)
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).rfind("rate:"))
                        
                    y=int("".join(output).rfind("%"))
                            
                     
                     
                    z="".join(output)[x+5:y].strip()


                    x1=int("".join(output).find("utility rate:"))
                    
                    y1=int("".join(output).find("%"))
                    z1="".join(output)[x1+13:y1].strip()
                    print(i[1] )
                    print("IN",z1)
                    print("OUT",z)
                    if (float(z)>=float(z1)):
                     
                        bh=Switch.objects.get(namedevice=i[1])
                        print("Valeur BD",bh.percent)
                        
                        if(float(z)>=bh.percent):
                            bh.percent= float(z) 
                            print("Valeur Enregistrée",bh.percent)
                            bh.save()
                    else:
                       
                         
                        bh=Switch.objects.get(namedevice=i[1])
                        print("Valeur BD",bh.percent)
                        if(float(z1)>=bh.percent):
                            bh.percent= float(z1) 
                            print("Valeur Enregistrée",bh.percent)
                            bh.save()
                     
                    session.close()
                
         
                 
            except:
                     (list_result).index(i)+1
def resetsw():
    print("supression de données SW")
     
    fn_fo_fh=(Switch.objects.all().values_list())
    for i in fn_fo_fh:
        fnfn=Switch.objects.get(namedevice=i[1])
        fnfn.percent=0
        fnfn.save() 

def dimmemorycpu():
     
    ne40=(Routeur.objects.all().values_list())
    list_result = [entry for entry in ne40]
    
    for i in (list_result):
      
                print(i[1])
                
                 
                try:    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command("dis memory-usage | i Memory Using Percentage Is")
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).find("Is:"))
                    
                    y=int("".join(output).find("%"))
                            
                     
                     
                    z="".join(output)[x+3:y].strip()
                     
                    print(round(float(z),2))
                    memory=Routeur.objects.get(name=i[1])
                    print(memory.percentmemory)
                    if(float(z)>=memory.percentmemory):
                        memory.percentmemory= float(z) 
                        print(memory.percentmemory)
                        memory.save()
                    session.close()
                except:
                     (list_result).index(i)+1
                try:    
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(i[2], port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command("dis cpu-usage | i System cpu use rate is")
                    output= []
                    output = stdout.readlines()
                    x=int("".join(output).find("is :"))
                    
                    y=int("".join(output).find("%"))
                            
                     
                     
                    z="".join(output)[x+4:y].strip()
                     
                    print(round(float(z),2))
                    cpu=Routeur.objects.get(name=i[1])
                    print(cpu.percentcpu)
                    if(float(z)>=cpu.percentcpu):
                        cpu.percentcpu= float(z) 
                        print(cpu.percentcpu)
                        cpu.save()
                    session.close()
                except:
                     (list_result).index(i)+1


def resetdimcpu():
    print("supression de données CPU MEMORY")
     
    cpucpu=(Routeur.objects.all().values_list())
    for i in cpucpu:
        cpumem=Routeur.objects.get(name=i[1])
        cpumem.percentmemory=0
        cpumem.percentcpu=0
        cpumem.save() 


def generatenode():
      
    node=Node.objects.all()
    
    node.all().delete()
    
    time.sleep(5)
   #print(time.strftime('%H:%M:%S'),multiprocessing.current_process().name + " Obtenir le fonctionnement de la serrure");
    DEVICE_LIST =['10.51.2.' + str(n) for n in range(1,217)]

    for RTR in DEVICE_LIST:
        print ('\n #### Connecting to the device ' + RTR + '####\n' )
        if RTR=="10.51.2.205" or RTR=="10.51.2.103" or RTR=="10.51.2.60" or RTR=="10.51.2.57" or RTR=="10.51.2.58" or RTR=="10.51.2.66" or RTR=="10.51.2.68" or RTR=="10.51.2.71" or RTR=="10.51.2.33":
            DEVICE_LIST.index(RTR)+1
        else:
          try:  
               
              session = paramiko.SSHClient()
              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              session.connect(RTR, port=22, username= 'mhammouda', password='mh@mm0ud@')
                      
              stdin, stdout, stderr = session.exec_command("dis cu | section i network-entity   | no-more")
              
                      
              output = stdout.readlines()
              session.close()
               
              sub_l = [i for i in output if i.startswith(' is-name')  ]
              sub_l_sysid=[i for i in output if i.startswith(' network-entity')  ]
               
              name_Device="".join(sub_l[0][9:]).strip()
              sysID="".join(sub_l_sysid[0][15:]).strip()
               
              
              
              
              
              CMD="dis isis spf-tree systemid "+sysID[8:]
               
                          #print(CMD_COST)
              no_more=" | no-more"
              session = paramiko.SSHClient()
              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              session.connect(RTR, port=22, username= 'mhammouda', password='mh@mm0ud@')
                      
              stdin, stdout, stderr = session.exec_command(CMD+no_more)
              
                      
              output_LINK = stdout.readlines()
              session.close()
              sub_l_LINK = [i for i in output_LINK if i.startswith('                                        ->')  ]
              sub_l_source=[i for i in output_LINK if i.startswith('>')  ]
              Find_Node_Flag="".join(sub_l_source).strip().find("-/-/-/-   0")
              Find_Node="".join(sub_l_source).strip().find(">")
              #print(sub_l_source[0][Find_Node+1:Find_Node_Flag])
              source=(sub_l_source[0][Find_Node+1:Find_Node_Flag]).strip()
              list_node=list(Node.objects.filter(id_node=source ))
              if(len(list_node)==0):
                  node=Node(id_node=source,name=name_Device,device_type='router',x=random.randint(100,2000),y=random.randint(2000,4000))
                  node.save()
                
           
          except:

            DEVICE_LIST.index(RTR)+1  


def generatelink():
    topology_dict_LINK = {'links': []} 
    LIST_NODE=[] 
    link=Link.objects.all()
     
    link.all().delete() 
    time.sleep(5)
    #print(time.strftime('%H:%M:%S'),multiprocessing.current_process().name + " Obtenir le fonctionnement de la serrure");
    DEVICE_LIST =['10.51.2.' + str(n) for n in range(1,217)]
    for RTR in DEVICE_LIST:
        print ('\n #### Connecting to the device ' + RTR + '####\n' )
        if RTR=="10.51.2.205" or RTR=="10.51.2.103" or RTR=="10.51.2.60" or RTR=="10.51.2.57" or RTR=="10.51.2.58" or RTR=="10.51.2.66" or RTR=="10.51.2.68" or RTR=="10.51.2.71" or RTR=="10.51.2.33":
            DEVICE_LIST.index(RTR)+1
        else:
            try:   
              session = paramiko.SSHClient()
              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              session.connect(RTR, port=22, username= 'mhammouda', password='mh@mm0ud@')
                      
              stdin, stdout, stderr = session.exec_command("dis cu | section i network-entity   | no-more")
              
                      
              output = stdout.readlines()
              session.close()
               
              sub_l = [i for i in output if i.startswith(' is-name')  ]
              sub_l_sysid=[i for i in output if i.startswith(' network-entity')  ]
               
              name_Device="".join(sub_l[0][9:]).strip()
              sysID="".join(sub_l_sysid[0][15:]).strip()
              #print(name_Device)
              #print(sysID)
              
              
              
              
              CMD="dis isis spf-tree systemid "+sysID[8:]
              print(CMD)
                          #print(CMD_COST)
              no_more=" | no-more"
              session = paramiko.SSHClient()
              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              session.connect(RTR, port=22, username= 'mhammouda', password='mh@mm0ud@')
                      
              stdin, stdout, stderr = session.exec_command(CMD+no_more)
              
                      
              output_LINK = stdout.readlines()
              session.close()
              sub_l_LINK = [i for i in output_LINK if i.startswith('                                        ->')  ]
              sub_l_source=[i for i in output_LINK if i.startswith('>')  ]
              Find_Node_Flag="".join(sub_l_source).strip().find("-/-/-/-   0")
              Find_Node="".join(sub_l_source).strip().find(">")
              #print(sub_l_source[0][Find_Node+1:Find_Node_Flag])
              source=(sub_l_source[0][Find_Node+1:Find_Node_Flag]).strip()
              for i_link in sub_l_LINK:
                     
                    find_D=i_link.strip().rfind(" D")
                    find_U=i_link.strip().rfind(" U")
                    find_F=i_link.strip().rfind(" F")
                    
                    if find_D!=-1:
                        name_Device_Destination=(i_link.strip()[2:find_D]).strip()
                        cost_link=(i_link.strip()[find_D+2:]).strip()
                        target= name_Device_Destination
                        if (cost_link).isdigit():
                                cost_link=int(cost_link)
                            
                        list_link=list(Link.objects.filter(source=source,target=target))
                        list_link1=list(Link.objects.filter(source=target,target=source,srcUtilMap=cost_link))
                        if(len(list_link)==0) and (len(list_link1)==0) :
                            link=Link(src_name=name_Device,dist_name=name_Device_Destination,source=source,target=target,srcUtilMap=cost_link)
                            link.save()
                    
                    if find_U!=-1:
                        name_Device_Destination=(i_link.strip()[2:find_U]).strip()
                        cost_link=(i_link.strip()[find_U+2:]).strip()
                        target= name_Device_Destination
                        if (cost_link).isdigit():
                            cost_link=int(cost_link)
                            
                        list_link=list(Link.objects.filter(source=source,target=target))
                        list_link1=list(Link.objects.filter(source=target,target=source,srcUtilMap=cost_link))
                        if(len(list_link)==0) and (len(list_link1)==0) :
                            link=Link(src_name=name_Device,dist_name=name_Device_Destination,source=source,target=target,srcUtilMap=cost_link)
                            link.save()
                      
                    if find_F!=-1:
                        name_Device_Destination=(i_link.strip()[2:find_F]).strip()
                        cost_link=(i_link.strip()[find_F+2:]).strip()
                        target= name_Device_Destination
                    
                        
                        if (cost_link).isdigit():
                                cost_link=int(cost_link)
                            
                        list_link=list(Link.objects.filter(source=source,target=target))
                        list_link1=list(Link.objects.filter(source=target,target=source,srcUtilMap=cost_link))
                        if(len(list_link)==0) and (len(list_link1)==0) :
                            link=Link(src_name=name_Device,dist_name=name_Device_Destination,source=source,target=target,srcUtilMap=cost_link)
                            link.save()

            except:

                DEVICE_LIST.index(RTR)+1

import re
def reportingservice():
    reportingservice = ReportingB2BService.objects.all()

    reportingservice.all().delete()
    time.sleep(5)
    print("I am a scheduled job")
    commands = ['dis ip vpn-instance Internet_vpn interface |  begin Interface | exclude Eth | exclude Gi | no-more ',
                'dis ip vpn-instance Voice_vpn interface |  begin Interface | exclude Eth | exclude Gi | no-more ',
                'dis mac-address vsi BUSINESS-CLIENT-VSI | no-more ', 'dis mac-address vsi BUSINESS-VSI | no-more ',
                'dis mpls l2vc brief | no-more ']

    DEVICE_LIST = ['10.51.2.' + str(n) for n in range(1, 217)]

    for RTR in DEVICE_LIST:
        print('\n #### Connecting to the device ' + RTR + '####\n')
        if RTR == "10.51.2.205" or RTR == "10.51.2.103" or RTR == "10.51.2.60" or RTR == "10.51.2.57" or RTR == "10.51.2.58" or RTR == "10.51.2.66" or RTR == "10.51.2.68" or RTR == "10.51.2.71" or RTR == "10.51.2.33":
            DEVICE_LIST.index(RTR) + 1
        else:
            try:
                # Service Internet
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username='mhammouda', password='mh@mm0ud@', look_for_keys=False,
                                allow_agent=False)

                stdin, stdout, stderr = session.exec_command(commands[0])

                output = stdout.readlines()
                session.close()
                sub_l = [i for i in output if i.startswith('  Interface Number :')]

                print("Service Internet")
                if len(sub_l) == 0:
                    print("Info: The VPN instance does not exist")
                    nbr_service_internet = 0
                    print(nbr_service_internet)
                else:
                    for i in sub_l:
                        index2pt = int(i.find(":"))

                        nbr_service_internet = int((i[index2pt + 1:]).strip())
                        print(nbr_service_internet)




                # Service VOIP
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username='mhammouda', password='mh@mm0ud@', look_for_keys=False,
                                allow_agent=False)

                stdin, stdout, stderr = session.exec_command(commands[1])

                output = stdout.readlines()
                session.close()
                sub_l = [i for i in output if i.startswith('  Interface Number :')]

                print("Service VOIP")
                if len(sub_l) == 0:
                    print("Info: The VPN instance does not exist")
                    nbr_service_voip = 0
                    print(nbr_service_voip)
                else:
                    for i in sub_l:
                        index2pt = int(i.find(":"))

                        nbr_service_voip = int((i[index2pt + 1:]).strip())
                        print(nbr_service_voip)





                # Service BUSINESS-CLIENT-VSI
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username='mhammouda', password='mh@mm0ud@', look_for_keys=False,
                                allow_agent=False)

                stdin, stdout, stderr = session.exec_command(commands[2])

                output = stdout.readlines()
                session.close()
                sub_l = [i for i in output if i.startswith('Total matching items on slot')]

                print("Service BUSINESS-CLIENT-VSI")
                if len(sub_l) == 0:
                    print("Info: The VSI does not exist")
                    nbr_service_BUSSNESCLIENTVSI = 0
                    print(nbr_service_BUSSNESCLIENTVSI)
                else:

                    index2pt = int(sub_l[0].find("="))

                    nbr_service_BUSSNESCLIENTVSI = int((sub_l[0][index2pt + 1:]).strip())
                    print(nbr_service_BUSSNESCLIENTVSI)




                # Service BUSINESS-VSI
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username='mhammouda', password='mh@mm0ud@', look_for_keys=False,
                                allow_agent=False)

                stdin, stdout, stderr = session.exec_command(commands[3])

                output = stdout.readlines()
                session.close()
                sub_l = [i for i in output if i.startswith('Total matching items on slot')]

                print("Service BUSINESS-VSI")
                if len(sub_l) == 0:
                    print("Info: The VSI does not exist")
                    nbr_service_BUSINESS_VSI = 0
                    print(nbr_service_BUSINESS_VSI)
                else:

                    index2pt = int(sub_l[0].find("="))

                    nbr_service_BUSINESS_VSI = int((sub_l[0][index2pt + 1:]).strip())
                    print(nbr_service_BUSINESS_VSI)




                # Service L2VC
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(RTR, port=22, username='mhammouda', password='mh@mm0ud@', look_for_keys=False,
                                allow_agent=False)

                stdin, stdout, stderr = session.exec_command(commands[4])

                output = stdout.readlines()
                session.close()
                sub_l = [i for i in output if i.startswith(' Total LDP VC :')]

                print("Service L2VC")
                if len(sub_l) == 0:
                    print("Info: The VPN instance does not exist")
                    nbr_service_L2VC = 0
                    print(nbr_service_L2VC)
                else:
                    for i in sub_l:
                        nombres = re.findall("\d+", i)

                        nbr_service_L2VC = int(nombres[0])
                        print(nbr_service_L2VC)

                reportingB2BService=ReportingB2BService(name_device=RTR,nbr_service_Internet=nbr_service_internet,nbr_service_voip=nbr_service_voip,nbr_service_L2VC=nbr_service_L2VC,nbr_service_BUSINESS_CLIENT_VSI=nbr_service_BUSSNESCLIENTVSI,nbr_service_BUSINESS_VSI=nbr_service_BUSINESS_VSI)
                reportingB2BService.save()
            except:

                DEVICE_LIST.index(RTR) + 1