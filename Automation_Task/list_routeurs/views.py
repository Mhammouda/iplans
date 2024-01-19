 
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
import paramiko
import  ipaddress 
import re
from .serializers import  ServiceSerializer ,ScriptSerializer
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import status
 
 
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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


#@allowed_Users(allowredGroups=['admin'])
@login_required(login_url='login')
@forAdmins
def home(request):
     NE40=Routeur.objects.all()
     user=User.objects.all()
     switch=Switch.objects.all()
     
     nbr_user=user.count()
     nbrN40=NE40.count()
     nbrsw=switch.count()
     Nbr_Script=Script.objects.all()
     
     tot_script=Nbr_Script.count()
     delService=DelService.objects.all()
     Nbr_Del_service=delService.count()
     service=Service.objects.all()
     tot_Service=service.count()
     l2vc=L2VC.objects.all()
     totL2VC=l2vc.count()
     context={'NE40':NE40 , 'user':user,'switch':switch, 'Nbr_Script':Nbr_Script ,
              'tot_script':tot_script,
              'nbr_user':nbr_user,
              'nbrN40':nbrN40, 'Nbr_Del_service':Nbr_Del_service,
              'tot_Service':tot_Service,'totL2VC':totL2VC ,'nbrsw':nbrsw}




     return render(request, 'liste_routeur/dashboard.html',context)

@login_required(login_url='login')
@forAdmins
def routeur(request):
     NE40=Routeur.objects.all()
     return render(request, 'liste_routeur/routeur.html',{'NE40':NE40})

@login_required(login_url='login')
@forAdmins
def SW(request):
     return render(request, 'liste_routeur/switch.html')

 
 


 
@login_required(login_url='login')
@forCustomer
def MX(request,pk):
    
     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     time=[]
     percent=[]
      
     item=list(Trafic.objects.filter(routeur=looprr).values_list('percent','date'))
     
     for courbe in item:
          time.append(courbe[1].strftime("%m/%d/%Y, %H:%M:%S"))
          percent.append(courbe[0])
      
     context={
          'looprr':looprr,
          'labels':time,
          'data':percent
     }
     return render(request, 'liste_routeur/MX.html',context)
 
@login_required(login_url='login')
@forCustomer
def SC(request):
     script=Script.objects.all()
     l2VC=L2VC.objects.all()
     service=Service.objects.all()
     servicemanuel=ServiceManuel.objects.all()
     delService=DelService.objects.all()
    
     
      
      
      

 
     
     context={'script':script,'service':service,'servicemanuel':servicemanuel,'delService':delService,'l2VC':l2VC}
     return render(request, 'liste_routeur/script.html',context)



#Pour visiteur

@login_required(login_url='login')
@forVisiteur
def Visiteur(request):
     

     script=Script.objects.all()
     l2VC=L2VC.objects.all()
     service=Service.objects.all()
     delService=DelService.objects.all()
     paginator = Paginator(script,4)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)

     paginator1 = Paginator(l2VC,2)
     page_number1 = request.GET.get('page')
     page_obj1 = paginator1.get_page(page_number1)

     paginator2 = Paginator(service,1)
     page_number2 = request.GET.get('page')
     page_obj2 = paginator2.get_page(page_number2)

     paginator3 = Paginator(delService,4)
     page_number3 = request.GET.get('page')
     page_obj3 = paginator3.get_page(page_number3)
     
      
      
      

 
     
     context={'script':script,'page_obj':page_obj,'page_obj1':page_obj1,'page_obj2':page_obj2,'page_obj3':page_obj3,'service':service,'delService':delService,'l2VC':l2VC}
     return render(request, 'liste_routeur/visiteur.html',context)







@login_required(login_url='login')
@forAdmins
def SCADMIN(request):
     script=Script.objects.all()
     l2VC=L2VC.objects.all()
     service=Service.objects.all()
     servicemanuel=ServiceManuel.objects.all()
     delService=DelService.objects.all()
     
     
      

 
     
     context={'script':script, 'servicemanuel':servicemanuel,'service':service,'delService':delService,'l2VC':l2VC}
     return render(request, 'liste_routeur/scriptadmin.html',context)

@login_required(login_url='login')
@forAdmins
def SCADMINBBIP(request):
     try:
      
          dim=Dimens.objects.all().values_list()
          if request.method=='POST':
               for i in dim:
                    dimens=Dimens.objects.get(liaison=i[1])
                    dimens.percent=0
                    dimens.save() 
                    
               return redirect('/')
          context={'dim':dim}
          return render(request, 'liste_routeur/RAZ_DIM_IP_CONFIRMATION.html',context)
     except:
          return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forAdmins
def SCADMINBBTRAFIC(request):
    try:

        trafic = Trafic.objects.all()


        if request.method == 'POST':
            trafic.all().delete()

            return redirect('/')
        context = {'trafic': trafic}
        return render(request, 'liste_routeur/RAZ_TRAFIC_IP_CONFIRMATION.html', context)
    except:
        return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forAdmins
def SCADMINBH(request):
     try:
      
           
          bh=Bh_sharing.objects.all().values_list()
          
          if request.method=='POST':
               for i in bh:
                    bhs=Bh_sharing.objects.get(liaison=i[1])
                    bhs.percent=0
                    bhs.save()
                    
               return redirect('/')
          context={'bh':bh}
          return render(request, 'liste_routeur/RAZ_DIM_BH_CONFIRMATION.html',context)
     except:
          return render(request, 'liste_routeur/Erreursupp.html')
     

@login_required(login_url='login')
@forAdmins
def SCADMINFN(request):
     try:
      
          fn_fo_fh=(FN.objects.all().values_list())
          if request.method=='POST':
               for i in fn_fo_fh:
                    fnfn=FN.objects.get(description=i[1])
                    fnfn.percent=0
                    fnfn.save() 
                    
               return redirect('/')
          context={'fn_fo_fh':fn_fo_fh}
          return render(request, 'liste_routeur/RAZ_DIM_FN_CONFIRMATION.html',context)
     except:
          return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forAdmins
def SCADMINSW(request):
     try:
      
          fn_fo_fh=(Switch.objects.all().values_list())
          if request.method=='POST':
               for i in fn_fo_fh:
                    fnfn=Switch.objects.get(namedevice=i[1])
                    fnfn.percent=0
                    fnfn.save() 
                    
               return redirect('/')
          context={'fn_fo_fh':fn_fo_fh}
          return render(request, 'liste_routeur/RAZ_DIM_SW_CONFIRMATION.html',context)
     except:
          return render(request, 'liste_routeur/Erreursupp.html')



@login_required(login_url='login')
@forAdmins
def SCADMINCPU(request):
     try:
      
          cpucpu=(Routeur.objects.all().values_list())
          if request.method=='POST':
               for i in cpucpu:
                    cpumem=Routeur.objects.get(name=i[1])
                    cpumem.percentmemory=0
                    cpumem.percentcpu=0
                    cpumem.save() 
                    
               return redirect('/')
          context={'cpucpu':cpucpu}
          return render(request, 'liste_routeur/RAZ_DIM_CPU_CONFIRMATION.html',context)
     except:
          return render(request, 'liste_routeur/Erreursupp.html')



@login_required(login_url='login')
@forAdmins
def create(request):
 try:
     form=RouteurForm()
     if request.method=='POST':
            #print(request.POST)
          form=RouteurForm(request.POST)
          if form.is_valid:
               form.save()
               return render(request, 'liste_routeur/Succesaddrouteur.html')

     context={'form':form}
     return render(request, 'liste_routeur/my_form.html',context)
 except:
  return render(request, 'liste_routeur/erreuraddrouteur.html')

@login_required(login_url='login')
@forAdmins
def adduser(request):
 try:
     form=UserForm()
     if request.method=='POST':
            #print(request.POST)
          form=UserForm(request.POST)
          if form.is_valid:
               form.save()
               return render(request, 'liste_routeur/Succesadduser.html')

     context={'form':form}
     return render(request, 'liste_routeur/register.html',context)
 except:
  return render(request, 'liste_routeur/erreuradduser.html')

@login_required(login_url='login')
@forCustomer
def index(request):
     form=ScriptForm()
     context = {
                    'Title' : 'Upgrade',
                    'Header' : 'Configure B2B',
                    'form' : form,
          }

     try:
          if request.method == 'POST' and "btn1"  in request.POST  :
                    
                    
                    routeur = context['routeur'] = request.POST['routeur']
                
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(" dis int desc | i B2B |  no-more ")

                    outputinet = stdout.readlines()
                      
                    x=int("".join(outputinet).find("GE"))
                    y=int("".join(outputinet).find("Loop0")) 
                    i=("".join(outputinet)[x:y])
                    sub_l = [i for i in outputinet if i.startswith('GE')]
                    for i in sub_l:
                        
                          print(i.rstrip('\n \r'))
                    
                    session.close()
                    form=ScriptForm(request.POST)
                     
                    form.routeur="routeur"
                    form.interface=sub_l
                    context = {
                         'form': form,
                         'interface': sub_l,
                      }
                    return render(request, 'liste_routeur/AddScript.html',context)   
          if request.method == 'POST' and "btn"  in request.POST:     
               debit = context['debit'] = request.POST['debit']
               routeur = context['routeur'] = request.POST['routeur']
               interface = request.POST.get('monselect')          
               bd= "shaping"+debit
               
               qos=  "# qos-profile shaping"+debit
               qu=   "user-queue cir "+ debit+"000 pir "+debit+"000 outbound  "
               ququ="user-queue cir "+ debit+"000 pir "+debit+"000 inbound  "
               
               Inp="qos-profile "+ bd + " outbound identifier none"
               out="qos-profile "+ bd + " inbound identifier none"
                         #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
               rt="<"+routeur+">"      
               
               
               if  interface==None or debit=="":
                         messages.error(request, 'Merci de remplir tout les champs')
               else:

                    x=int(interface.find("up up"))
                    y=int(interface.find("GE"))
                    z=int(interface.find("("))
                    v=int(interface.find("down"))
               
                    interfacece=list(interface)
                    if v==-1:
                         if (z==-1):
                         
                              interfacece=interfacece[2:x]
                         if(z!=-1):
                              interfacece=interfacece[2:z]
                         
                         
                         inter="interface GigabitEthernet"+"".join(interfacece)     
                              
                    
                         
                              
                         strstr="".join(interfacece)
                         serser=list(Script.objects.filter(routeur=routeur,interface=strstr,debit=debit))
               
                         if len(serser)!=0:
                                        messages.error(request, 'Service deja traité')
                         if len(serser)==0:
                              form=ScriptForm(request.POST)
                              if form.is_valid:
                                                  updateser=form.save(commit=False)
                                                  updateser.user=request.user.username
                                                  updateser.interface= "".join(interfacece)
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                  shapingoutput = stdout.readlines()
                                                  bdFIND=bd+" "
                                                  sub_l = [i for i in shapingoutput if i.find(bdFIND)!=-1 ]
                                                  print(sub_l)
                                                  if len(sub_l)!=0:
                                                   
                                                            updateser.generate= rt+ '\n'+inter+'\n'+Inp+'\n'+out   
                                                            form.save()
                                                            messages.success(request, 'Generation de script est effectée avec succes')         
                                                            messages.add_message(request,messages.INFO,"Le Shaping est deja Configuré")          
                                                            context ['result'] = [rt,  inter,Inp,out]
                                                       
                                                  if len(sub_l)==0:           
                                                            updateser.generate= rt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+inter+'\n'+Inp+'\n'+out   
                                                            form.save()
                                                            messages.success(request, 'Generation de script est effectée avec succes')         
                                                            messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectée avec succes")         
                                                            context ['result'] = [rt, qos ,ququ,qu,inter,Inp,out]          
                    else:                    
                              messages.error(request, 'Interface est DOWN')
          return render(request, 'liste_routeur/AddScript.html',context)
     except:
          return render(request, 'liste_routeur/erreurconnect.html',context)

          

@login_required(login_url='login')
@forAdmins
def update(request,pk):

     routeur=Routeur.objects.get(id=pk)
     print(routeur)
     form=RouteurForm(instance=routeur)
     if request.method=='POST':
          form=RouteurForm(request.POST, instance=routeur)
          if form.is_valid():
               form.save()
               return redirect('/')
     context={'form':form}
     return render(request, 'liste_routeur/my_form.html',context)

 



@login_required(login_url='login')
@forAdmins
def updateuser(request,pk):

     user=User.objects.get(id=pk)
     form=UserForm(instance=user)
     if request.method=='POST':
          form=UserForm(request.POST, instance=user)
          if form.is_valid():
               form.save()
               return redirect('/')
     context={'form':form}
     return render(request, 'liste_routeur/my_form.html',context)


@login_required(login_url='login')
@forAdmins
def deleterouteur(request,pk):
  try:
     routeur=Routeur.objects.get(id=pk)
     if request.method=='POST':
          routeur.delete()
          return redirect('/')
     context={'routeur':routeur}
     return render(request, 'liste_routeur/delete_form.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forAdmins
def deleteservice(request,pk):
  try:
     service=Service.objects.get(id=pk)
     if request.method=='POST':
          service.delete()
           
          return redirect('/')
     context={'service':service}
     return render(request, 'liste_routeur/delete_form_service.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forAdmins
def deleteL2VC(request,pk):
  try:
     l2VC=L2VC.objects.get(id=pk)
     if request.method=='POST':
          l2VC.delete()
           
          return redirect('/')
     context={'l2VC':l2VC}
     return render(request, 'liste_routeur/delete_form_l2VC.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')




@login_required(login_url='login')
@forAdmins
def deleteserviceALL(request):
  try:
     service=Service.objects.all()
     if request.method=='POST':
          service.all().delete()
           
          return redirect('/')
     context={'service':service}
     return render(request, 'liste_routeur/delete_form_service_all.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')    



@login_required(login_url='login')
@forAdmins
def deletedelservice(request,pk):
  try:
     delservice=DelService.objects.get(id=pk)
     if request.method=='POST':
          delservice.delete()
           
          return redirect('/')
     context={'delservice':delservice}
     return render(request, 'liste_routeur/delete_form_delservice.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forAdmins
def deletedelserviceALL(request):
  try:
     delserviceall=DelService.objects.all()
     if request.method=='POST':
          delserviceall.all().delete()
           
          return redirect('/')
     context={'delserviceall':delserviceall}
     return render(request, 'liste_routeur/delete_form_dellservice_all.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')    



@login_required(login_url='login')
@forAdmins
def deletedelscript(request,pk):
  try:
     delscript=Script.objects.get(id=pk)
     if request.method=='POST':
          delscript.delete()
           
          return redirect('/')
     context={'delscript':delscript}
     return render(request, 'liste_routeur/delete_form_delscript.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forAdmins
def deletedelscriptALL(request):
  try:
     delscriptall=Script.objects.all()
     if request.method=='POST':
          delscriptall.all().delete()
           
          return redirect('/')
     context={'delscriptall':delscriptall}
     return render(request, 'liste_routeur/delete_form_delscript_all.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')    


@login_required(login_url='login')
@forAdmins
def deletedelscriptMAN(request,pk):
  try:
     delscript=ServiceManuel.objects.get(id=pk)
     if request.method=='POST':
          delscript.delete()
           
          return redirect('/')
     context={'delscript':delscript}
     return render(request, 'liste_routeur/delete_form_delscriptMAN.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forAdmins
def deletedelscriptALLMAN(request):
  try:
     delscriptall=ServiceManuel.objects.all()
     if request.method=='POST':
          delscriptall.all().delete()
           
          return redirect('/')
     context={'delscriptall':delscriptall}
     return render(request, 'liste_routeur/delete_form_delscript_allMAN.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')  


 










@login_required(login_url='login')
@forAdmins
def deleteL2VCALL(request):
  try:
     l2vc=L2VC.objects.all()
     if request.method=='POST':
          l2vc.all().delete()
           
          return redirect('/')
     context={'l2vc':l2vc}
     return render(request, 'liste_routeur/delete_form_L2VC_all.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')  

@login_required(login_url='login')
@forAdmins
def deleteuser(request,pk):
  try:
     user=User.objects.get(id=pk)
     if request.method=='POST':
          user.delete()
          return redirect('/')
     context={'user':user}
     return render(request, 'liste_routeur/delete_form_user.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')

@notLogedUsers
def userLogin(request):

          if  request.method=='POST':
               username=request.POST.get('username')
               password=request.POST.get('password')
               user=authenticate(request, username=username, password=password)
               if user is not None:
                    mylogin(request, user)
                    messages.success(request, 'Bonjour '+username)
                    return redirect('/')
                           
               else :
                    messages.error(request, 'CONNECTION FAILED')


          context={}
          return render(request, 'liste_routeur/login.html',context)




@login_required(login_url='login')
@forAdmins
def register(request):

          form=CreateNewUser()
          if  request.method=='POST':
               form=CreateNewUser(request.POST)
               if form.is_valid():

                    user = form.save()
                    username=form.cleaned_data.get('username')
                    group=Group.objects.get(name="customer")
                    user.groups.add(group)
                    return redirect('login')
          context={'form':form}
          return render(request, 'liste_routeur/register.html',context)


@login_required(login_url='login')
def userlogout(request):

     logout(request)
     return redirect('login')


from django.contrib.auth import update_session_auth_hash

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get("q_Old_Password")
        new_password = request.POST.get("q_new_Password")
        confirmed_new_password = request.POST.get("q_confirm_new_Password")

        if old_password and new_password and confirmed_new_password:
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user.username)
                print(user)
                if not user.check_password(old_password):
                    messages.warning(request, "your old password is not correct!")
                else:
                    if new_password != confirmed_new_password:
                        messages.warning(request, "your new password not match the confirm password !")

                    elif len(new_password) < 8 or new_password.lower() == new_password or \
                            new_password.upper() == new_password or new_password.isalnum() or \
                            not any(i.isdigit() for i in new_password):
                        messages.warning(request, "your password is too weak!")



                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)

                        messages.success(request, "your password has been changed successfuly.!")

                        return redirect('login')

        else:
            messages.warning(request, " sorry , all fields are required !")

    context = {

    }
    return render(request, "liste_routeur/change_password.html", context)


@login_required(login_url='login')
@forCustomer
def userProfile(request):
  
     NE40=Routeur.objects.all()
     listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
     listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
     serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
     print(serviceadressepublic)
     serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
     serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
     print(serviceadresseprive)
     listpublic31=listpublic[0]
     listpublic32=listpublic[1]
     liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))
     liste32 =list(ipaddress.ip_network(listpublic32).subnets(new_prefix=32))
     listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
     listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
     serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
     serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
     if len(serviceadressepublic31) == 0:
                              lenaddpub31=len(liste31)  
                                
     else:
                              for L31 in  serviceadressepublic31:
                                        L31str="".join(L31)
                                        liste31.remove(ipaddress.ip_network(L31str))
                                        lenaddpub31=len(liste31)
                              
                               
     if len(serviceadresseprive) == 0:
                              lenaddpriv=len(listprive)     
     else:
                              for L30 in  serviceadresseprive:
                                        L30str="".join(L30)
                                        listprive.remove(ipaddress.ip_network(L30str))
                                        lenaddpriv=len(listprive)
                              
     if len(serviceadressepublic) == 0:
                              lenaddpub32=len(liste32)      
     else:
                              for L32 in  serviceadressepublic:
                                        L32str="".join(L32)
                                        liste32.remove(ipaddress.ip_network(L32str))
                                        lenaddpub32=len(liste32)

     if len(serviceadressepublic28) == 0:
         lenaddpub28=len(listpuclic28)
     else:
         for L31 in serviceadressepublic28:
             L31str = "".join(L31)
             listpuclic28.remove(ipaddress.ip_network(L31str))
             lenaddpub28=len(listpuclic28)

     if len(serviceadressepublic29) == 0:
         lenaddpub29 = len(listpuclic29)
     else:
         for L31 in serviceadressepublic29:
             L31str = "".join(L31)
             listpuclic29.remove(ipaddress.ip_network(L31str))
             lenaddpub29 = len(listpuclic29)

     nbr_service_Internet = ReportingB2BService.objects.aggregate(Sum('nbr_service_Internet'))
     nbr_service_voip = ReportingB2BService.objects.aggregate(Sum('nbr_service_voip'))
     nbr_service_L2vc = ReportingB2BService.objects.aggregate(Sum('nbr_service_L2VC'))
     nbr_service_BUSINESS_CLIENT_VSI = ReportingB2BService.objects.aggregate(Sum('nbr_service_BUSINESS_CLIENT_VSI'))
     nbr_service_BUSINESS_VSI = ReportingB2BService.objects.aggregate(Sum('nbr_service_BUSINESS_VSI'))


     somme_general_nbr_service_Internet=nbr_service_Internet['nbr_service_Internet__sum']
     somme_general_nbr_service_VOIP=nbr_service_voip['nbr_service_voip__sum']
     somme_general_nbr_service_BUSINESS_CLIENT_VSI=nbr_service_BUSINESS_CLIENT_VSI['nbr_service_BUSINESS_CLIENT_VSI__sum']
     somme_general_nbr_service_BUSINESS_VSI =nbr_service_BUSINESS_VSI['nbr_service_BUSINESS_VSI__sum']
     somme_general_nbr_service_L2vc =nbr_service_L2vc['nbr_service_L2VC__sum']

     print(somme_general_nbr_service_Internet)
     print(somme_general_nbr_service_VOIP)
     print(somme_general_nbr_service_BUSINESS_CLIENT_VSI)
     print(somme_general_nbr_service_BUSINESS_VSI)
     print(somme_general_nbr_service_L2vc)

     service_BUSINESS_CLIENT_VSI_TUN_5_B = (ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_BUSINESS_CLIENT_VSI

      
     service_BUSINESS_CLIENT_VSI_TUN_91_B =(ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_BUSINESS_CLIENT_VSI

     service_BUSINESS_VSI_TUN_5_B =(ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_BUSINESS_VSI
     service_BUSINESS_VSI_TUN_91_B =(ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_BUSINESS_VSI

     service_L2VC_TUN_5_B =(ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_L2VC
     service_L2VC_TUN_91_B =(ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_L2VC
     print("***********")
     print(service_BUSINESS_CLIENT_VSI_TUN_5_B)
     print(service_BUSINESS_CLIENT_VSI_TUN_91_B)
     print(service_BUSINESS_VSI_TUN_5_B)
     print(service_BUSINESS_VSI_TUN_91_B)
     print(service_L2VC_TUN_5_B)
     print(service_L2VC_TUN_91_B)

     final_somme_general_nbr_service_Internet=somme_general_nbr_service_Internet
     final_somme_general_nbr_service_VOIP=somme_general_nbr_service_VOIP
     final_somme_general_nbr_service_BUSINESS_CLIENT_VSI=(service_BUSINESS_CLIENT_VSI_TUN_5_B)
     final_somme_general_nbr_service_BUSINESS_VSI=(service_BUSINESS_VSI_TUN_5_B)
     final_somme_general_nbr_service_L2vc=(service_L2VC_TUN_5_B)+(service_L2VC_TUN_91_B)
     print("***********")
     print(final_somme_general_nbr_service_Internet)
     print(final_somme_general_nbr_service_VOIP)
     print(final_somme_general_nbr_service_BUSINESS_CLIENT_VSI)
     print(final_somme_general_nbr_service_BUSINESS_VSI)
     print(final_somme_general_nbr_service_L2vc)
     script_DEMANDE = Service.objects.filter(etat="DEMANDE").count()
     script_PLANNED = Service.objects.filter(etat="PLANNED").count()
     script_SUCCESS = Service.objects.filter(etat="SUCCESS").count()
     script_REJECTED = Service.objects.filter(etat="REJECTED").count()
     user=User.objects.all()
     switch=Switch.objects.all()
     nbrsw=switch.count()
     nbr_user=user.count()
     nbrN40=NE40.count()
     Nbr_Script=Script.objects.all()
     tot_script=Nbr_Script.count()
     delService=DelService.objects.all()
     Nbr_Del_service=delService.count()
     service=Service.objects.all()
     tot_Service=service.count()
     l2vc=L2VC.objects.all()
     
     servicebyuser=Service.objects.filter(user=request.user.username).count()
     updatebyuser=Script.objects.filter(user=request.user.username).count()
     deletebyuser=DelService.objects.filter(user=request.user.username).count()
     L2VCbyuser=L2VC.objects.filter(user=request.user.username).count()
     smanuelbyuser=ServiceManuel.objects.filter(user=request.user.username).count()
     scriptbyuser= L2VCbyuser + deletebyuser +updatebyuser + servicebyuser + smanuelbyuser
     totL2VC=l2vc.count()
     searchfilter=RouteurFilter(request.GET, queryset=NE40)
     NE40=searchfilter.qs
     paginator = Paginator(NE40,2)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     context={'final_somme_general_nbr_service_L2vc':final_somme_general_nbr_service_L2vc,'final_somme_general_nbr_service_BUSINESS_VSI':final_somme_general_nbr_service_BUSINESS_VSI,'final_somme_general_nbr_service_BUSINESS_CLIENT_VSI':final_somme_general_nbr_service_BUSINESS_CLIENT_VSI,'final_somme_general_nbr_service_VOIP':final_somme_general_nbr_service_VOIP,'final_somme_general_nbr_service_Internet':final_somme_general_nbr_service_Internet,'scriptbyuser':scriptbyuser,'lenaddpriv':lenaddpriv,'lenaddpub31':lenaddpub31,'lenaddpub32':lenaddpub32,'NE40':NE40 ,'switch':switch,'nbrsw':nbrsw,'page_obj':page_obj, 'user':user, 'Nbr_Script':Nbr_Script ,
              'tot_script':tot_script,
              'nbr_user':nbr_user,
              'nbrN40':nbrN40,'searchfilter':searchfilter,
              'Nbr_Del_service':Nbr_Del_service,'tot_Service':tot_Service,'totL2VC':totL2VC,'lenaddpub29':lenaddpub29,'lenaddpub28':lenaddpub28,'script_DEMANDE':script_DEMANDE,'script_PLANNED':script_PLANNED,'script_SUCCESS':script_SUCCESS,'script_REJECTED':script_REJECTED }

     return render(request, 'liste_routeur/profile.html',context)
 

@login_required(login_url='login')
@forCustomer
def userreporting(request):

    listprive = list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
    listpublic = list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
    serviceadressepublic = list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
    print(serviceadressepublic)
    serviceadressepublic31 = list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
    serviceadresseprive = list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
    print(serviceadresseprive)
    listpublic31 = listpublic[0]
    listpublic32 = listpublic[1]
    liste31 = list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))
    liste32 = list(ipaddress.ip_network(listpublic32).subnets(new_prefix=32))
    listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
    listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
    serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
    serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
    if len(serviceadressepublic31) == 0:
        lenaddpub31 = len(liste31)

    else:
        for L31 in serviceadressepublic31:
            L31str = "".join(L31)
            liste31.remove(ipaddress.ip_network(L31str))
            lenaddpub31 = len(liste31)

    if len(serviceadresseprive) == 0:
        lenaddpriv = len(listprive)
    else:
        for L30 in serviceadresseprive:
            L30str = "".join(L30)
            listprive.remove(ipaddress.ip_network(L30str))
            lenaddpriv = len(listprive)

    if len(serviceadressepublic) == 0:
        lenaddpub32 = len(liste32)
    else:
        for L32 in serviceadressepublic:
            L32str = "".join(L32)
            liste32.remove(ipaddress.ip_network(L32str))
            lenaddpub32 = len(liste32)

    if len(serviceadressepublic28) == 0:
        lenaddpub28 = len(listpuclic28)
    else:
        for L31 in serviceadressepublic28:
            L31str = "".join(L31)
            listpuclic28.remove(ipaddress.ip_network(L31str))
            lenaddpub28 = len(listpuclic28)

    if len(serviceadressepublic29) == 0:
        lenaddpub29 = len(listpuclic29)
    else:
        for L31 in serviceadressepublic29:
            L31str = "".join(L31)
            listpuclic29.remove(ipaddress.ip_network(L31str))
            lenaddpub29 = len(listpuclic29)

    adressepriveutilise=len(serviceadresseprive)
    adressepriverestant=lenaddpriv

    adressepublic32utilise = len(serviceadressepublic)
    adressepublic32restant = lenaddpub32

    adressepublic31utilise = len(serviceadressepublic31)
    adressepublic31restant = lenaddpub31

    adressepublic28utilise = len(serviceadressepublic28)
    adressepublic28restant = lenaddpub28

    adressepublic29utilise = len(serviceadressepublic29)
    adressepublic29restant = lenaddpub29

    context = {   'lenaddpriv': lenaddpriv, 'lenaddpub31': lenaddpub31,
               'lenaddpub32': lenaddpub32,
               'lenaddpub29': lenaddpub29, 'lenaddpub28': lenaddpub28,'adressepriveutilise':adressepriveutilise,
                  'adressepriverestant':adressepriverestant,'adressepublic32utilise':adressepublic32utilise,'adressepublic32restant':adressepublic32restant,
                  'adressepublic31utilise':adressepublic31utilise,'adressepublic31restant':adressepublic31restant,
                  'adressepublic28utilise':adressepublic28utilise,'adressepublic28restant':adressepublic28restant,
                  'adressepublic29utilise':adressepublic29utilise,'adressepublic29restant':adressepublic29restant
                  }

    return render(request, 'liste_routeur/suivi_address.html', context)

@login_required(login_url='login')
@forCustomer
def scriptreporting(request):

    script_DEMANDE=Service.objects.filter(etat="DEMANDE").count()
    script_PLANNED = Service.objects.filter(etat="PLANNED").count()
    script_SUCCESS = Service.objects.filter(etat="SUCCESS").count()
    script_REJECTED = Service.objects.filter(etat="REJECTED").count()
    context = {
        'script_DEMANDE':script_DEMANDE,'script_PLANNED':script_PLANNED,'script_SUCCESS':script_SUCCESS,'script_REJECTED':script_REJECTED
                  }

    return render(request, 'liste_routeur/suivi_script.html', context)

@login_required(login_url='login')
@forCustomer
def reportingB2B(request):
 try:
    reportingB2B = ReportingB2BService.objects.all()
    nbr_service_Internet = ReportingB2BService.objects.aggregate(Sum('nbr_service_Internet'))
    nbr_service_voip = ReportingB2BService.objects.aggregate(Sum('nbr_service_voip'))
    nbr_service_L2vc = ReportingB2BService.objects.aggregate(Sum('nbr_service_L2VC'))
    nbr_service_BUSINESS_CLIENT_VSI = ReportingB2BService.objects.aggregate(Sum('nbr_service_BUSINESS_CLIENT_VSI'))
    nbr_service_BUSINESS_VSI = ReportingB2BService.objects.aggregate(Sum('nbr_service_BUSINESS_VSI'))

    somme_general_nbr_service_Internet = nbr_service_Internet['nbr_service_Internet__sum']
    somme_general_nbr_service_VOIP = nbr_service_voip['nbr_service_voip__sum']
    somme_general_nbr_service_BUSINESS_CLIENT_VSI = nbr_service_BUSINESS_CLIENT_VSI[
        'nbr_service_BUSINESS_CLIENT_VSI__sum']
    somme_general_nbr_service_BUSINESS_VSI = nbr_service_BUSINESS_VSI['nbr_service_BUSINESS_VSI__sum']
    somme_general_nbr_service_L2vc = nbr_service_L2vc['nbr_service_L2VC__sum']

    print(somme_general_nbr_service_Internet)
    print(somme_general_nbr_service_VOIP)
    print(somme_general_nbr_service_BUSINESS_CLIENT_VSI)
    print(somme_general_nbr_service_BUSINESS_VSI)
    print(somme_general_nbr_service_L2vc)

    service_BUSINESS_CLIENT_VSI_TUN_5_B = (
        ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_BUSINESS_CLIENT_VSI

    service_BUSINESS_CLIENT_VSI_TUN_91_B = (
        ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_BUSINESS_CLIENT_VSI

    service_BUSINESS_VSI_TUN_5_B = (ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_BUSINESS_VSI
    service_BUSINESS_VSI_TUN_91_B = (ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_BUSINESS_VSI

    service_L2VC_TUN_5_B = (ReportingB2BService.objects.get(name_device="10.51.2.2")).nbr_service_L2VC
    service_L2VC_TUN_91_B = (ReportingB2BService.objects.get(name_device="10.51.2.4")).nbr_service_L2VC
    print("***********")
    print(service_BUSINESS_CLIENT_VSI_TUN_5_B)
    print(service_BUSINESS_CLIENT_VSI_TUN_91_B)
    print(service_BUSINESS_VSI_TUN_5_B)
    print(service_BUSINESS_VSI_TUN_91_B)
    print(service_L2VC_TUN_5_B)
    print(service_L2VC_TUN_91_B)

    final_somme_general_nbr_service_Internet = somme_general_nbr_service_Internet
    final_somme_general_nbr_service_VOIP = somme_general_nbr_service_VOIP
    final_somme_general_nbr_service_BUSINESS_CLIENT_VSI = (service_BUSINESS_CLIENT_VSI_TUN_5_B)
    final_somme_general_nbr_service_BUSINESS_VSI = (service_BUSINESS_VSI_TUN_5_B)
    final_somme_general_nbr_service_L2vc = (service_L2VC_TUN_5_B) + (service_L2VC_TUN_91_B)
    print("***********")
    print(final_somme_general_nbr_service_Internet)
    print(final_somme_general_nbr_service_VOIP)
    print(final_somme_general_nbr_service_BUSINESS_CLIENT_VSI)
    print(final_somme_general_nbr_service_BUSINESS_VSI)
    print(final_somme_general_nbr_service_L2vc)
    context={'final_somme_general_nbr_service_L2vc':final_somme_general_nbr_service_L2vc,'final_somme_general_nbr_service_BUSINESS_VSI':final_somme_general_nbr_service_BUSINESS_VSI,'final_somme_general_nbr_service_BUSINESS_CLIENT_VSI':final_somme_general_nbr_service_BUSINESS_CLIENT_VSI,'final_somme_general_nbr_service_VOIP':final_somme_general_nbr_service_VOIP,'final_somme_general_nbr_service_Internet':final_somme_general_nbr_service_Internet,'reportingB2B':reportingB2B}
    return render(request, 'liste_routeur/reportingB2B.html', context)
 except:
     return render(request, 'liste_routeur/Erreurchargement.html')
@login_required(login_url='login')
@forCustomer
def changelog(request):
    service_content_history = Service.history.all().order_by('-history_date')
    script_content_history = Script.history.all().order_by('-history_date')

    context = {  'box_content_history': service_content_history ,'script_content_history': script_content_history}


    return render(request, 'liste_routeur/changelog.html', context)



@login_required(login_url='login')
@forCustomer
def genratescript(request):
     
     servicebyuser=Service.objects.filter(user=request.user.username)
     box_content_history = Service.history.all().order_by('-history_date')
     for item in box_content_history:
         print (item)
         print(type(item.history_type))
     servicemanuel=ServiceManuel.objects.filter(user=request.user.username)
     updatebyuser=Script.objects.filter(user=request.user.username)
     deletebyuser=DelService.objects.filter(user=request.user.username)
     L2VCbyuser=L2VC.objects.filter(user=request.user.username)
     context={ 'servicebyuser':servicebyuser,'box_content_history':box_content_history,'servicemanuel':servicemanuel,'updatebyuser':updatebyuser,'deletebyuser':deletebyuser,'L2VCbyuser':L2VCbyuser}

     return render(request, 'liste_routeur/scriptprofile.html',context)





@login_required(login_url='login')
@forCustomer
def delete_script(request, pk):
    try:
            script = Script.objects.get(id=pk)



            if request.method == 'POST' and 'btn':
                script.delete()
                messages.success(request,"Supression Effectuée Avec succées")
                return redirect('genratescript',)

            context = {'script': script}
            return render(request, 'liste_routeur/delete_scriptbyuser.html', context)

    except:
        return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forCustomer
def delete_service(request, pk):
    try:
            service = Service.objects.get(id=pk)

            if request.method == 'POST' and 'btn':
                service.delete()
                messages.success(request, "Supression Effectuée Avec succées")
                return redirect('genratescript', )

            context = {'service': service}
            return render(request, 'liste_routeur/delete_servicebyuser.html', context)

    except:
        return render(request, 'liste_routeur/Erreursupp.html')



@login_required(login_url='login')
@forCustomer
def change_architect_service_NAT(request,pk):

     service=Service.objects.get(id=pk)
     nomClient=service.nomClient
     nomClient = nomClient.replace(" ","_")
     nomClient=nomClient.upper()
     routeur=service.routeur
     VRF=service.VRF
     trans = service.trans

     if VRF == "CCTV" or VRF == "CCTV_Wimax":
         stra = "CCTV"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Internet_vpn":
         stra = "INTERNET"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Boutique_Orange":
         stra = "MPLS"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Voice_vpn":
         stra = "VOICE"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "MonitoringB2B_vpn":
         stra = "MNG_SW"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra






     rt = "####" + str(routeur) + "###"




     monselectarch = request.POST.get("monselectarch")
     rangeaddress = request.POST.get('monselectadd')


     listprive = list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
     listpublic = list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
     listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
     listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
     serviceadressepublic = list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
     serviceadressepublic31 = list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
     serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
     serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
     serviceadresseprive = list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
     listpublic31 = listpublic[0]

     liste31 = list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))



     if monselectarch=="__NA__":
         messages.error(request, 'Merci de selectionner une architecture cible de ce client')
     if  monselectarch=="SANS NAT AVEC CPE":
         if rangeaddress == "__NA__":
             messages.error(request, 'Merci de selectionner  un range @ afin de re-generer votre script')
         if rangeaddress == "/31 Public Address":

             if len(serviceadressepublic31) == 0:
                 nextaddpub31 = liste31[0]
                 print(nextaddpub31)
             else:
                 for L31 in serviceadressepublic31:
                     L31str = "".join(L31)
                     liste31.remove(ipaddress.ip_network(L31str))
                     nextaddpub31 = liste31[0]
                 print("le 1ier @ pub")
                 print(nextaddpub31)
             ancianipadresspublic=service.ipadresspublic

             AdressReseau31= (ipaddress.IPv4Interface(nextaddpub31)).ip
             ancienAdressReseau32= (ipaddress.IPv4Interface(ancianipadresspublic)).ip
             list2 = (list(ipaddress.ip_network(service.ipadress).hosts()))
             adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.252"


             routs1 = "ip route-static vpn-instance " + VRF + " " + format(AdressReseau31) + " 255.255.255.254 " + format(ipaddress.IPv4Address(list2[1])) + " " + desc
             service.ipadresspublic = None
             undostatictr="undo ip route-static vpn-instance " + VRF + " " + format(ancienAdressReseau32) + " 255.255.255.255 " + format(ipaddress.IPv4Address(list2[1]))
             service.generate = rt + '\n' + undostatictr + '\n' + routs1
             service.ipadresspublic31 = nextaddpub31

             service.save()
             messages.success(request, 'Generation de Script est effectuée avec succes')

             return redirect('genratescript', )
         if rangeaddress == "/28 Public Address":
             if len(serviceadressepublic28) == 0:
                 nextaddpub31 = listpuclic28[0]
                 print(nextaddpub31)
             else:
                 for L31 in serviceadressepublic28:
                     L31str = "".join(L31)
                     listpuclic28.remove(ipaddress.ip_network(L31str))
                     nextaddpub31 = listpuclic28[0]
                 print("le 1ier @ pub")
                 print(nextaddpub31)
             ancianipadresspublic = service.ipadresspublic

             AdressReseau31 = (ipaddress.IPv4Interface(nextaddpub31)).ip
             ancienAdressReseau32 = (ipaddress.IPv4Interface(ancianipadresspublic)).ip
             list2 = (list(ipaddress.ip_network(service.ipadress).hosts()))
             adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.252"

             routs1 = "ip route-static vpn-instance " + VRF + " " + format(
                 AdressReseau31) + " 255.255.255.240 " + format(ipaddress.IPv4Address(list2[1])) + " " + desc
             service.ipadresspublic = None
             undostatictr = "undo ip route-static vpn-instance " + VRF + " " + format(
                 ancienAdressReseau32) + " 255.255.255.255 " + format(ipaddress.IPv4Address(list2[1]))
             service.generate = rt + '\n' + undostatictr + '\n' + routs1
             service.ipadresspublic28 = nextaddpub31

             service.save()
             messages.success(request, 'Generation de Script est effectuée avec succes')
             return redirect('genratescript', )
         if rangeaddress == "/29 Public Address":
             if len(serviceadressepublic29) == 0:
                 nextaddpub31 = listpuclic29[0]
                 print(nextaddpub31)
             else:
                 for L31 in serviceadressepublic29:
                     L31str = "".join(L31)
                     listpuclic29.remove(ipaddress.ip_network(L31str))
                     nextaddpub31 = listpuclic29[0]
                 print("le 1ier @ pub")
                 print(nextaddpub31)
             ancianipadresspublic = service.ipadresspublic

             AdressReseau31 = (ipaddress.IPv4Interface(nextaddpub31)).ip
             ancienAdressReseau32 = (ipaddress.IPv4Interface(ancianipadresspublic)).ip
             list2 = (list(ipaddress.ip_network(service.ipadress).hosts()))
             adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.252"

             routs1 = "ip route-static vpn-instance " + VRF + " " + format(
                 AdressReseau31) + " 255.255.255.248 " + format(ipaddress.IPv4Address(list2[1])) + " " + desc
             service.ipadresspublic = None
             undostatictr = "undo ip route-static vpn-instance " + VRF + " " + format(
                 ancienAdressReseau32) + " 255.255.255.255 " + format(ipaddress.IPv4Address(list2[1]))
             service.generate = rt + '\n' + undostatictr + '\n' + routs1
             service.ipadresspublic29 = nextaddpub31


             service.save()
             messages.success(request, 'Changement architecture DONE vers' + monselectarch)
             return redirect('genratescript', )
     if monselectarch == "SANS NAT SANS CPE":
         messages.error(request, 'Service Non supporté')


     return render(request, 'liste_routeur/my_form_service_update_arch.html')


@login_required(login_url='login')
@forCustomer
def change_architect_service_SANS_NAT_AVEC_CPE(request,pk):


     service=Service.objects.get(id=pk)
     nomClient=service.nomClient
     nomClient = nomClient.replace(" ","_")
     nomClient=nomClient.upper()
     routeur=service.routeur
     VRF=service.VRF
     trans = service.trans

     if VRF == "CCTV" or VRF == "CCTV_Wimax":
         stra = "CCTV"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Internet_vpn":
         stra = "INTERNET"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Boutique_Orange":
         stra = "MPLS"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "Voice_vpn":
         stra = "VOICE"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
     if VRF == "MonitoringB2B_vpn":
         stra = "MNG_SW"
         desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra






     rt = "####" + str(routeur) + "###"




     monselectarch = request.POST.get("monselectarch")
     rangeaddress = request.POST.get('monselectadd')


     listprive = list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
     listpublic = list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
     listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
     listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
     serviceadressepublic = list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
     serviceadressepublic31 = list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
     serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
     serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
     serviceadresseprive = list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
     listpublic31 = listpublic[0]

     liste31 = list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




     if rangeaddress == "__NA__":
             messages.error(request, 'Merci de selectionner  un range @ afin de re-generer votre script')

     if rangeaddress == "/28 Public Address":
             if len(serviceadressepublic28) == 0:
                 nextaddpub31 = listpuclic28[0]
                 print(nextaddpub31)
             else:
                 for L31 in serviceadressepublic28:
                     L31str = "".join(L31)
                     listpuclic28.remove(ipaddress.ip_network(L31str))
                     nextaddpub31 = listpuclic28[0]
                 print("le 1ier @ pub")
                 print(nextaddpub31)
             ancianipadresspublic = service.ipadresspublic31

             AdressReseau31 = (ipaddress.IPv4Interface(nextaddpub31)).ip
             ancienAdressReseau32 = (ipaddress.IPv4Interface(ancianipadresspublic)).ip
             list2 = (list(ipaddress.ip_network(service.ipadress).hosts()))
             adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.252"

             routs1 = "ip route-static vpn-instance " + VRF + " " + format(
                 AdressReseau31) + " 255.255.255.240 " + format(ipaddress.IPv4Address(list2[1])) + " " + desc
             service.ipadresspublic31 = None
             undostatictr = "undo ip route-static vpn-instance " + VRF + " " + format(
                 ancienAdressReseau32) + " 255.255.255.254 " + format(ipaddress.IPv4Address(list2[1]))
             service.generate = rt + '\n' + undostatictr + '\n' + routs1
             service.ipadresspublic28 = nextaddpub31

             service.save()
             messages.success(request, 'Generation de Script est effectuée avec succes')
             return redirect('genratescript', )
     if rangeaddress == "/29 Public Address":
             if len(serviceadressepublic29) == 0:
                 nextaddpub31 = listpuclic29[0]
                 print(nextaddpub31)
             else:
                 for L31 in serviceadressepublic29:
                     L31str = "".join(L31)
                     listpuclic29.remove(ipaddress.ip_network(L31str))
                     nextaddpub31 = listpuclic29[0]
                 print("le 1ier @ pub")
                 print(nextaddpub31)
             ancianipadresspublic = service.ipadresspublic31

             AdressReseau31 = (ipaddress.IPv4Interface(nextaddpub31)).ip
             ancienAdressReseau32 = (ipaddress.IPv4Interface(ancianipadresspublic)).ip
             list2 = (list(ipaddress.ip_network(service.ipadress).hosts()))
             adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.252"

             routs1 = "ip route-static vpn-instance " + VRF + " " + format(
                 AdressReseau31) + " 255.255.255.248 " + format(ipaddress.IPv4Address(list2[1])) + " " + desc
             service.ipadresspublic31 = None
             undostatictr = "undo ip route-static vpn-instance " + VRF + " " + format(
                 ancienAdressReseau32) + " 255.255.255.254 " + format(ipaddress.IPv4Address(list2[1]))
             service.generate = rt + '\n' + undostatictr + '\n' + routs1
             service.ipadresspublic29 = nextaddpub31


             service.save()
             messages.success(request, 'Changement architecture DONE vers' + monselectarch)
             return redirect('genratescript', )



     return render(request, 'liste_routeur/my_form_service_update_arch_sans_nat_avec_cpe.html')

@login_required(login_url='login')
@forCustomer
def change_architect_service_SANS_NAT_SANS_CPE(request,pk):
    service = Service.objects.get(id=pk)
    nomClient = service.nomClient
    nomClient = nomClient.replace(" ", "_")
    nomClient = nomClient.upper()
    routeur = service.routeur
    interface=service.interface
    VRF = service.VRF
    trans = service.trans
    vlan=service.vlan

    if VRF == "CCTV" or VRF == "CCTV_Wimax":
        stra = "CCTV"
        desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
    if VRF == "Internet_vpn":
        stra = "INTERNET"
        desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
    if VRF == "Boutique_Orange":
        stra = "MPLS"
        desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
    if VRF == "Voice_vpn":
        stra = "VOICE"
        desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra
    if VRF == "MonitoringB2B_vpn":
        stra = "MNG_SW"
        desc = "description TO_B2B_client_" + nomClient + "_" + trans + "_" + stra

    rt = "####" + str(routeur) + "###"

    monselectarch = request.POST.get("monselectarch")
    rangeaddress = request.POST.get('monselectadd')

    listprive = list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
    listpublic = list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
    listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
    listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
    serviceadressepublic = list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
    serviceadressepublic31 = list(
        Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
    serviceadressepublic28 = list(
        Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
    serviceadressepublic29 = list(
        Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
    serviceadresseprive = list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
    listpublic31 = listpublic[0]

    liste31 = list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))

    if rangeaddress == "__NA__":
        messages.error(request, 'Merci de selectionner  un range @ afin de re-generer votre script')

    if rangeaddress == "/28 Public Address":
        if len(serviceadressepublic28) == 0:
            nextaddpub31 = listpuclic28[0]
            print(nextaddpub31)
        else:
            for L31 in serviceadressepublic28:
                L31str = "".join(L31)
                listpuclic28.remove(ipaddress.ip_network(L31str))
                nextaddpub31 = listpuclic28[0]
            print("le 1ier @ pub")
            print(nextaddpub31)
        ancianipadresspublic = service.ipadresspublic31
        list1= (list(ipaddress.ip_network(ancianipadresspublic).hosts()))
        ancienadresser2 = " undo ip address  " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.254"
        list2 = (list(ipaddress.ip_network(nextaddpub31).hosts()))
        adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.240"

        interface= "interface GigabitEthernet"+"".join(interface).strip()+"."+str(vlan)
        service.ipadresspublic31 = None
        
        service.generate = rt + '\n' + interface + '\n' + ancienadresser2 + '\n' + adresser2
        service.ipadresspublic28 = nextaddpub31

        service.save()
        messages.success(request, 'Generation de Script est effectuée avec succes')
        return redirect('genratescript', )
    if rangeaddress == "/29 Public Address":
        if len(serviceadressepublic29) == 0:
            nextaddpub31 = listpuclic29[0]
            print(nextaddpub31)
        else:
            for L31 in serviceadressepublic29:
                L31str = "".join(L31)
                listpuclic29.remove(ipaddress.ip_network(L31str))
                nextaddpub31 = listpuclic29[0]
            print("le 1ier @ pub")
            print(nextaddpub31)
        ancianipadresspublic = service.ipadresspublic31
        list1 = (list(ipaddress.ip_network(ancianipadresspublic).hosts()))
        ancienadresser2 = " undo ip address  " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.254"

        list2 = (list(ipaddress.ip_network(nextaddpub31).hosts()))
        adresser2 = " ip address " + format(ipaddress.IPv4Address(list2[0])) + " 255.255.255.248"

        interface = "interface GigabitEthernet" + "".join(interface).strip()+"."+str(vlan)
        service.ipadresspublic31 = None

        service.generate = rt + '\n' + interface + '\n' + ancienadresser2 + '\n' + adresser2
        service.ipadresspublic29 = nextaddpub31

        service.save()
        messages.success(request, 'Changement architecture DONE vers ' + monselectarch)
        return redirect('genratescript', )

    return render(request, 'liste_routeur/my_form_service_update_arch_sans_nat_sans_cpe.html')

@login_required(login_url='login')
@forCustomer
def delete_service_manuel(request, pk):
    try:
            servicemanuel = ServiceManuel.objects.get(id=pk)

            if request.method == 'POST' and 'btn':
                servicemanuel.delete()
                messages.success(request, "Supression Effectuée Avec succées")
                return redirect('genratescript', )

            context = {'servicemanuel': servicemanuel}
            return render(request, 'liste_routeur/delete_servicemanuelbyuser.html', context)

    except:
        return render(request, 'liste_routeur/Erreursupp.html')

@login_required(login_url='login')
@forCustomer
def delete_service_resiliation(request, pk):
    try:
            delservice = DelService.objects.get(id=pk)

            if request.method == 'POST' and 'btn':
                delservice.delete()
                messages.success(request, "Supression Effectuée Avec succées")
                return redirect('genratescript', )

            context = {'delservice': delservice}
            return render(request, 'liste_routeur/delete_delservicebyuser.html', context)

    except:
        return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forCustomer
def delete_service_MPLS(request, pk):
    try:
            mpls = L2VC.objects.get(id=pk)

            if request.method == 'POST' and 'btn':
                mpls.delete()
                messages.success(request, "Supression Effectuée Avec succées")

                return redirect('genratescript', )

            context = {'mpls': mpls}
            return render(request, 'liste_routeur/delete_mplsbyuser.html', context)

    except:
        return render(request, 'liste_routeur/Erreursupp.html')


@login_required(login_url='login')
@forCustomer
def infoRouteur(request,pk):

     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     try:
         session = paramiko.SSHClient()
         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')

         stdin, stdout, stderr = session.exec_command("dis clock")

         output = stdout.readlines()
         outout=output[0:]
         session.close() 
         print("*******"+outout[-1])
         vars= str('X3' in outout[-1])
         print(vars)
         if vars=="True":
               commands = ['screen-length 0 temporary \n', 'dis isis peer  \n']
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               connection = session.invoke_shell()
               outputs = []
               result=[]
               while connection.recv_ready():
                         connection.recv(1024)
               for cmd in commands:
                         connection.send(cmd)
                         sleep(1)
                         outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                    
               session.close()
               i = 0
               while i < len(commands):
                         print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                         out = outputs[i].split('\n')
                          
                         for line in out:

                              print(line.rstrip('\n'))
                              result.append(line.rstrip('\n'))
                         i =i+1

   
         else:
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis isis peer | no-more")

               output = stdout.readlines()
               
               sub_l = [i for i in output if int(i.find('Eth'))!=-1 ]
                
         context={'Table':sub_l}

         return render(request, 'liste_routeur/infoRouteur.html',context)
     except:
         return render(request, 'liste_routeur/erreurconnect.html')





@login_required(login_url='login')
@forCustomer
def ConfigR(request,pk):
    NE40=Routeur.objects.filter(id=pk)
    print(type(NE40))
    loop=str(NE40[0])
    loop1=list(loop)
    del loop1[0:10]

    loopr=''.join(loop1)

    looprr=loopr.strip()
    try:
        driver = get_network_driver("ce")
        device = driver(looprr, "ing_onap", "Ingenierie@!23")
        device.open()

        dic=device.get_config(retrieve='all', full=False, sanitized=False)
        Table = []
        for key,value in dic.items():
            temp = []
            temp.extend([key,value])
            Table.append(temp)

        context={'Table':Table}
        return render(request, 'liste_routeur/ConfigR.html',context)
    except:
        return render(request, 'liste_routeur/erreurconnect.html')



@login_required(login_url='login')
@forCustomer
def infoportdown(request,pk):

     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     try:
         session = paramiko.SSHClient()
         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')

         stdin, stdout, stderr = session.exec_command("dis clock")

         output = stdout.readlines()
         outout=output[0:]
         session.close() 
         print("*******"+outout[-1])
         vars= str('X3' in outout[-1])
         print(vars)
         if vars=="True":
               commands = ['screen-length 0 temporary \n', 'dis int desc | i  *down  \n']
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               connection = session.invoke_shell()
               outputs = []
               result=[]
               while connection.recv_ready():
                         connection.recv(1024)
               for cmd in commands:
                         connection.send(cmd)
                         sleep(1)
                         outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                    
               session.close()
               i = 0
               while i < len(commands):
                         print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                         out = outputs[i].split('\n')
                          
                         for line in out:

                              print(line.rstrip('\n'))
                              result.append(line.rstrip('\n'))
                         i =i+1

   
         else:
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis interface desc | i *down  | no-more")

               output = stdout.readlines()
               
               
                
               sub_l = [i for i in output if i.startswith('GE') ]
                
         context={'result':sub_l}

         return render(request, 'liste_routeur/infoportdown.html',context)
     except:
         return render(request, 'liste_routeur/erreurconnect.html')



@login_required(login_url='login')
@forCustomer
def infoportup(request,pk):

     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     try:
         session = paramiko.SSHClient()
         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')

         stdin, stdout, stderr = session.exec_command("dis clock")

         output = stdout.readlines()
         outout=output[0:]
         session.close() 
         print("*******"+outout[-1])
         vars= str('X3' in outout[-1])
         print(vars)
         if vars=="True":
               commands = ['screen-length 0 temporary \n', 'dis int desc | i up  \n']
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               connection = session.invoke_shell()
               outputs = []
               result=[]
               while connection.recv_ready():
                         connection.recv(1024)
               for cmd in commands:
                         connection.send(cmd)
                         sleep(1)
                         outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                    
               session.close()
               i = 0
               while i < len(commands):
                         print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                         out = outputs[i].split('\n')
                          
                         for line in out:

                              print(line.rstrip('\n'))
                              result.append(line.rstrip('\n'))
                         i =i+1

   
         else:
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis interface desc | i up | no-more")

               output = stdout.readlines()
               sub_l = [i for i in output if i.startswith('GE') ]
         context={'result':sub_l}

         return render(request, 'liste_routeur/infoportup.html',context)
     except:
         return render(request, 'liste_routeur/erreurconnect.html')


@login_required(login_url='login')
@forCustomer
def B2B(request,pk):
     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     try:
         session = paramiko.SSHClient()
         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')

         stdin, stdout, stderr = session.exec_command("dis clock")

         output = stdout.readlines()
         outout=output[0:]
         session.close() 
         print("*******"+outout[-1])
         vars= str('X3' in outout[-1])
         print(vars)
         if vars=="True":
               commands = ['screen-length 0 temporary \n', 'dis int desc | i B2B  \n']
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               connection = session.invoke_shell()
               outputs = []
               result=[]
               while connection.recv_ready():
                         connection.recv(1024)
               for cmd in commands:
                         connection.send(cmd)
                         sleep(1)
                         outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                    
               session.close()
               i = 0
               while i < len(commands):
                         print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                         out = outputs[i].split('\n')
                          
                         for line in out:

                              print(line.rstrip('\n'))
                              result.append(line.rstrip('\n'))
                         i =i+1

   
         else:
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis interface desc | i B2B | no-more")

               output = stdout.readlines()
               sub_l = [i for i in output if i.startswith('GE') or i.startswith('Eth') ]
         context={'result':sub_l}
         #NE40=Routeur.objects.all()

         return render(request, 'liste_routeur/B2B.html',context)
     except:
         return render(request, 'liste_routeur/erreurconnect.html')

@login_required(login_url='login')
@forCustomer
@login_required(login_url='login')
@forCustomer
def vueG(request,pk):

     NE40=Routeur.objects.filter(id=pk)
     print(type(NE40))
     loop=str(NE40[0])
     loop1=list(loop)
     del loop1[0:10]

     loopr=''.join(loop1)
     print(loopr)
     looprr=loopr.strip()
     print(looprr)
     try:
         session = paramiko.SSHClient()
         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')

         stdin, stdout, stderr = session.exec_command("dis clock")

         output = stdout.readlines()
         outout=output[0:]
         session.close() 
         print("*******"+outout[-1])
         vars= str('X3' in outout[-1])
         print(vars)
         if vars=="True":
               commands = ['screen-length 0 temporary \n', 'dis   interface brief | i up  \n']
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               connection = session.invoke_shell()
               outputs = []
               result=[]
               while connection.recv_ready():
                         connection.recv(1024)
               for cmd in commands:
                         connection.send(cmd)
                         sleep(1)
                         outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                    
               session.close()
               i = 0
               while i < len(commands):
                         print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                         out = outputs[i].split('\n')
                          
                         for line in out:

                              print(line.rstrip('\n'))
                              result.append(line.rstrip('\n'))
                         i =i+1

   
         else:
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(looprr, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis   interface brief | i up | no-more")

               output = stdout.readlines()
               outout=output[10:]
               result =[]
               for item in outout:

                    print(item.rstrip('\n'))
                    result.append(item.rstrip('\n')) 
         context={'Table':result}

         return render(request, 'liste_routeur/vuegeneral.html',context)
     except:
         return render(request, 'liste_routeur/erreurconnect.html')




@login_required(login_url='login')
@forCustomer
def routeurConfig1(request,pk):
     form=ExecutionForm()
     context = {
            'Title' : 'Exécuter une commande',
            'Header' : 'Exécuter une commande',
            'form' : form,
      }
     try:
          if request.method == 'POST':
               NE40=Routeur.objects.filter(id=pk)
               print(type(NE40))
               loop=str(NE40[0])
               loop1=list(loop)
               del loop1[0:10]

               loopr=''.join(loop1)
               print(loopr)
               looprr=loopr.strip()
               print(looprr)
               routeur = looprr
               script = context['script'] = request.POST['script']
               print(routeur)
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command("dis clock")

               output = stdout.readlines()
               outout=output[0:]
               session.close() 
               print("*******"+outout[-1])
               vars= str('X3' in outout[-1])
               print(vars)
               if vars=="True":
                         print(script)
                         commands = ['screen-length 0 temporary \n', script+'\n']
                         
                         session = paramiko.SSHClient()
                         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                         session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                         connection = session.invoke_shell()
                         outputs = []
                         result=[]
                         while connection.recv_ready():
                                   connection.recv(1024)
                         for cmd in commands:
                                   connection.send(cmd)
                                   sleep(1)
                                   outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
                              
                         session.close()
                         i = 0
                         while i < len(commands):
                                   print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
                                   out = outputs[i].split('\n')
                                   
                                   for line in out:

                                        print(line.rstrip('\n'))
                                        result.append(line.rstrip('\n'))
                                   i =i+1
                         
          
               else:
                         session = paramiko.SSHClient()
                         session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                         session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                         stdin, stdout, stderr = session.exec_command(script+" | no-more")

                         output = stdout.readlines()
                         outout=output[3:]
                         result =[]
                         for item in outout:

                              print(item.rstrip('\n'))
                              result.append(item.rstrip('\n')) 
               context={'result':result}
          return render(request, 'liste_routeur/configt.html',context)
     except:
           return render(request, 'liste_routeur/erreurexecution.html')

@login_required(login_url='login')
@forCustomer
def serviceL2VC(request):
   form=L2VCForm()
    
   context = {
               'Title' : 'Upgrade',
               'Header' : 'Configure B2B',
               'form' : form,
               

          }
   try:
     if request.method == 'POST' and "btn3"  in request.POST  :
                    routeur = context['routeur'] = request.POST['routeur']
                    print(routeur)
                    if routeur=="":
                         messages.error(request, 'Merci de selectionner un Routeur')
                    if routeur!="":    
                          
                         listswrt=list(Switch.objects.filter(routeur=routeur).values_list("namedevice"))      
                                   
                         
                         if len((listswrt))==0:

                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                               
                              
                              session.close()
                              form=L2VCForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }
                         if len((listswrt))!=0:
                              
                              
                              form=L2VCForm(request.POST) 
                              form.routeur="routeur"
                              form.switch=listswrt
                              
                              context = {
                                   'form': form,
                                   
                                   'switch': listswrt,
                              }
                    return render(request, 'liste_routeur/AddserviceL2VC.html',context)  
     if request.method == 'POST' and "btn4"  in request.POST  :
                              switch1 = request.POST.get('monselectSW')  
                              if switch1==None:
                                   messages.error(request, 'Merci de selectionner un SWITCH')
                              else:

                                   routeur = context['routeur'] = request.POST['routeur']
                                   findx=int(switch1.find("("))
                                   findy=int(switch1.find("',)")) 
                                   switch11=switch1[findx+2:findy]
                                   print(switch11)
                                   switchfind=list(Switch.objects.filter(namedevice=switch11).values_list("loopswitch"))
                                   switch=("".join(switchfind[0]))
                                   print(switch)
                                   session = paramiko.SSHClient()
                                   session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                   session.connect(switch, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                    
                                   stdin, stdout, stderr = session.exec_command(" show interfaces terse  | no-more")
                                   outputinetsw = stdout.readlines()
                                   x=int("".join(outputinetsw).find("ge"))
                                   y=int("".join(outputinetsw).find("Loop0")) 
                                   i=("".join(outputinetsw)[x:y])
                                   sub_sw = [i for i in outputinetsw if i.startswith('ge') and int(i.find(".")==-1)]
                                   
                                   
                                   session.close()
                                   form=L2VCForm(request.POST)
                                   
                                   form.routeur="routeur"
                                   #listswrt=list(Switch.objects.filter(routeur=routeur).values_list("loopswitch"))
                                   selctsw=[]
                                   selctsw.append(switch)
								   #form.switch=listswrt
                                   form.interface=sub_sw
                                   context = {
                                        'form': form,
                                        'switch': selctsw,
                                        'interface': sub_sw,
                                        
                                   }
     if request.method == 'POST' and "btn22222"  in request.POST  :
                         
                              routeur = context['routeur'] = request.POST['routeur']
                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                              
                              
                              session.close()
                              form=L2VCForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }
     if request.method == 'POST' and 'btnform2' in request.POST:
            
                                        
                                   routeur = context['routeur'] = request.POST['routeur']
                                    
                                   routeur = context['routeur'] = request.POST['routeur']
                                   
                                   switch1 = request.POST.get('monselectSW')
                                   print(switch1)     
                                   interface = request.POST.get('monselect')
                                   print(interface) 
                                   vlan = context['vlan'] = request.POST['vlan']
                                   description=context['description'] = request.POST['description']
                                   trans=context['trans'] = request.POST['trans']
                                   dist=context['dist'] =  request.POST['dist']
                                
                                   
                                   rt="<"+routeur+">"
                                   desc="description TO_B2B_client_"+description+"_"+trans+"_MPLS"
                                   
                                   stat="statistic enable "
                                   mtu="mtu 4470"
                                   upstream="trust upstream default"
                                   vlantype="vlan-type dot1q "+vlan
                                   mpls="mpls l2vc "+dist+" "+vlan

                                   intern="interface Eth-Trunk22"+"."+vlan

                                   vlantypen="vlan-type dot1q "+vlan
                                   mplsn="mpls l2vc "+routeur+" "+vlan
                                   #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
                                   rtn="<"+dist+">"
            
                                   if routeur=="" and interface==None  and switch1==None     :
                                                   messages.error(request, ' MERCI DE CHOISIR LE SR')
                                   if routeur!="" and interface==None   and switch1==None       :
                                             messages.error(request, ' MERCI DE CHOISIR interface')                    
                                   if routeur!="" and interface==None   and switch1!=None       :
                                             messages.error(request, ' MERCI DE CHOISIR interface') 
                                   if routeur!="" and interface!=None and switch1==None   : 
                                                            
                                                            interface = request.POST.get('monselect')
                                                            
                                                            y=int(interface.find("GE"))
                                                            indice=['down','*down','up']
                                                            for i in indice:
                                                                 z=int(interface.find(i))
                                                                 if z!=-1:

                                                                      interfacece=interface[y+2:z]
                                                                      H=int(interfacece.find("("))         
                                                                      if H!=-1:
                                                                           interfacece=interfacece[:H]
                                                            yetdown=int(interface.find("*down"))
                                                            yetup=int(interface.find("up"))
                                                            descyetdown=" description TO_B2B_client_"+description+"_"+trans
                                                            interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                            undoshutdown=" undo shutdown"
                                                            inter="interface GigabitEthernet"+interfacece.strip()+"."+vlan
                                                            session = paramiko.SSHClient()
                                                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                            session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                            stdin, stdout, stderr = session.exec_command(" dis cu "+inter)
                                                            
                                                            outputinterfacevlan = stdout.readlines()
                                                            session.close()
                                                            serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                            l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                            serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                            form=L2VCForm(request.POST)
                                                            if len(serser)!=0 or len(l2vc1)!=0 or len(serser1)!=0:
                                                                      messages.error(request, 'Ce service est deja ajouté')
                                                            else:
                                                                 if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                      messages.error(request, 'CE VLAN est deja configuré sur cette Interface')  
                                                                 else:          
                                                                      if form.is_valid:
                                                                           serviceL2VC=form.save(commit=False)
                                                                           serviceL2VC.user=request.user.username
                                                                           serviceL2VC.interface=interfacece
                                                                           if yetdown!=-1:
                                                                                serviceL2VC.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mpls+'\n'+rtn+'\n'+intern+'\n'+vlantypen+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mplsn
                                                                           if yetdown==-1 and yetup==-1:
                                                                                serviceL2VC.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mpls+'\n'+rtn+'\n'+intern+'\n'+vlantypen+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mplsn
                                                                           if yetup!=-1:
                                                                                serviceL2VC.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mpls+'\n'+rtn+'\n'+intern+'\n'+vlantypen+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mplsn
                                                                                
                                                                           form.save()     
                                                                           messages.success(request, 'Success')
                                                                           if yetdown!=-1:
                                                                                context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,mtu,desc, stat,upstream,mpls,rtn,intern,vlantypen,mtu,desc,stat,upstream,mplsn]
                                                                           if yetdown==-1 and yetup==-1:
                                                                                context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,mtu,desc, stat,upstream,mpls,rtn,intern,vlantypen,mtu,desc,stat,upstream,mplsn]
                                                                           if yetup!=-1:
                                                                                context ['result'] = [rt,inter,vlantype,mtu,desc, stat,upstream,mpls,rtn,intern,vlantypen,mtu,desc,stat,upstream,mplsn]
                                                                                
                                   
                                   if  switch1!=None and interface!=None and routeur!="": 
                                             interface = request.POST.get('monselect')
                                                   
                                             y=int(interface.find("ge-"))
                                             indice=['down','up']
                                             for i in indice:
                                                       z=int(interface.find(i))
                                                       if z!=-1:

                                                            interfacece=interface[y+3:z]
                                                                    
                                                             
                                              
                                             switch=switch1 
                                              
                                             SWSW=Switch.objects.filter(loopswitch=switch)
                                             result = SWSW.values() 
                                             for res in result :
                                                  
                                                  loopsw="<"+res.get("loopswitch")+">"
                                                  looprt="<"+res.get("routeur_id")+">"
                                             swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                             l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                             sw2=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                             
                                             print(res.get("interfaceswrt")) 
                                             print(interfacece)    
                                             if res.get("interfaceswrt")==interfacece:
                                                  print("================")
                                             vsw="set vlans "+ description + " vlan-id "+vlan 
                                             descsw="set interfaces "+ interfacece +" description "+ description
                                             modesw="set interfaces "+ interfacece +" unit 0 family ethernet-switching port-mode trunk"
                                             vlanmembersw="set interfaces "+ interfacece +" unit 0 family ethernet-switching vlan members "+ description
                                             vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ description
                                             if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                  interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                             else:
                                                  interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan
                                             
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                             outputinterfacertvlan = stdout.readlines()
                                             session.close() 
                                             
                                             form=L2VCForm(request.POST)         
                                             if len(swsw)!=0 or len(l2vcsw1)!=0 or len(sw2)!=0:
                                                  messages.error(request, 'Service deja ajouté')
                                                       
                                                            

                                             else:
                                                  if ("".join(outputinterfacertvlan).find("Error")==-1):
                                                            messages.error(request, 'CE VLAN est deja configuré sur cette Interface')  
                                                  else:
                                                       if form.is_valid:
                                                                      serviceL2VC=form.save(commit=False)
                                                                      serviceL2VC.user=request.user.username 
                                                                      serviceL2VC.switch=switch 
                                                                      serviceL2VC.interfacertsw=("".join(res.get("interfacertsw")))
                                                                      serviceL2VC.interface=interfacece 
                                                                      serviceL2VC.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw+'\n'+vlantype+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mpls+'\n'+rtn+'\n'+intern+'\n'+vlantypen+'\n'+mtu+'\n'+desc+'\n'+stat+'\n'+upstream+'\n'+mplsn
                                                                      form.save()
                                                                           
                                                                      messages.success(request, 'Success')
                                                                      context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,mtu,desc, stat,upstream,mpls,rtn,intern,vlantypen,mtu,desc,stat,upstream,mplsn]
          

     return render(request, 'liste_routeur/AddserviceL2VC.html',context)
   except:
               return render(request, 'liste_routeur/erreurconnect.html')

@login_required(login_url='login')
@forCustomer
def service(request):

 form=ServiceForm()

 context = {
                   'Title' : 'Upgrade',
                   'Header' : 'Configure B2B',
                   'form' : form,


     }

 try:
     if request.method == 'POST' and "btn1"  in request.POST  :
                    routeur = context['routeur'] = request.POST['routeur']
                    print(routeur)
                    if routeur=="":
                         messages.error(request, 'Merci de selectionner un Routeur')
                    if routeur!="":    
                         listswrt=list(Switch.objects.filter(routeur=routeur).values_list("namedevice"))
                         if len((listswrt))==0:

                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                               
                              
                              session.close()
                              form=ServiceForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }
                         if len((listswrt))!=0:
                              
                              
                              form=ServiceForm(request.POST) 
                              form.routeur="routeur"
                              form.switch=listswrt
                              
                              context = {
                                   'form': form,
                                   
                                   'switch': listswrt,
                              }
                    return render(request, 'liste_routeur/Addservice.html',context)  
     if request.method == 'POST' and "btn2"  in request.POST  :
                              switch1 = request.POST.get('monselectSW')  
                              if switch1==None:
                                   messages.error(request, 'Merci de selectionner un SWITCH')
                              else:
                                    
                                   routeur = context['routeur'] = request.POST['routeur']
                                   findx=int(switch1.find("("))
                                   findy=int(switch1.find("',)")) 
                                   switch11=switch1[findx+2:findy]
                                   print(switch11)
                                   switchfind=list(Switch.objects.filter(namedevice=switch11).values_list("loopswitch"))
                                   switch=("".join(switchfind[0]))
                                   print(switch)
                                   session = paramiko.SSHClient()
                                   session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                   session.connect(switch, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                   stdin, stdout, stderr = session.exec_command(" show interfaces terse  | no-more")

                                   outputinetsw = stdout.readlines()
                                   x=int("".join(outputinetsw).find("ge"))
                                   y=int("".join(outputinetsw).find("Loop0")) 
                                   i=("".join(outputinetsw)[x:y])
                                   sub_sw = [i for i in outputinetsw if i.startswith('ge') and int(i.find(".")==-1)]
                                   
                                   
                                   session.close()
                                   form=ServiceForm(request.POST)
                                   
                                   form.routeur="routeur"
                                   #listswrt=list(Switch.objects.filter(routeur=routeur).values_list("loopswitch"))
                                   selctsw=[]
                                   selctsw.append(switch)
                                   #form.switch=listswrt
                                   form.interface=sub_sw
                                   context = {
                                        'form': form,
                                        'switch': selctsw,
                                        'interface': sub_sw,
                                        
                                   }
                                   
     if request.method == 'POST' and "btn22222"  in request.POST  :
                         
                              routeur = context['routeur'] = request.POST['routeur']
                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                              
                              
                              session.close()
                              form=ServiceForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }

     if request.method == 'POST' and 'btnform3'    in request.POST:

                         rangeaddress = request.POST.get('monselectadd')
                         print("rangeaddress")

                         if rangeaddress != "__NA__":
                             messages.error(request, 'Merci de rendre le range Public @ vers __NA__ afin de generer ce script')
                         else:
                             nomClient=context['nomClient'] = request.POST['nomClient']
                             nomClient=nomClient.replace(" ", "_")
                             nomClient=nomClient.upper()
                             routeur = context['routeur'] = request.POST['routeur']
    

                             switch1 = request.POST.get('monselectSW')
                             print(switch1)     
                             interface = request.POST.get('monselect')
                             print(interface) 
                             vlan = context['vlan'] = request.POST['vlan']
                             debit = context['debit'] = request.POST['debit']
                             VRF=context['VRF'] = request.POST['VRF']
    
                              
                              
                             if VRF=="CCTV" or VRF=="CCTV_Wimax":
                                str="CCTV"  
                             if VRF=="Internet_vpn":
                                  str="INTERNET"
                             if VRF=="Boutique_Orange":
                                  str="MPLS"
                             if VRF=="Voice_vpn":
                                  str="VOICE"
                             if VRF=="MonitoringB2B_vpn":
                                  str="MNG_SW"
                                       
                             trans=context['trans'] = request.POST['trans']
                             bd= "shaping"+debit
                             
                             qos=  "qos-profile shaping"+debit
                             qu=   " user-queue cir "+ debit+"000 pir "+debit+"000 outbound  "
                             ququ=   " user-queue cir "+ debit+"000 pir "+debit+"000 inbound  "
    
                             vlantype=" vlan-type dot1q "+vlan
                             Inp=" qos-profile "+ bd + " outbound identifier none"
                             out=" qos-profile "+ bd + " inbound identifier none"
                              
                                               
                        #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
                             rt="<"+routeur+">"
                             if str=="CCTV_W":
                                   
                                  desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_CCTV_WIMAX"
                             else:     
                                  desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_"+str
                             binding=" ip binding vpn-instance "+VRF
                             
                             stat=" statistic enable "
                             upstream=" trust upstream default"
                             
    
                             
                             
                                                      
                              
    
                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             print(serviceadressepublic)
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))
                             print(serviceadresseprive)
                             listpublic31=listpublic[0]
                             listpublic32=listpublic[1]
                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))
                             liste32 =list(ipaddress.ip_network(listpublic32).subnets(new_prefix=32))
    
                                       
                             if len(serviceadressepublic) == 0:
                                            nextaddpub=listpublic32[0]     
                             else:
                                            for L32 in  serviceadressepublic:
                                                      L32str="".join(L32)
                                                      liste32.remove(ipaddress.ip_network(L32str))
                                                      lenpub32=len(liste32)
                                                      
                                                      nextaddpub= liste32[0]
                                            
                                            print("le 1ier @ pub")
                                            print(nextaddpub) 
                                  
                             if len(serviceadresseprive) == 0:
                                            nextaddpr=listprive[0]     
                             else:
                                            for L30 in  serviceadresseprive:
                                                      L30str="".join(L30)
                                                      listprive.remove(ipaddress.ip_network(L30str))
                                                      nextaddpr= listprive[0]
                                            print("le 1ier @ pri")
                                            print(nextaddpr)      
                                       
                                       
                                            
                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')                    
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface') 
                             if routeur!="" and interface!=None and switch1==None   : 
                                                      
                                                      interface = request.POST.get('monselect')
                                                       
                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                       
                                                      
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:
    
                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))         
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]
    
                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"
                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      
                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                       
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)
    
                                                      outputinterfacevlan = stdout.readlines()
                                                         
                                                 
                                                      list1=(list(ipaddress.ip_network(nextaddpub)))  
                                                      list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                      adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                      print(list1[0])
                                                      print(list2[1])
                                                      
                                                      
                                                      routs1="ip route-static vpn-instance "+ VRF+" "+ format(list1[0])+" 255.255.255.255 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                      form=ServiceForm(request.POST)
                                                      
                                                      
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')  
                                                           else:
                                                                
                                                                if form.is_valid:
                                                                     
                                                                     service=form.save(commit=False)
                                                                     
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece 
                                                                     service.ipadress=nextaddpr
                                                                     service.ipadresspublic=nextaddpub
                                                                     
                                                                if debit!="":
                                                                      
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")
    
                                                                     shapingoutput = stdout.readlines()
                                                                     session.close()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:
                                                                       
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]  
                                                                               if yetdown!=-1:
                                                                                     service.generate=rt+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1 
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1 
                                                                               if yetup!=-1:
                                                                                         service.generate=rt+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja Configuré") 
                                                                               if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:           
                                                                                    context ['result'] = [rt,interetdown,descyetdown, undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt,interetdown,descyetdown,   inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                           
    
                                                                               
                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                               vrfout = stdout.readlines()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ] 
                                                                               session.close()
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if  yetup!=-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               form.save()     
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                                
                                                                               if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                                               
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
    
                                                                               if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if  yetup!=-1:           
                                                                                         context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
    
                                                                          
                                                                          
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ] 
                                                                     if yetdown!=-1: 
                                                                          service.generate=rt+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1 
                                                                     if yetdown==-1 and yetup==-1:
                                                                          service.generate=rt+'\n'+'\n'+ interetdown +'\n'+ descyetdown +'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1 
                                                                     if yetup!=-1:
                                                                          service.generate=rt+ '\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1 
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                           
                                                                                
                                                                     if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non COnfiguré")
                                                                     else:
                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetdown==-1 and yetup==-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown, inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetup!=-1:
                                                                           context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                      else:
                                                           messages.error(request, 'Ce Service est deja ajouté ')      
                             if  switch1!=None and interface!=None and routeur!="": 
                                                 interface = request.POST.get('monselect')
                                                       
                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:
    
                                                                interfacece=interface[y+3:z]
                                                                        
                                                                 
                                                  
                                                 switch=switch1 
                                                 
                                                 
                                                 list1=(list(ipaddress.ip_network(nextaddpub)))  
                                                 list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                 adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values() 
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan)) 
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan)) 
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan)) 
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan 
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan
                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 
    
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 session.close()
                                                 routs1="ip route-static vpn-instance "+ VRF+" "+ format(list1[0])+" 255.255.255.255 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')  
                                                      else:
                                                             
                                                           if form.is_valid:
                                                                service=form.save(commit=False)
                                                                service.user=request.user.username 
                                                                service.ipadress=nextaddpr
                                                                service.switch=switch
                                                                service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                service.interface=interfacece
                                                                service.ipadresspublic=nextaddpub
                                                           
                                                                
                                                           if debit!="":
                                                                session = paramiko.SSHClient()
                                                                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")
    
                                                                shapingoutput = stdout.readlines()
                                                                bdfind=bd+" "
                                                                sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                print(sub_l)
                                                                if len(sub_l)!=0:
                                                                  
                                                                          session = paramiko.SSHClient()
                                                                          session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                          session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                          stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                          vrfout = stdout.readlines()
                                                                          session.close()
                                                                          VRFFIND=VRF+" "
                                                                          sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]    
                                                                          service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ '\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                          form.save()
                                                                          messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                          messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                          if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                          else:
                                                                                messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")                
                                                                          context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,  interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                     
                                                                if len(sub_l)==0:
                                                                          session = paramiko.SSHClient()
                                                                          session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                          session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                          stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                          vrfout = stdout.readlines()
                                                                          session.close()
                                                                          VRFFIND=VRF+" "
                                                                          sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ] 
                                                                          service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                          form.save()
                                                                          messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                          messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                          if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                          else:
                                                                               messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")      
                                                                          context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                                                                               
                                                           else :
                                                                session = paramiko.SSHClient()
                                                                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
    
                                                                vrfout = stdout.readlines()
                                                                session.close()
                                                                VRFFIND=VRF+" "
                                                                sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]  
                                                                service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                form.save()
                                                                messages.success(request, 'Generation de Script est effectuée avec succes')
                                                             
                                                                if len(sub_vrf)==0:     
                                                                                    
                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                else:
                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")                
                                                                context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                 else:
                                                           messages.error(request, 'Ce service est deja ajouté')
                                       



     #Bouton SANS NAT avec CPE OTN form4

     if request.method == 'POST' and 'btnform4'    in request.POST:
               
                         
                         nomClient=context['nomClient'] = request.POST['nomClient']
                         nomClient=nomClient.replace(" ", "_")
                         nomClient = nomClient.upper()
                         routeur = context['routeur'] = request.POST['routeur']
                         
                         switch1 = request.POST.get('monselectSW')
                         print(switch1)     
                         interface = request.POST.get('monselect')
                         print(interface) 
                         vlan = context['vlan'] = request.POST['vlan']
                         debit = context['debit'] = request.POST['debit']
                         VRF=context['VRF'] = request.POST['VRF']

                         if VRF=="CCTV" or VRF=="CCTV_Wimax":
                                str="CCTV"  
                         if VRF=="Internet_vpn":
                              str="INTERNET"
                         if VRF=="Boutique_Orange":
                              str="MPLS"
                         if VRF=="Voice_vpn":
                              str="VOICE"
                         if VRF=="MonitoringB2B_vpn":
                              str="MNG_SW"

                         trans=context['trans'] = request.POST['trans']
                         bd= "shaping"+debit
                         
                         qos=  "qos-profile shaping"+debit
                         qu=   " user-queue cir "+ debit+"000 pir "+debit+"000 outbound  "
                         ququ=   " user-queue cir "+ debit+"000 pir "+debit+"000 inbound  "

                         vlantype=" vlan-type dot1q "+vlan
                         Inp=" qos-profile "+ bd + " outbound identifier none"
                         out=" qos-profile "+ bd + " inbound identifier none"
                         
                                           
                    #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
                         rt="<"+routeur+">"
                         if str=="CCTV_W":
                               
                              desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_CCTV_WIMAX"
                         else:     
                              desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_"+str
                         binding=" ip binding vpn-instance "+VRF
                         
                         stat=" statistic enable "
                         upstream=" trust upstream default"

                         rangeaddress = request.POST.get('monselectadd')
                         print(rangeaddress)
                         if rangeaddress=="__NA__":
                             messages.error(request,  'Merci de selectionner  un range @ afin de generer votre script')
                         if rangeaddress == "/31 Public Address":


                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             listpuclic28=list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29=list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic31) == 0:
                                            nextaddpub31=liste31[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic31:
                                                      L31str="".join(L31)
                                                      liste31.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= liste31[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)

                             if len(serviceadresseprive) == 0:
                                           nextaddpr=listprive[0]
                             else:
                                            for L30 in  serviceadresseprive:
                                                      L30str="".join(L30)
                                                      listprive.remove(ipaddress.ip_network(L30str))
                                                      nextaddpr= listprive[0]
                                            print("le 1ier @ pri")
                                            print(nextaddpr)



                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"

                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      print(serser)
                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()

                                                      list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                      list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                      adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                      print(list1[1])
                                                      print(list2[1])


                                                      routs1="ip route-static vpn-instance "+ VRF+" " + format(list1[0]) +" 255.255.255.254 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.ipadress=nextaddpr
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic31=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt,interetdown,descyetdown,undoshutdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt,interetdown,descyetdown,   inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                     context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                   service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     form.save()
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetdown==-1 and yetup==-1:
                                                                               service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetdown==-1 and yetup==-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]

                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')

                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1


                                                 list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                 list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                 adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()

                                                 routs1="ip route-static vpn-instance "+ VRF+" " + format(list1[0]) +" 255.255.255.254 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadress=nextaddpr
                                                                     service.ipadresspublic31=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                         messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')
                         
                         
                         
                         
                         
                         if rangeaddress == "/28 Public Address":


                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             listpuclic28=list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29=list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic28) == 0:
                                            nextaddpub31=listpuclic28[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic28:
                                                      L31str="".join(L31)
                                                      listpuclic28.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= listpuclic28[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)

                             if len(serviceadresseprive) == 0:
                                           nextaddpr=listprive[0]
                             else:
                                            for L30 in  serviceadresseprive:
                                                      L30str="".join(L30)
                                                      listprive.remove(ipaddress.ip_network(L30str))
                                                      nextaddpr= listprive[0]
                                            print("le 1ier @ pri")
                                            print(nextaddpr)



                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"

                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      print(serser)
                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()

                                                      list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                      list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                      AdressReseau28= (ipaddress.IPv4Interface(nextaddpub31)).ip
                                                      print("adresse reseau est ",format(AdressReseau28))

                                                      adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"



                                                      routs1="ip route-static vpn-instance "+ VRF+" " + format(AdressReseau28) +" 255.255.255.240 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.ipadress=nextaddpr
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic28=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt,interetdown,descyetdown,undoshutdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt,interetdown,descyetdown,   inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                     context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                   service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     form.save()
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetdown==-1 and yetup==-1:
                                                                               service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetdown==-1 and yetup==-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]

                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')

                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1


                                                 list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                 list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                 adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 AdressReseau28 = (ipaddress.IPv4Interface(nextaddpub31)).ip
                                                 routs1="ip route-static vpn-instance "+ VRF+" " + format(AdressReseau28) +" 255.255.255.240 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadress=nextaddpr
                                                                     service.ipadresspublic28=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                         messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')


                         if rangeaddress == "/29 Public Address":


                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             listpuclic28=list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29=list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic29) == 0:
                                            nextaddpub31=listpuclic29[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic29:
                                                      L31str="".join(L31)
                                                      listpuclic29.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= listpuclic29[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)

                             if len(serviceadresseprive) == 0:
                                           nextaddpr=listprive[0]
                             else:
                                            for L30 in  serviceadresseprive:
                                                      L30str="".join(L30)
                                                      listprive.remove(ipaddress.ip_network(L30str))
                                                      nextaddpr= listprive[0]
                                            print("le 1ier @ pri")
                                            print(nextaddpr)



                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"

                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      print(serser)
                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()

                                                      list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                      list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                      adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                      print(list1[1])
                                                      print(list2[1])
                                                      AdressReseau29 = (ipaddress.IPv4Interface(nextaddpub31)).ip
                                                      print("adresse reseau est ", format(AdressReseau29))

                                                      routs1="ip route-static vpn-instance "+ VRF+" " + format(AdressReseau29) +" 255.255.255.248 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.ipadress=nextaddpr
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic29=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt,interetdown,descyetdown,undoshutdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt,interetdown,descyetdown,   inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                     context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                   service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     form.save()
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetdown==-1 and yetup==-1:
                                                                               service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetdown==-1 and yetup==-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream,routs1]

                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')

                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1


                                                 list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))
                                                 list2=(list(ipaddress.ip_network(nextaddpr).hosts()) )
                                                 adresser2=" ip address "+format(ipaddress.IPv4Address(list2[0]))+" 255.255.255.252"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 AdressReseau29 = (ipaddress.IPv4Interface(nextaddpub31)).ip
                                                 print("adresse reseau est ", format(AdressReseau29))
                                                 routs1="ip route-static vpn-instance "+ VRF+" " + format(AdressReseau29) +" 255.255.255.248 "+format(ipaddress.IPv4Address(list2[1]))+" "+ desc
                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadress=nextaddpr
                                                                     service.ipadresspublic29=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                         messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]


                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream,routs1]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream,routs1]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')


     if request.method == 'POST' and 'btnform5'    in request.POST:

                         
                         nomClient=context['nomClient'] = request.POST['nomClient']
                         nomClient=nomClient.replace(" ", "_")
                         nomClient = nomClient.upper()
                         routeur = context['routeur'] = request.POST['routeur']
                         
                         switch1 = request.POST.get('monselectSW')
                         print(switch1)     
                         interface = request.POST.get('monselect')
                         print(interface) 
                         vlan = context['vlan'] = request.POST['vlan']
                         debit = context['debit'] = request.POST['debit']
                         VRF=context['VRF'] = request.POST['VRF']

                         if VRF=="CCTV" or VRF=="CCTV_Wimax":
                                str="CCTV"  
                         if VRF=="Internet_vpn":
                              str="INTERNET"
                         if VRF=="Boutique_Orange":
                              str="MPLS"
                         if VRF=="Voice_vpn":
                              str="VOICE"
                         if VRF=="MonitoringB2B_vpn":
                              str="MNG_SW"

                         trans=context['trans'] = request.POST['trans']
                         bd= "shaping"+debit
                         
                         qos=  "qos-profile shaping"+debit
                         qu=   " user-queue cir "+ debit+"000 pir "+debit+"000 outbound  "
                         ququ=   " user-queue cir "+ debit+"000 pir "+debit+"000 inbound "

                         vlantype=" vlan-type dot1q "+vlan
                         Inp=" qos-profile "+ bd + " outbound identifier none"
                         out=" qos-profile "+ bd + " inbound identifier none"
                         
                                           
                    #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
                         rt="<"+routeur+">"
                         if str=="CCTV_W":
                               
                              desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_CCTV_WIMAX"
                         else:     
                              desc=" description TO_B2B_client_"+nomClient+"_"+trans+"_"+str
                         binding=" ip binding vpn-instance "+VRF
                         
                         stat=" statistic enable "
                         upstream=" trust upstream default"

                         rangeaddress = request.POST.get('monselectadd')
                         if rangeaddress=="__NA__":
                             messages.error(request,  'Merci de selectionner  un range @ afin de generer votre script')
                         if rangeaddress == "/31 Public Address":
                             listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             print(serviceadressepublic31)
                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic31) == 0:
                                            nextaddpub31=liste31[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic31:
                                                      L31str="".join(L31)
                                                      liste31.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= liste31[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)





                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')

                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"
                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))

                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()



                                                      list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                      adresser2=" ip address "+format(ipaddress.IPv4Address(list1[0]))+" 255.255.255.254"

                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic31=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+undoshutdown+ '\n'+ '\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+ '\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]

                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+ undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetdown==-1 and yetup==-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetdown==-1 and yetup==-1:
                                                                              context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')
                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1


                                                 list1=(list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                 adresser2=" ip address "+format(ipaddress.IPv4Address(list1[0]))+" 255.255.255.254"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 session.close()

                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadresspublic31=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                          messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]


                                                                     if len(sub_l)==0:
                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                                    if len(sub_vrf)==0:

                                                                                        messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')


                         if rangeaddress == "/28 Public Address":
                             listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             print(serviceadressepublic28)
                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic28) == 0:
                                            nextaddpub31=listpuclic28[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic28:
                                                      L31str="".join(L31)
                                                      listpuclic28.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= listpuclic28[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)





                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')

                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"
                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))

                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()




                                                      list1 = (list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                      adresser2 = " ip address " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.240"


                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic28=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+undoshutdown+ '\n'+ '\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+ '\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]

                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+ undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetdown==-1 and yetup==-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetdown==-1 and yetup==-1:
                                                                              context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')
                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1

                                                 list1 = (list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                 adresser2 = " ip address " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.240"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 session.close()

                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadresspublic28=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                          messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]


                                                                     if len(sub_l)==0:
                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                                    if len(sub_vrf)==0:

                                                                                        messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')

                         
                         if rangeaddress == "/29 Public Address":
                             listpuclic28 = list(ipaddress.ip_network('196.224.81.0/24').subnets(new_prefix=28))
                             listpuclic29 = list(ipaddress.ip_network('196.224.82.0/24').subnets(new_prefix=29))
                             listprive=list(ipaddress.ip_network('10.240.100.0/22').subnets(new_prefix=30))
                             listpublic=list(ipaddress.ip_network('41.224.4.0/23').subnets(new_prefix=24))
                             serviceadressepublic=list(Service.objects.filter(ipadresspublic__isnull=False).values_list('ipadresspublic'))
                             serviceadressepublic31=list(Service.objects.filter(ipadresspublic31__isnull=False).values_list('ipadresspublic31'))
                             serviceadressepublic28 = list(Service.objects.filter(ipadresspublic28__isnull=False).values_list('ipadresspublic28'))
                             serviceadressepublic29 = list(Service.objects.filter(ipadresspublic29__isnull=False).values_list('ipadresspublic29'))
                             serviceadresseprive=list(Service.objects.filter(ipadress__isnull=False).values_list('ipadress'))

                             print(serviceadressepublic31)
                             listpublic31=listpublic[0]

                             liste31 =list(ipaddress.ip_network(listpublic31).subnets(new_prefix=31))




                             if len(serviceadressepublic29) == 0:
                                            nextaddpub31=listpuclic29[0]
                                            print(nextaddpub31)
                             else:
                                            for L31 in  serviceadressepublic29:
                                                      L31str="".join(L31)
                                                      listpuclic29.remove(ipaddress.ip_network(L31str))
                                                      nextaddpub31= listpuclic29[0]
                                            print("le 1ier @ pub")
                                            print(nextaddpub31)





                             if routeur=="" and interface==None  and switch1==None     :
                                                 messages.error(request, ' MERCI DE CHOISIR LE SR')
                             if routeur!="" and interface==None   and switch1==None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')
                             if routeur!="" and interface==None   and switch1!=None       :
                                                 messages.error(request, ' MERCI DE CHOISIR interface')

                             if routeur!="" and interface!=None and switch1==None   :

                                                      interface = request.POST.get('monselect')

                                                      y=int(interface.find("GE"))
                                                      indice=['down','*down','up']
                                                      for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+2:z]
                                                                H=int(interfacece.find("("))
                                                                if H!=-1:
                                                                     interfacece=interfacece[:H]

                                                      yetdown=int(interface.find("*down"))
                                                      yetup=int(interface.find("up"))
                                                      descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
                                                      interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
                                                      undoshutdown=" undo shutdown"
                                                      serser=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
                                                      serser1=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))

                                                      inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
                                                      session = paramiko.SSHClient()
                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                      stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

                                                      outputinterfacevlan = stdout.readlines()

                                                      list1 = (list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                      adresser2 = " ip address " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.248"

                                                      form=ServiceForm(request.POST)
                                                      if len(serser)==0 and len(l2vc1)==0 and len(serser1)==0:
                                                           if ("".join(outputinterfacevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                           else:

                                                                if form.is_valid:

                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.ipadresspublic29=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+undoshutdown+ '\n'+ '\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+ '\n'+interetdown+ '\n'+descyetdown+ '\n'+ '\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+  inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                     context ['result'] = [rt, interetdown, descyetdown,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt,  inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]

                                                                     if len(sub_l)==0:
                                                                               session = paramiko.SSHClient()
                                                                               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                               stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                               vrfout = stdout.readlines()
                                                                               session.close()
                                                                               VRFFIND=VRF+" "
                                                                               sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                               if yetdown!=-1:
                                                                                    service.generate=rt+'\n'+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                               if yetup!=-1:
                                                                                    service.generate=rt+'\n'+qos+'\n'+ququ+'\n'+qu+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream

                                                                               form.save()
                                                                               messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                               messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                               if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                               else:
                                                                                     messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                               if yetdown!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetdown==-1 and yetup==-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                               if yetup!=-1:
                                                                                    context ['result'] = [rt, qos ,ququ,qu,inter,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     if yetdown!=-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+ undoshutdown+'\n'+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetdown==-1 and yetup==-1:
                                                                          service.generate=rt+'\n'+'\n'+interetdown+'\n'+ descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     if yetup!=-1:
                                                                          service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     if yetdown!=-1:
                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetdown==-1 and yetup==-1:
                                                                              context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                                     if yetup!=-1:
                                                                          context ['result'] = [rt,inter,vlantype,desc,binding,adresser2,stat,upstream]
                                                      else:
                                                           messages.error(request, 'Ce service est deja ajouté')
                             if  switch1!=None and interface!=None and routeur!="":
                                                 interface = request.POST.get('monselect')

                                                 y=int(interface.find("ge-"))
                                                 indice=['down','up']
                                                 for i in indice:
                                                           z=int(interface.find(i))
                                                           if z!=-1:

                                                                interfacece=interface[y+3:z]



                                                 switch=switch1

                                                 list1 = (list(ipaddress.ip_network(nextaddpub31).hosts()))

                                                 adresser2 = " ip address " + format(ipaddress.IPv4Address(list1[0])) + " 255.255.255.248"
                                                 SWSW=Switch.objects.filter(loopswitch=switch)
                                                 result = SWSW.values()
                                                 for res in result :
                                                      print(res)
                                                      print(type(res))
                                                 swsw=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 l2vcsw1=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 swsw1=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
                                                 print(res.get("loopswitch"))
                                                 print(res.get("interfaceswrt"))
                                                 print(res.get("routeur_id"))
                                                 print(res.get("interfacertsw"))
                                                 loopsw="<"+res.get("loopswitch")+">"
                                                 looprt="<"+res.get("routeur_id")+">"
                                                 vsw="set vlans "+ nomClient + " vlan-id "+vlan
                                                 descsw="set interfaces "+ interface +" description "+ nomClient
                                                 modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
                                                 vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
                                                 if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                      interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
                                                 else:
                                                      interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan

                                                 session = paramiko.SSHClient()
                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                 stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)
                                                 outputinterfacrtevlan = stdout.readlines()
                                                 session.close()

                                                 form=ServiceForm(request.POST)
                                                 if len(swsw)==0 and len(l2vcsw1)==0 and len(swsw1)==0:
                                                      if ("".join(outputinterfacrtevlan).find("Error")==-1):
                                                                messages.error(request, 'CE VLAN est deja configuré sur cette Interface')
                                                      else:

                                                                if form.is_valid:
                                                                     service=form.save(commit=False)
                                                                     service.user=request.user.username
                                                                     service.interface=interfacece
                                                                     service.switch=switch
                                                                     service.interfacertsw=("".join(res.get("interfacertsw")))
                                                                     service.ipadresspublic29=nextaddpub31

                                                                if debit!="":
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                                     shapingoutput = stdout.readlines()
                                                                     bdfind=bd+" "
                                                                     sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                                     print(sub_l)
                                                                     if len(sub_l)!=0:

                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.INFO,"Le Shaping est deja configuré")
                                                                                    if len(sub_vrf)==0:

                                                                                          messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]


                                                                     if len(sub_l)==0:
                                                                                    session = paramiko.SSHClient()
                                                                                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                    stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                    vrfout = stdout.readlines()
                                                                                    session.close()
                                                                                    VRFFIND=VRF+" "
                                                                                    sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                    service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+ququ +'\n'+qu +'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                                    form.save()
                                                                                    messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                    messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                                    if len(sub_vrf)==0:

                                                                                        messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                    else:
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                    context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,ququ,qu,interfacertsw,vlantype,desc,binding,adresser2,Inp,out,stat,upstream]
                                                                else :
                                                                     session = paramiko.SSHClient()
                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                     vrfout = stdout.readlines()
                                                                     session.close()
                                                                     VRFFIND=VRF+" "
                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                     service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype +'\n'+desc+'\n'+binding+'\n'+adresser2+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                     form.save()
                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')

                                                                     if len(sub_vrf)==0:

                                                                                    messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                     else:
                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                     context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresser2,stat,upstream]
                                                 else:
                                                       messages.error(request, 'Ce service est deja ajouté')
     return render(request, 'liste_routeur/Addservice.html',context)
 except:
     return render(request, 'liste_routeur/erreurconnect.html')

@login_required(login_url='login')
@forCustomer
def addvrf(request):

          form=VRFForm()

          context = {
                 'Title' : 'VRF',
                 'Header' : 'Configure B2B',
                 'form' : form,


           }
          if request.method == 'POST' :
                    form=VRFForm(request.POST)
                    if form.is_valid:
                         form.save()
                         messages.success(request, 'Success')
                    routeur=context['routeur'] =request.POST['routeur']
                    route_distinguisher=context['route_distinguisher'] =request.POST['route_distinguisher']
                    rt="<"+routeur+">"
                    namevrf = request.POST.getlist('vpn')
                    
                    print(namevrf)
                    l4=" ipv4-family"
                    l6="  apply-label per-instance"
                    l88="#"
                    l9="bgp 65100"

                    l11="  preference 170 170 170"
                    l12="  import-route direct"
                    l13="  import-route static "
                    if   'option4' in  namevrf :
                         l1="*******MonitoringB2B_vpn*********"
                         l10=" ipv4-family vpn-instance MonitoringB2B_vpn"
                         l2="ip vpn-instance MonitoringB2B_vpn "
                         l3=" description MonitoringB2B_vpn"
                         l7="  vpn-target 65000:1700 export-extcommunity"
                         l8="  vpn-target 65000:1700 import-extcommunity"
                         l5="  route-distinguisher 65100:93"+route_distinguisher
                         context ['result'] = [rt,l1, l2,l3,l4,l5,l6,l7,l8,l88,l9,l10,l11,l12,l13]
                    if   'option3' in  namevrf:
                         l1c="*******CCTV_Wimax*********"
                         l10c=" ipv4-family vpn-instance CCTV_Wimax"
                         l2c="ip vpn-instance CCTV_Wimax "
                         l3c=" description CCTV_Wimax"
                         l7c="  vpn-target 65000:86004 export-extcommunity"
                         l8c="  vpn-target 65000:86004 import-extcommunity"
                         l5c="  route-distinguisher 65100:86"+route_distinguisher
                         context ['result'] = [rt,l1c, l2c,l3c,l4,l5c,l6,l7c,l8c,l88,l9,l10c,l11,l12,l13]
                    if   'option2' in  namevrf:
                         l1v="*******Voice_vpn*********"
                         l10v=" ipv4-family vpn-instance Voice_vpn"
                         l2v="ip vpn-instance Voice_vpn "
                         l3v=" description Voice_vpn"
                         l7v="  vpn-target 65000:40 export-extcommunity"
                         l8v="  vpn-target 65000:40 import-extcommunity"
                         l5v="  route-distinguisher 65100:29"+route_distinguisher
                         context ['result'] = [rt,l1v, l2v,l3v,l4,l5v,l6,l7v,l8v,l88,l9,l10v,l11,l12,l13]
                    if   'option1' in  namevrf:
                         l1i="*******Internet_vpn*********"
                         l10i=" ipv4-family vpn-instance Internet_vpn"
                         l2i="ip vpn-instance Internet_vpn "
                         l3i=" description Internet_vpn"
                         l7i="  vpn-target 65000:55 65000:58 export-extcommunity"
                         l8i="  vpn-target 65000:55 import-extcommunity"
                         l5i="  route-distinguisher 65100:35"+route_distinguisher
                         context ['result'] = [rt,l1i, l2i,l3i,l4,l5i,l6,l7i,l8i,l88,l9,l10i,l11,l12,l13]
                    if   'option5' in  namevrf:
                         l1="*******MonitoringB2B_vpn*********"
                         l10=" ipv4-family vpn-instance MonitoringB2B_vpn"
                         l2="ip vpn-instance MonitoringB2B_vpn "
                         l3=" description MonitoringB2B_vpn"
                         l7="  vpn-target 65000:1700 export-extcommunity"
                         l8="  vpn-target 65000:1700 import-extcommunity"
                         l5="  route-distinguisher 65100:93"+route_distinguisher
                         l1c="*******CCTV_Wimax*********"
                         l10c=" ipv4-family vpn-instance CCTV_Wimax"
                         l2c="ip vpn-instance CCTV_Wimax "
                         l3c=" description CCTV_Wimax"
                         l7c="  vpn-target 65000:86004 export-extcommunity"
                         l8c="  vpn-target 65000:86004 import-extcommunity"
                         l5c="  route-distinguisher 65100:86"+route_distinguisher
                         l1v="*******Voice_vpn*********"
                         l10v=" ipv4-family vpn-instance Voice_vpn"
                         l2v="ip vpn-instance Voice_vpn "
                         l3v=" description Voice_vpn"
                         l7v="  vpn-target 65000:40 export-extcommunity"
                         l8v="  vpn-target 65000:40 import-extcommunity"
                         l5v="  route-distinguisher 65100:29"+route_distinguisher
                         l1i="*******Internet_vpn*********"
                         l10i=" ipv4-family vpn-instance Internet_vpn"
                         l2i="ip vpn-instance Internet_vpn "
                         l3i=" description Internet_vpn"
                         l7i="  vpn-target 65000:55 65000:58 export-extcommunity"
                         l8i="  vpn-target 65000:55 import-extcommunity"
                         l5i="  route-distinguisher 65100:35"+route_distinguisher
                         
                         context ['result'] = [rt,l1, l2,l3,l4,l5,l6,l7,l8,l88,l9,l10,l11,l12,l13,l1c, l2c,l3c,l4,l5c,l6,l7c,l8c,l88,l9,l10c,l11,l12,l13,l1v, l2v,l3v,l4,l5v,l6,l7v,l8v,l88,l9,l10v,l11,l12,l13,l1i, l2i,l3i,l4,l5i,l6,l7i,l8i,l88,l9,l10i,l11,l12,l13]
                    
          return render(request, 'liste_routeur/AddVRF.html',context)





@login_required(login_url='login')
@forCustomer
def delservice(request):
               
          form=DelServiceForm()

          context = {
                    'Title' : 'Upgrade',
                    'Header' : 'Configure B2B',
                    'form' : form,


          }
          try: 
               if request.method == 'POST' and "btn1"  in request.POST  :
                    routeur = context['routeur'] = request.POST['routeur']
                
                    session = paramiko.SSHClient()
                    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                    stdin, stdout, stderr = session.exec_command(" dis int desc | i B2B |  no-more ")

                    outputinet = stdout.readlines()
                      
                    x=int("".join(outputinet).find("GE"))
                    y=int("".join(outputinet).find("Loop0")) 
                    i=("".join(outputinet)[x:y])
                    sub_l = [i for i in outputinet if i.startswith('GE')]
                    for i in sub_l:
                        
                          print(i.rstrip('\n \r'))
                    
                    session.close()
                    form=ScriptForm(request.POST)
                     
                    form.routeur="routeur"
                    form.interface=sub_l
                    context = {
                         'form': form,
                         'interface': sub_l,
                      }
                    return render(request, 'liste_routeur/delservice.html',context)      
               if request.method == 'POST' and "btn"  in request.POST :
                              
                                   
                                   
                    routeur = context['routeur'] = request.POST['routeur']
                    interface = request.POST.get('monselect')
                    if interface==None :
                         messages.error(request, 'MERCI DE CHOISIR UNE INTERFACE')   
                    else:
                         x=int(interface.find("up up"))
                         
                         y=int(interface.find("GE"))
                         z11=int(interface.find("("))
                         u=int(interface.find("."))
                         v=int(interface.find("down"))
                         print(x)
                         print(y)
                         interfacece=list(interface)
                         vlan=list(interface)
                         if(v!=-1):
                              messages.error(request, 'Interface est DOWN')
                         if v==-1:
                              if (z11==-1):
                                   
                                             interfacece=interfacece[2:x]
                                             vlan=vlan[u:x]
                                             print(vlan) 
                              if(z11!=-1):
                                             interfacece=interfacece[2:z11]
                                             vlan=vlan[u:z11]
                                             
                                             print(vlan) 
                                             print(interfacece)
                              strstr="".join(interfacece)
                              serser=list(DelService.objects.filter(routeur=routeur,interface=strstr))
                              if len(serser)!=0:
                                     messages.error(request, 'SERVICE DEJA TRAITE')   
                              if len(serser)==0:           
                                   rt="<"+routeur+">"
                                   desc= "undo interface GigabitEthernet"+"".join(interfacece)
                                   print(desc)
                                   peer1="<10.51.2.2>"
                                   peer2="<10.51.2.4>"
                                   trunk="undo interface Eth-Trunk22"+"".join(vlan)
                                   print(trunk)
                                   session = paramiko.SSHClient()
                                   session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                   session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                   stdin, stdout, stderr = session.exec_command(" dis cu interface GigabitEthernet"+"".join(interfacece))

                                   output = stdout.readlines()
                                             
                                   print(output)
                                   xxx=int("".join(output).find(".10."))
                                   vvv= int("".join(output).find(".192."))         
                                   x=int("".join(output).find("10."))
                                   y=int("".join(output).find("192."))
                                   l2VC1=int("".join(output).find("l2vc 10.51.1.2"))
                                   l2VC2=int("".join(output).find("l2vc 10.51.1.4"))
                                             
                                             
                                   session.close() 
                                             
                                             
                                   form=DelServiceForm(request.POST)
                                   if x!=-1 and y==-1 and l2VC1==-1 and l2VC2==-1 and xxx==-1 and  vvv==-1 :
                                             
                                                  z=("".join(output)[x:x+30])
                                                  masque=int(z.find("255."))
                                                  listdel=list(z)
                                                  del listdel[masque:]
                                                  print(listdel)
                                                  add=ipaddress.IPv4Address("".join(listdel).strip())  
                                                  print(add)   
                                                  print(masque)
                                                  print(list(z))                                                     
                                                  
                                                  nexthop=(add)+1
                                                  
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command(" dis cu | i "+format(ipaddress.IPv4Address(nexthop)))

                                                  output1 = stdout.readlines()
                                                  nbrstatic=int("".join(output1).count("ip route-static"))
                                                  print("************")
                                                  print(nbrstatic)
                                                  xstatic=int("".join(output1).find("ip route-static"))
                                                  xstatic1=int("".join(output1).rfind("ip route-static"))
                                                  z1=("".join(output1)[xstatic:])
                                                  z2=("".join(output1)[xstatic1:])

                                                  masque1=int(z1.find("description"))
                                                  masque2=int(z2.rfind("description"))
                                                  listdel1=list(z1)
                                                  listdel2=list(z2)
                                                  del listdel1[masque1:]
                                                  del listdel2[masque2:]
                                                  print(listdel1)
                                                  print(listdel2)
                                                  
                                                  if nbrstatic ==0:
                                                       
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username 
                                                            delservice.interface= "".join(interfacece)
                                                            delservice.generate= rt+'\n'+desc
                                                            form.save()
                                                            context ['result'] = [rt,desc]
                                                            messages.success(request, 'Success')    
                                                  if nbrstatic ==2:
                                                       static="undo "+"".join(listdel1).rstrip('\r\n')
                                                       static1="undo "+"".join(listdel2).rstrip('\r\n')
                                                       print(static)
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username 
                                                            delservice.interface= "".join(interfacece) 
                                                            delservice.generate= rt+'\n'+desc+'\n'+static+'\n'+static1
                                                            form.save()
                                                            context ['result'] = [rt,desc,static,static1]
                                                            messages.success(request, 'Success')
                                                  if nbrstatic ==1:
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username 
                                                            delservice.interface= "".join(interfacece)     
                                                             
                                                            static="undo "+"".join(listdel1).rstrip('\r\n')
                                                            delservice.generate= rt+'\n'+desc+'\n'+static 
                                                            form.save()
                                                            context ['result'] = [rt,desc,static]
                                                            messages.success(request, 'Success')
                                                  if nbrstatic ==3:
                                                       messages.error(request, 'Opps , service Indisponible')
                                   if x==-1 and y!=-1 and l2VC1==-1 and l2VC2==-1 and xxx==-1 and  vvv==-1 :

                                             
                                                  z=("".join(output)[y:y+30])
                                                  masque=int(z.find("255."))
                                                  listdel=list(z)
                                                  del listdel[masque:]
                                                  print(listdel)
                                                  add=ipaddress.IPv4Address("".join(listdel).strip())  
                                                  print(add)   
                                                  print(masque)
                                                  print(list(z))                                                     
                                                  
                                                  nexthop=(add)+1
                                                  
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command(" dis cu | i "+format(ipaddress.IPv4Address(nexthop)))

                                                  output1 = stdout.readlines()
                                                  
                                                  nbrstatic=int("".join(output1).count("ip route-static"))
                                                  ystatic=int("".join(output1).find("ip route-static"))
                                                  ystatic1=int("".join(output1).rfind("ip route-static"))
                                                  z1=("".join(output1)[ystatic:])
                                                  z2=("".join(output1)[ystatic1:])
                                                  masque1=int(z1.find("description"))
                                                  masque2=int(z2.rfind("description"))
                                                  listdel1=list(z1)
                                                  listdel2=list(z2)
                                                  del listdel1[masque1:]
                                                  del listdel2[masque2:]
                                                  print(listdel1)
                                                  if nbrstatic ==0:
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username
                                                            delservice.interface= "".join(interfacece)   
                                                            delservice.generate= rt+'\n'+desc  
                                                            form.save()
                                                            context ['result'] = [rt,desc]
                                                            messages.success(request, 'Success')    
                                                  if nbrstatic ==2:
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username 
                                                            delservice.interface= "".join(interfacece)  
                                                             
                                                            static="undo "+"".join(listdel1).rstrip('\r\n')
                                                            static1="undo "+"".join(listdel2).rstrip('\r\n')
                                                            print(static)
                                                            delservice.generate= rt+'\n'+desc+'\n'+static+'\n'+static1
                                                            form.save()
                                                            context ['result'] = [rt,desc,static,static1]
                                                            messages.success(request, 'Success')
                                                  if nbrstatic ==1:
                                                       if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username 
                                                            delservice.interface= "".join(interfacece) 
                                                           
                                                            static="undo "+"".join(listdel1).rstrip('\r\n')
                                                            delservice.generate= rt+'\n'+desc+'\n'+static 
                                                            form.save()
                                                            context ['result'] = [rt,desc,static]
                                                            messages.success(request, 'Success')
                                                  if nbrstatic ==3:
                                                       messages.error(request, 'Opps , service Indisponible')
                                   if x!=-1 and y==-1 and l2VC1!=-1   and l2VC2==-1 and xxx==-1 and  vvv==-1:
                                                  if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username
                                                            delservice.interface= "".join(interfacece)  
                                                            delservice.generate= rt+'\n'+desc+'\n'+peer1+'\n'+trunk
                                                            form.save()
                                                            context ['result'] = [rt,desc,peer1,trunk]
                                                            messages.success(request, 'Success,Service en L2VC') 

                                   if x!=-1 and y==-1 and l2VC1==-1   and l2VC2!=-1 and xxx==-1 and  vvv==-1:
                                                  if form.is_valid:
                                                            delservice=form.save(commit=False)
                                                            delservice.user=request.user.username
                                                            delservice.interface= "".join(interfacece) 
                                                            delservice.generate= rt+'\n'+desc+'\n'+peer2+'\n'+trunk 
                                                            form.save()
                                                            
                                                            context ['result'] = [rt,desc,peer2,trunk]
                                                            messages.success(request, 'Success,Service en L2VC')
                                   if x!=-1 and y==-1 and l2VC1==-1   and l2VC2==-1 and xxx!=-1 and  vvv==-1:
                                                  delservice=form.save(commit=False)
                                                  delservice.user=request.user.username
                                                  delservice.interface= "".join(interfacece)  
                                                  delservice.generate= rt+'\n'+desc  
                                                  form.save()
                                                  context ['result'] = [rt,desc]
                                                  messages.success(request, 'Success')   
                                   if x==-1 and y!=-1 and l2VC1==-1   and l2VC2==-1 and xxx==-1 and  vvv!=-1:
                                                  delservice=form.save(commit=False)
                                                  delservice.user=request.user.username
                                                  delservice.interface= "".join(interfacece)  
                                                  delservice.generate= rt+'\n'+desc  
                                                  form.save()
                                                  context ['result'] = [rt,desc]
                                                  messages.success(request, 'Success')

                                   if x==-1 and y==-1 and l2VC1==-1   and l2VC2==-1 and xxx==-1 and  vvv==-1:
                                             yinterface=int("".join(output).find("Error"))
                                             if yinterface!=-1:
                                                  messages.error(request, 'Opps , Interface Non configurée')
                                             if yinterface==-1:     
                                                  delservice=form.save(commit=False)
                                                  delservice.user=request.user.username
                                                  delservice.interface= "".join(interfacece)  
                                                  delservice.generate= rt+'\n'+desc  
                                                  form.save()
                                                  context ['result'] = [rt,desc]
                                                  messages.success(request, 'Success')   
                              
                                        

               return render(request, 'liste_routeur/delservice.html',context)
          except:
                return render(request, 'liste_routeur/erreurconnect.html') 

@login_required(login_url='login')
@forAdmins
def createswitch(request):
  
     form=SwitchForm()
     if request.method=='POST':
            #print(request.POST)
          form=SwitchForm(request.POST)
          if form.is_valid:
               form.save()
               return render(request, 'liste_routeur/Succesaddsw.html')

     context={'form1':form}
     return render(request, 'liste_routeur/my_form_SW.html',context)
 


@login_required(login_url='login')
@forAdmins
def deleteswitch(request,pk):
  try:
     switch=Switch.objects.get(id=pk)
     if request.method=='POST':
          switch.delete()
          return redirect('/')
     context={'switch':switch}
     return render(request, 'liste_routeur/delete_switch.html',context)
  except:
     return render(request, 'liste_routeur/Erreursupp.html')



@login_required(login_url='login')
@forAdmins
def updateswitch(request,pk):

     switch=Switch.objects.get(id=pk)
     print(routeur)
     form=SwitchForm(instance=switch)
     if request.method=='POST':
          form=SwitchForm(request.POST, instance=switch)
          if form.is_valid():
               form.save()
               return redirect('/')
     context={'form1':form}
     return render(request, 'liste_routeur/my_form_SW.html',context)




@login_required(login_url='login')
@forFront
def front(request):
     form=FrontForm()
     context = {
               'Title' : 'Upgrade',
               'Header' : 'Configure B2B',
               'form' : form,
     }
     DEVICE_LIST =['10.51.2.' + str(n) for n in range(2,3)]
     for RTR in DEVICE_LIST:
          try:     
               if request.method == 'POST' and "btn1"  in request.POST  :
                         
                         
                         nom_client = context['nom_client'] = request.POST['nom_client']

                         if RTR=="10.51.2.205" or RTR=="10.51.2.103" or RTR=="10.51.2.60" or RTR=="10.51.2.57" or RTR=="10.51.2.58" or RTR=="10.51.2.66" or RTR=="10.51.2.68" or RTR=="10.51.2.71" or RTR=="10.51.2.33":
                              DEVICE_LIST.index(RTR)+1
                         else:

          
                              
                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(RTR, port=22, username= 'ing_onap', password='Ingenierie@!23', look_for_keys=False, allow_agent=False)
                              
                              stdin, stdout, stderr = session.exec_command("dis int desc | i "+ nom_client)
                              output= []
                              FN=[]
                              output = stdout.readlines()
                              session.close()
                              sub_l = [i for i in output if i.startswith('GE') or  i.startswith('Eth') ]
                                        
                                       
                              form=FrontForm(request.POST)
                                        
                              form.nom_client="nom_client"
                              form.List_client=sub_l
                              context = {
                                             'form': form,
                                             'List_client': sub_l,
                                        }
                                        
                         
               return render(request, 'liste_routeur/front.html',context)
          except:
               return render(request, 'liste_routeur/erreurconnect.html')   



@login_required(login_url='login')
@forCustomer
def dimmensionnement(request):
     dimens=Dimens.objects.all() 
     
     dimen=list(Dimens.objects.filter().values_list('liaison','percent'))
     
     time=[]
     percent=[]
     target=[]
     target90 =[]
     for courbe in list(dimen):
          if(courbe[1]>70):
               time.append(courbe[0])
               percent.append(courbe[1])
               target.append(90)


     context={'dimens':dimens ,
          'labels':time,
          'data':percent,
            'target' : target,

              }

     return render(request, 'liste_routeur/dimens.html',context)

@login_required(login_url='login')
@forCustomer
def dimmensionnementBH(request):
      
     bhs=Bh_sharing.objects.all()   
    
   
     bh=list(Bh_sharing.objects.filter().values_list('liaison','percent')) 
     bh2=list(Bh_sharing.objects.filter().values_list('percent','typeBH','capa')) 
     sumOOO=[]
     sumTT=[]
     sumcapOOO=[]
     sumcapTT=[]
     time1=[]
     percent1=[]
     target = []
     for i in bh2:
          if i[1]=="BH_TT":
               
               serch =i[2].find("G")
               valcap=float(i[2][:serch])  
               print(valcap)   
               valtrafic=i[0]*valcap/100
               sumTT.append(valtrafic)
               sumcapTT.append(valcap)
          if i[1]=="BH_OOO":
               serch =i[2].find("G")
               valcap=float(i[2][:serch])  
               print(valcap)   
               valtrafic=i[0]*valcap/100
               sumOOO.append(valtrafic)   
               sumcapOOO.append(valcap) 

     print(sum(sumTT))
     print(sum(sumcapTT))
     print(sum(sumOOO))   
     print(sum(sumcapOOO))  
     for courbe1 in list(bh):
          if(courbe1[1]>60):
               time1.append(courbe1[0])
               percent1.append(courbe1[1])
               target.append(90)
 

     context={ 'bhs':bhs, 
           
          'labels1':time1,
          'data1':percent1,
          'sumTT':sum(sumTT),
          'sumOOO':sum(sumOOO),
          'sumcapOOO':sum(sumcapOOO),
          'sumcapTT':sum(sumcapTT),
                              'target': target,
              }

     return render(request, 'liste_routeur/dimensBH.html',context)
 

@login_required(login_url='login')
@forCustomer
def dimmensionnementFN(request):
 
     fns=FN.objects.all()  
     fn=list(FN.objects.filter().values_list('description','percent'))

     target = []
     time2=[]
     percent2=[]
       
  
     for courbe2 in list(fn):
          if(courbe2[1]>60):
               time2.append(courbe2[0])
               percent2.append(courbe2[1])
               target.append(90)

     context={ 'fns':fns,

               'target': target,
          'labels2':time2,
          'data2':percent2,
              }

     return render(request, 'liste_routeur/dimensFN.html',context)

@login_required(login_url='login')
@forCustomer
def generatescript(request,pk):

     d=L2VC.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response


@login_required(login_url='login')
@forCustomer
def generatescriptmanuel(request,pk):

     d=ServiceManuel.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response



@login_required(login_url='login')
@forCustomer
def generatenewscript(request,pk):

     d=Service.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response

@login_required(login_url='login')
@forCustomer
def generatedelscript(request,pk):

     d=DelService.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response

@login_required(login_url='login')
@forCustomer
def generateupscript(request,pk):

     d=Script.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response







#pour visiteur 

@login_required(login_url='login')
@forVisiteur
def generatescript1(request,pk):

     d=L2VC.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response

@login_required(login_url='login')
@forVisiteur
def generatenewscript1(request,pk):

     d=Service.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response

@login_required(login_url='login')
@forVisiteur
def generatedelscript1(request,pk):

     d=DelService.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response

@login_required(login_url='login')
@forVisiteur
def generateupscript1(request,pk):

     d=Script.objects.get(id=pk)
     file_name = 'script.txt'
     lines = []
     generate=d.generate
	 
     
     lines.append('{0}'.format(generate))
            
     response_content = '\n'.join(lines)
     response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
     response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
     return response




@login_required(login_url='login')
@forCustomer
def dimmensionnementsw(request):
 
     sws=Switch.objects.all()  
     sw=list(Switch.objects.filter().values_list('namedevice','percent'))
      
     
     time2=[]
     percent2=[]
     target = []
  
     for courbe2 in list(sw):
          if(courbe2[1]>50):
               time2.append(courbe2[0])
               percent2.append(courbe2[1])
               target.append(90)

     context={ 'fns':sws,

               'target': target,
          'labels2':time2,
          'data2':percent2,
              }

     return render(request, 'liste_routeur/dimenssw.html',context)


@login_required(login_url='login')
@forCustomer
def dimmensionnementMECP(request):
 
     NE40=Routeur.objects.all()  
     NE401=list(Routeur.objects.filter().values_list('name','percentmemory','percentcpu'))
     target1 = []
     target2 = []



     time2=[]
     percent2=[]
     time1=[]
     percent1=[] 
  
     for courbe2 in list(NE401):
          if(courbe2[1]>65):
               time2.append(courbe2[0])
               percent2.append(courbe2[1])
               target2.append(90)
          if(courbe2[2]>65):
               time1.append(courbe2[0])
               percent1.append(courbe2[2])
               target1.append(90)
     context={ 'NE40':NE40,
               'target1': target1,
               'target2': target2,

          'labels2':time2,
          'data2':percent2,
          'labels1':time1,
          'data1':percent1,

              }

     return render(request, 'liste_routeur/cpumemory.html',context)

@login_required(login_url='login')
@forCustomer
def servicemanuel(request):
 form=ServiceManuelForm()
 
 context = {
        'Title' : 'Upgrade',
        'Header' : 'Configure B2B',
        'form' : form,
       

  }
 
 
 try:
     if request.method == 'POST' and "btn1"  in request.POST  :
                    routeur = context['routeur'] = request.POST['routeur']
                    print(routeur)
                    if routeur=="":
                         messages.error(request, 'Merci de selectionner un Routeur')
                    if routeur!="":    
                         listswrt=list(Switch.objects.filter(routeur=routeur).values_list("namedevice"))
                         if len((listswrt))==0:

                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                               
                              
                              session.close()
                              form=ServiceManuelForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }
                         if len((listswrt))!=0:
                              
                              
                              form=ServiceManuelForm(request.POST) 
                              form.routeur="routeur"
                              form.switch=listswrt
                              
                              context = {
                                   'form': form,
                                   
                                   'switch': listswrt,
                              }
                    return render(request, 'liste_routeur/Addservicemanuel.html',context)  
     if request.method == 'POST' and "btn2"  in request.POST  :
                              switch1 = request.POST.get('monselectSW')  
                              if switch1==None:
                                   messages.error(request, 'Merci de selectionner un SWITCH')
                              else:
                                    
                                   routeur = context['routeur'] = request.POST['routeur']
                                   findx=int(switch1.find("("))
                                   findy=int(switch1.find("',)")) 
                                   switch11=switch1[findx+2:findy]
                                   print(switch11)
                                   switchfind=list(Switch.objects.filter(namedevice=switch11).values_list("loopswitch"))
                                   switch=("".join(switchfind[0]))
                                   print(switch)
                                   session = paramiko.SSHClient()
                                   session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                   session.connect(switch, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                   stdin, stdout, stderr = session.exec_command(" show interfaces terse  | no-more")

                                   outputinetsw = stdout.readlines()
                                   x=int("".join(outputinetsw).find("ge"))
                                   y=int("".join(outputinetsw).find("Loop0")) 
                                   i=("".join(outputinetsw)[x:y])
                                   sub_sw = [i for i in outputinetsw if i.startswith('ge') and int(i.find(".")==-1)]
                                   
                                   
                                   session.close()
                                   form=ServiceManuelForm(request.POST)
                                   
                                   form.routeur="routeur"
                                   #listswrt=list(Switch.objects.filter(routeur=routeur).values_list("loopswitch"))
                                   selctsw=[]
                                   selctsw.append(switch)
                                   #form.switch=listswrt
                                   form.interface=sub_sw
                                   context = {
                                        'form': form,
                                        'switch': selctsw,
                                        'interface': sub_sw,
                                        
                                   }
                                   
     if request.method == 'POST' and "btn22222"  in request.POST  :
                         
                              routeur = context['routeur'] = request.POST['routeur']
                              session = paramiko.SSHClient()
                              session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                              session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                              stdin, stdout, stderr = session.exec_command(" dis int desc |  no-more ")

                              outputinet = stdout.readlines()
                              
                              x=int("".join(outputinet).find("GE"))
                              y=int("".join(outputinet).find("Loop0")) 
                              i=("".join(outputinet)[x:y])
                              sub_l = [i for i in outputinet if i.startswith('GE') and int(i.find(".")==-1)]
                              
                              
                              session.close()
                              form=ServiceManuelForm(request.POST)
                              
                              form.routeur="routeur"
                              form.interface=sub_l
                              context = {
                                   'form': form,
                                   'interface': sub_l,
                              }

     if request.method == 'POST' and 'btnform1'    in request.POST:
          

           print("ok")
           ipGW=context['ipGW'] =request.POST['ipGW']
           ipmasque=context['ipmasque'] =request.POST['ipmasque']
           switch1 = request.POST.get('monselectSW')
           print(switch1)     
           interface = request.POST.get('monselect')
           print(interface) 
           print( (ipGW)) 
           nomClient=context['nomClient'] = request.POST['nomClient']
           nomClient=nomClient.replace(" ", "_")
           nomClient = nomClient.upper()
           routeur = context['routeur'] = request.POST['routeur']
            
           
           vlan = context['vlan'] = request.POST['vlan']
           debit = context['debit'] = request.POST['debit']
           VRF=context['VRF'] = request.POST['VRF']
               
           if VRF=="CCTV" or VRF=="CCTV_Wimax":
                            str="CCTV"  
           if VRF=="Internet_vpn":
                             str="INTERNET"
           if VRF=="Boutique_Orange":
                              str="MPLS"
           if VRF=="Voice_vpn":
                              str="VOICE"
           if VRF=="MonitoringB2B_vpn":
                              str="MNG_SW"
           if VRF=="Voice_Avaya_Client":
                              str="Voice_Avaya"                  
           trans=context['trans'] = request.POST['trans']
           bd= "shaping"+debit
            
           qos=  "# qos-profile shaping"+debit
           qu=   "user-queue cir "+ debit+"000 pir "+debit+"000 outbound  "
           ququ="user-queue cir "+ debit+"000 pir "+debit+"000 inbound  " 
            
               
                
                
                  
           vlantype="vlan-type dot1q "+vlan
           Inp="qos-profile "+ bd + " outbound identifier none"
           out="qos-profile "+ bd + " inbound identifier none"

           #print("set interfaces '{% interface %} 'unit 702 family inet policer input Bandwidth30M")
           rt="<"+routeur+">"
           if str=="CCTV_W":
                               
                              desc="description TO_B2B_client_"+nomClient+"_"+trans+"_CCTV_WIMAX"
           else:     
                              desc="description TO_B2B_client_"+nomClient+"_"+trans+"_"+str
            
           binding="ip binding vpn-instance "+VRF
           adresse="ip address "+ipGW+" "+ipmasque
           stat="statistic enable "
           upstream="trust upstream default"
           route1 = request.POST.getlist('title[]')
           print(len(route1))


           
           if routeur=="" and interface==None  and switch1==None     :
                                             messages.error(request, ' MERCI DE CHOISIR LE SR')
           if routeur!="" and interface==None   and switch1==None       :
                                             messages.error(request, ' MERCI DE CHOISIR interface')                    
           if routeur!="" and interface==None   and switch1!=None       :
                                             messages.error(request, ' MERCI DE CHOISIR interface') 
           if routeur!="" and interface!=None and switch1==None   : 
                                                  
               interface = request.POST.get('monselect')
                                                   
               y=int(interface.find("GE"))
               indice=['down','*down','up']
               for i in indice:
                    z=int(interface.find(i))
                    if z!=-1:
                         interfacece=interface[y+2:z]
                         H=int(interfacece.find("("))         
                         if H!=-1:
                              interfacece=interfacece[:H]
               yetdown=int(interface.find("*down"))
               yetup=int(interface.find("up"))
               descyetdown=" description TO_B2B_client_"+nomClient+"_"+trans
               interetdown= "interface GigabitEthernet"+"".join(interfacece).strip()
               undoshutdown=" undo shutdown"          
               serser=list(ServiceManuel.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))                         
               serser1=list(Service.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
               l2vc1=list(L2VC.objects.filter(routeur=routeur,interface=interfacece,vlan=vlan,switch=None))
               inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command(" dis cu "+inter)

               outputinterfacevlan = stdout.readlines()
               session.close()
               if len(serser)!=0 or len(serser1)!=0 or len(l2vc1)!=0:
                     messages.error(request, 'Service deja traité')
               else:
                    if("".join(outputinterfacevlan).find("Error"))==-1:
                          messages.error(request, 'VLAN deja configuré sur cette Interface')  
                    else:
                         try:
                              ipaddress.ip_address(ipGW)
                              ipaddress.ip_address(ipmasque)
                               
                                    
                              
                          
                              if len(route1)==0 :
                                             
															

															 
                                             form=ServiceManuelForm(request.POST)
                                             if form.is_valid:
                                                  service=form.save(commit=False)
                                                  service.user=request.user.username
                                                  service.interface=interfacece
                                        
                                             if debit!="":
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                  shapingoutput = stdout.readlines()
                                                  
                                                  bdfind=bd+" "
                                                  sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                  print(sub_l)
                                                  if len(sub_l)!=0:
                                                    
                                                                 session = paramiko.SSHClient()
                                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                 stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                 vrfout = stdout.readlines()
                                                                 session.close()
                                                                 VRFFIND=VRF+" "
                                                                 sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                 if yetdown!=-1:
                                                                      service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                 if yetdown==-1 and yetup==-1:
                                                                      service.generate=rt+'\n'+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                 if yetup!=-1:
                                                                       service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                 form.save()
                                                                 messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                 messages.add_message(request,messages.INFO,"Le Shaping est deja Configuré")
                                                                   
                                                                 if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                 
                                                                 else: 
                                                                      messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                                 if yetdown!=-1:
                                                                      context ['result'] = [rt,interetdown,descyetdown,undoshutdown,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                                 if yetdown==-1 and yetup==-1:
                                                                           context ['result'] = [rt,  interetdown,descyetdown, inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                                 if yetup!=-1:
                                                                      context ['result'] = [rt,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                       
                                                  if len(sub_l)==0:
                                                            session = paramiko.SSHClient()
                                                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                            session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                            stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                            vrfout = stdout.readlines()
                                                            session.close()
                                                            VRFFIND=VRF+" "
                                                            sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                            if yetdown!=-1:
                                                                 service.generate=rt+'\n'+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                            if yetdown==-1 and yetup==-1:
                                                                 service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                            if yetup!=-1:     
                                                                 service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                            form.save()
                                                            messages.success(request, 'Generation de Script est effectuée avec succes')
                                                            messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                            if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                            
                                                            else: 
                                                                      messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                            if yetdown!=-1:
                                                                 context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                            if yetdown==-1 and yetup==-1:
                                                                 context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                            if yetup!=-1:          
                                                                  context ['result'] = [rt, qos ,qu,ququ,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                             else :
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                  vrfout = stdout.readlines()
                                                  session.close()
                                                  VRFFIND=VRF+" "
                                                  sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                  if yetdown!=-1:
                                                       service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream
                                                  if yetdown==-1 and yetup==-1:
                                                            service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream
                                                  if yetup!=-1:             
                                                        service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream
                                                  form.save()
                                                  messages.success(request, 'Generation de Script est effectuée avec succes')
                                         
                                                  if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                  else: 
                                                                      messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                  if yetdown!=-1:
                                                       context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,stat,upstream]
                                                  if yetdown==-1 and yetup==-1:
                                                            context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,stat,upstream]
                                                  if yetup!=-1: 
                                                        context ['result'] = [rt,inter,vlantype,desc,binding,adresse,stat,upstream]
                              elif len(route1)==1 or len(route1)==2:    
                                        messages.error(request, 'Erreur Static-Route') 

                              elif len(route1)==3 and route1[0]!='' and  route1[1]!='' and route1[2]!='':
                                   try:
                                        ipaddress.ip_address(route1[0])
                                        ipaddress.ip_address(route1[1])
                                        ipaddress.ip_address(route1[2])
                                        routs1="ip route-static vpn-instance "+ VRF+" "+ route1[0]+" "+ route1[1]+" "+route1[2]+" "+ desc
                                        print (routs1) 
                                        form=ServiceManuelForm(request.POST)
                                        if form.is_valid:
                                              
															
 
                                             service=form.save(commit=False)
                                             service.user=request.user.username
                                             service.interface=interfacece
                                             service.dist=route1[0]
                                             service.ipmasquedis=route1[1]
                                             service.nexthopedis=route1[2] 
                                        
                                        if debit!="":
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                             shapingoutput = stdout.readlines()
                                             bdfind=bd+" "
                                             sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                             print(sub_l)
                                          
                                             if len(sub_l)!=0:
                                               
                                                                                     session = paramiko.SSHClient()
                                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                     vrfout = stdout.readlines()
                                                                                     session.close()
                                                                                     VRFFIND=VRF+" "
                                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                     if yetdown!=-1:
                                                                                          service.generate=rt+'\n'+interetdown+'\n'+ descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                     if yetdown==-1 and yetup==-1:
                                                                                          service.generate=rt+'\n'+interetdown+'\n'+ descyetdown+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                     if yetup!=-1:
                                                                                          service.generate=rt+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                     
                                                                                     form.save()
                                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                     messages.add_message(request,messages.INFO,"Le  Shaping est deja configuré")
                                                                                     if len(sub_vrf)==0:     
                                                                                
                                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                     else: 
                                                                                           messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                                                     if yetdown!=-1:
                                                                                          context ['result'] = [rt,interetdown,descyetdown,undoshutdown,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                                                                     if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt, interetdown,descyetdown, inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                                                                     if yetup!=-1:
                                                                                          context ['result'] = [rt,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]     
                                             if len(sub_l)==0:
                                                                                     
                                                                                     session = paramiko.SSHClient()
                                                                                     session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                                     session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                                     stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                                     vrfout = stdout.readlines()
                                                                                     session.close()
                                                                                     VRFFIND=VRF+" "
                                                                                     sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                                     if yetdown!=-1:
                                                                                          service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                     if yetdown==-1 and yetup==-1:
                                                                                          service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                     if yetup!=-1:
                                                                                          service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                                          
                                                                                     form.save()
                                                                                     messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                                     messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                                     if len(sub_vrf)==0:     
                                                                                
                                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                                     else: 
                                                                                          messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                                     if yetdown!=-1:
                                                                                          context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                                                                     if yetdown==-1 and yetup==-1:
                                                                                          context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                                                                     if yetup!=-1:
                                                                                          context ['result'] = [rt, qos ,qu,ququ,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                                                                          
                                        else: 
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                             vrfout = stdout.readlines()
                                             session.close()
                                             VRFFIND=VRF+" "
                                             sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                             if yetdown!=-1:
                                                  service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1
                                             if yetdown==-1 and yetup==-1:
                                                  service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1
                                             if yetup!=-1:
                                                  service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                  
                                             form.save()
                                             messages.success(request, 'Generation de Script est effectuée avec succes')
  
                                             if len(sub_vrf)==0:     
                                                                                
                                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                             else:
                                                  messages.add_message(request,messages.INFO,"Le VRF est deja Configuré") 
                                             if yetdown!=-1:
                                                  context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,stat,upstream,routs1]
                                             if yetdown==-1 and yetup==-1:
                                                  context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,stat,upstream,routs1]
                                             if yetup!=-1:
                                                  context ['result'] = [rt,inter,vlantype,desc,binding,adresse,stat,upstream,routs1]
                                   except ValueError:
                                         messages.error(request, '@ NON VALIDE')
                              elif  len(route1)==3 and route1[0]=='' or  route1[1]=='' or route1[2]=='':
                                   messages.error(request, ' Erreur Static-Route')

                              elif  len(route1)==6 and route1[0]!='' and  route1[1]!='' and route1[2]!='' and route1[3]!='' and route1[4]!='' and route1[5]!='':
                             
                                   try:
                                        ipaddress.ip_address(route1[0])
                                        ipaddress.ip_address(route1[1])
                                        ipaddress.ip_address(route1[2])
                                        ipaddress.ip_address(route1[3])
                                        ipaddress.ip_address(route1[4])
                                        ipaddress.ip_address(route1[5])
                                        routs1="ip route-static vpn-instance "+ VRF+" "+ route1[0]+" "+ route1[1]+" "+route1[2]+" "+ desc
                                        routs2="ip route-static vpn-instance "+ VRF+" "+ route1[3]+" "+ route1[4]+" "+route1[5]+" "+ desc   
                                        form=ServiceManuelForm(request.POST)
                                        if form.is_valid:
                                                  
                                                  service=form.save(commit=False)
                                                  service.user=request.user.username
                                                  service.interface=interfacece
                                                  service.dist=route1[0]
                                                  service.ipmasquedis=route1[1]
                                                  service.nexthopedis=route1[2]
                                                  service.dist1=route1[3]
                                                  service.ipmasquedis1=route1[4]
                                                  service.nexthopedis1=route1[5]
                                        
                                        if debit!="":
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                             shapingoutput = stdout.readlines()
                                             bdfind=bd+" "
                                             sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                             print(sub_l)
                                             if len(sub_l)!=0:
                                               
                                                            session = paramiko.SSHClient()
                                                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                            session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                            stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                            vrfout = stdout.readlines()
                                                            session.close()
                                                            VRFFIND=VRF+" "
                                                            sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                            if yetdown!=-1:
                                                                 service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                            if yetdown==-1 and yetup==-1:
                                                                 service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                            if yetup!=-1:
                                                                 service.generate=rt+'\n'+ inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                                      
                                                            form.save()
                                                            messages.success(request, 'Generation de Script est effectuée avec succes')
                                                            messages.add_message(request,messages.INFO,"Le Shaping est deja Configuré")
                                                            if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                            else:
                                                                  messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")                
                                                            if yetdown!=-1:
                                                                 context ['result'] = [rt, interetdown,descyetdown,undoshutdown, inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2] 
                                                            if yetdown==-1 and yetup==-1:
                                                                 context ['result'] = [rt, interetdown,descyetdown,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                                            if yetup!=-1:
                                                                 context ['result'] = [rt,  inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                                             
                                                  
                                             if len(sub_l)==0: 
                                                       session = paramiko.SSHClient()
                                                       session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                       session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                       stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                       vrfout = stdout.readlines()
                                                       session.close()
                                                       VRFFIND=VRF+" "
                                                       sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                       if yetdown!=-1:
                                                            service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                       if yetdown==-1 and yetup==-1:
                                                            service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                       if yetup!=-1:
                                                            service.generate=rt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                            
                                                       form.save()
                                                       messages.success(request, 'Generation de Script est effectuée avec succes')
                                                       messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                       if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                       else:
                                                             messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")                       
                                                       if yetdown!=-1:
                                                            context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                                       if yetdown==-1 and yetup==-1:
                                                            context ['result'] = [rt, qos ,qu,ququ,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                                       if yetup!=-1:
                                                            context ['result'] = [rt, qos ,qu,ququ,inter,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                                            
                                        else:
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                             vrfout = stdout.readlines()
                                             session.close()
                                             VRFFIND=VRF+" "
                                             sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ] 
                                             if yetdown!=-1:   
                                                  service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+undoshutdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                             if yetdown==-1 and yetup==-1:   
                                                  service.generate=rt+'\n'+interetdown+'\n'+descyetdown+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                             if yetup!=-1:   
                                                  service.generate=rt+'\n'+inter+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                  
                                             messages.success(request, 'Generation de Script est effectuée avec succes')
           
                                             if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                            
                                             else:
                                                   messages.add_message(request,messages.INFO,"Le VRF est deja Configuré") 
                                             if yetdown!=-1:   
                                                  context ['result'] = [rt,interetdown,descyetdown,undoshutdown,inter,vlantype,desc,binding,adresse,stat,upstream,routs1,routs2]  
                                             if yetdown==-1 and yetup==-1:  
                                                  context ['result'] = [rt,interetdown,descyetdown,inter,vlantype,desc,binding,adresse,stat,upstream,routs1,routs2]  
                                             if yetup!=-1:   
                                                  context ['result'] = [rt,inter,vlantype,desc,binding,adresse,stat,upstream,routs1,routs2]  
                                   except ValueError:
                                       messages.error(request, '@ NON VALIDE')    
                              elif  len(route1)==6 and route1[0]=='' or  route1[1]=='' or route1[2]=='' or route1[3]=='' or route1[4]=='' or route1[5]=='':
                                   messages.error(request, ' Erreur Static-route')
                    
                              elif  len(route1)>6:
                                   messages.error(request, ' Erreur Static-route')
                               
                         except ValueError:
                               messages.error(request, '@ NON VALIDE')    

           if  switch1!=None and interface!=None and routeur!="": 
               interface = request.POST.get('monselect')
                                                   
               y=int(interface.find("ge-"))
               indice=['down','up']
               for i in indice:
                    z=int(interface.find(i))
                    if z!=-1:

                         interfacece=interface[y+3:z]
                                                                    
                                                             
                                              
               switch=switch1 
               inter= "interface GigabitEthernet"+"".join(interfacece).strip()+"."+vlan
               
               SWSW=Switch.objects.filter(loopswitch=switch)
               result = SWSW.values() 
               for res in result :
                    print(res)
                    print(type(res)) 
               swsw=list(ServiceManuel.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
               swsw1=list(Service.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
               swsw2=list(L2VC.objects.filter(switch=switch,interfacertsw=("".join(res.get("interfacertsw"))),vlan=vlan))
               
               
               loopsw="<"+res.get("loopswitch")+">"
               looprt="<"+res.get("routeur_id")+">"
               vsw="set vlans "+ nomClient + " vlan-id "+vlan 
                
               descsw="set interfaces "+ interface +" description "+ nomClient
               modesw="set interfaces "+ interface +" unit 0 family ethernet-switching port-mode trunk"
               vlanmembersw="set interfaces "+ interface +" unit 0 family ethernet-switching vlan members "+ nomClient
               vlanmemberswrt="set interfaces "+ res.get("interfaceswrt") +" unit 0 family ethernet-switching vlan members "+ nomClient
               if ("".join(res.get("interfacertsw")).find("Eth"))==-1:
                                                  interfacertsw= "interface GigabitEthernet"+res.get("interfacertsw")+"."+vlan
               else:
                                                  interfacertsw= "interface "+res.get("interfacertsw")+"."+vlan                        
               
               session = paramiko.SSHClient()
               session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
               stdin, stdout, stderr = session.exec_command(" dis cu "+interfacertsw)

               outputinterfacrtevlan = stdout.readlines()
               session.close()
               
               if len(swsw)==0 and len(swsw1)==0  and len(swsw2)==0 :
                    if("".join(outputinterfacrtevlan).find("Error"))==-1:
                          messages.error(request, 'VLAN deja configuré sur cette Interface')  
                    else:
                         try:
                              ipaddress.ip_address(ipGW)
                              ipaddress.ip_address(ipmasque)
                               
                                    
                              
                          
                              if len(route1)==0 :
                                             
                                             form=ServiceManuelForm(request.POST)
                                             if form.is_valid:
                                                  service=form.save(commit=False)
                                                  service.user=request.user.username
                                                  service.interface=interfacece
                                                  service.switch=switch
                                                  service.interfacertsw=("".join(res.get("interfacertsw")))
                                        
                                             if debit!="":
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                  shapingoutput = stdout.readlines()
                                                  bdfind=bd+" "
                                                  sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                  print(sub_l)
                                                  if len(sub_l)!=0:
                                                  
                                                        
                                                                 session = paramiko.SSHClient()
                                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                 stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                 vrfout = stdout.readlines()
                                                                 session.close()
                                                                 VRFFIND=VRF+" "
                                                                 sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                 service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n' +interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                 form.save()
                                                                 messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                 messages.add_message(request,messages.INFO,"Le Shaping est deja Configuré")
                                                                 if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                 else:
                                                                       messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")           
                                                                 context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,  interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                                     
                                                  if len(sub_l)==0:
                                                                 session = paramiko.SSHClient()
                                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                 stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                 vrfout = stdout.readlines()
                                                                 session.close()
                                                                 VRFFIND=VRF+" "
                                                                 sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                 service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream
                                                                 form.save()
                                                                 messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                 messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                 if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                 else:
                                                                       messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")          
                                                                 context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,qu,ququ,interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream]
                                             else :
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")
                                                  vrfout = stdout.readlines()
                                                  session.close()
                                                  VRFFIND=VRF+" "
                                                  sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                  service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream
                                                  form.save()
                                                  messages.success(request, 'Generation de Script est effectuée avec succes')
                                      
                                                  if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                  else:
                                                        messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                  context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresse,stat,upstream]
                              elif len(route1)==1 or len(route1)==2:    
                                        messages.error(request, 'Erreur Static-Route') 

                              elif len(route1)==3 and route1[0]!='' and  route1[1]!='' and route1[2]!='':
                                   try:
                                        ipaddress.ip_address(route1[0])
                                        ipaddress.ip_address(route1[1])
                                        ipaddress.ip_address(route1[2])
                                        routs1="ip route-static vpn-instance "+ VRF+" "+ route1[0]+" "+ route1[1]+" "+route1[2]+" "+ desc
                                        print (routs1) 
                                        form=ServiceManuelForm(request.POST)
                                        
                                        if form.is_valid:
                                             
															

														 
                                             service=form.save(commit=False)
                                             service.user=request.user.username
                                             service.interface=interfacece
                                             service.switch=switch
                                             service.interfacertsw=("".join(res.get("interfacertsw")))
                                             service.dist=route1[0]
                                             service.ipmasquedis=route1[1]
                                             service.nexthopedis=route1[2] 
                                        
                                        if debit!="":
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                  shapingoutput = stdout.readlines()
                                                  bdfind=bd+" "
                                                  sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                  print(sub_l)
                                                  if len(sub_l)!=0:
                                                    
                                                                      session = paramiko.SSHClient()
                                                                      session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                      session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                      stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                      vrfout = stdout.readlines()
                                                                      session.close()
                                                                      VRFFIND=VRF+" "
                                                                      sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                       
                                                                      service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n' +interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                      form.save()
                                                                      messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                      messages.add_message(request,messages.INFO,"Le  Shaping est deja configuré")
                                                                      if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                      else: 
                                                                                messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")   
                                                                      context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,  interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                        
                                                        
                                                  if len(sub_l)==0:
                                                                 session = paramiko.SSHClient()
                                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                 stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                 vrfout = stdout.readlines()
                                                                 session.close()
                                                                 VRFFIND=VRF+" "
                                                                 sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                 service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1
                                                                 form.save()
                                                                 messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                 messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                                 if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                 else:
                                                                      messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")   
                                                                 context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,qu,ququ,interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1]
                                        else: 
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                             vrfout = stdout.readlines()
                                             session.close()
                                             VRFFIND=VRF+" "
                                             sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                             service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1
                                             form.save()
                                             messages.success(request, 'Generation de Script est effectuée avec succes')
                                             if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                             else:
                                                  messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")   
                                             context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresse,stat,upstream,routs1]
                                   except ValueError:
                                         messages.error(request, '@ NON VALIDE')
                              elif  len(route1)==3 and route1[0]=='' or  route1[1]=='' or route1[2]=='':
                                   messages.error(request, ' Erreur Static-Route')

                              elif  len(route1)==6 and route1[0]!='' and  route1[1]!='' and route1[2]!='' and route1[3]!='' and route1[4]!='' and route1[5]!='':
                             
                                   try:
                                        ipaddress.ip_address(route1[0])
                                        ipaddress.ip_address(route1[1])
                                        ipaddress.ip_address(route1[2])
                                        ipaddress.ip_address(route1[3])
                                        ipaddress.ip_address(route1[4])
                                        ipaddress.ip_address(route1[5])
                                        routs1="ip route-static vpn-instance "+ VRF+" "+ route1[0]+" "+ route1[1]+" "+route1[2]+" "+ desc
                                        routs2="ip route-static vpn-instance "+ VRF+" "+ route1[3]+" "+ route1[4]+" "+route1[5]+" "+ desc   
                                        form=ServiceManuelForm(request.POST)
                                        if form.is_valid:
                                                  
                                                  service=form.save(commit=False)
                                                  service.user=request.user.username
                                                  service.interface=interfacece
                                                  service.switch=switch
                                                  service.interfacertsw=("".join(res.get("interfacertsw")))
                                                  service.dist=route1[0]
                                                  service.ipmasquedis=route1[1]
                                                  service.nexthopedis=route1[2]
                                                  service.dist1=route1[3]
                                                  service.ipmasquedis1=route1[4]
                                                  service.nexthopedis1=route1[5]
                                        
                                        if debit!="":
                                                  session = paramiko.SSHClient()
                                                  session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                  session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                  stdin, stdout, stderr = session.exec_command("dis qos-profile configuration | no-more  ")

                                                  shapingoutput = stdout.readlines()
                                                  bdfind=bd+" "
                                                  sub_l = [i for i in shapingoutput if i.find(bdfind)!=-1 ]
                                                  print(sub_l)
                                                  if len(sub_l)!=0:
                                                    
                                                                 session = paramiko.SSHClient()
                                                                 session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                                 session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                                 stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                                 vrfout = stdout.readlines()
                                                                 session.close()
                                                                 VRFFIND=VRF+" "
                                                                 sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                                 service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+ interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                                 form.save()
                                                                 messages.success(request, 'Generation de Script est effectuée avec succes')
                                                                 messages.add_message(request,messages.INFO,"Le  Shaping est deja Configuré")
                                                                 if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                                 else:
                                                                        messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                                 context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]  
                                        
                                                       
                                                             
                                                  if len(sub_l)==0:
                                                            session = paramiko.SSHClient()
                                                            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                                            session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                                            stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                                            vrfout = stdout.readlines()
                                                            session.close()
                                                            VRFFIND=VRF+" "
                                                            sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                                            service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+qos+'\n'+qu+'\n'+ququ+'\n'+interfacertsw+'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+Inp+'\n'+out+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                                            form.save()
                                                            messages.success(request, 'Generation de Script est effectuée avec succes')
                                                            messages.add_message(request,messages.SUCCESS,"Generation de Shaping est effectuée avec succes")
                                                            if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                                            else:
                                                                 messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                                            context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt, qos ,qu,ququ,interfacertsw,vlantype,desc,binding,adresse,Inp,out,stat,upstream,routs1,routs2]                                          
                                        else:
                                             session = paramiko.SSHClient()
                                             session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                             session.connect(routeur, port=22, username= 'ing_onap', password='Ingenierie@!23')
                                             stdin, stdout, stderr = session.exec_command("dis ip vpn-instance | no-more")

                                             vrfout = stdout.readlines()
                                             session.close()
                                             VRFFIND=VRF+" "
                                             sub_vrf = [j for j in vrfout if j.find(VRFFIND)!=-1 ]
                                             service.generate=loopsw+'\n'+vsw+'\n'+descsw+'\n'+modesw+'\n'+vlanmembersw+'\n'+vlanmemberswrt+'\n'+looprt+'\n'+interfacertsw +'\n'+vlantype+'\n'+desc+'\n'+binding+'\n'+adresse+'\n'+stat+'\n'+upstream+'\n'+routs1+'\n'+routs2
                                             messages.success(request, 'Generation de Script est effectuée avec succes')
                                             if len(sub_vrf)==0:     
                                                                                
                                                                                messages.add_message(request,messages.WARNING,"Le VRF est Non Configuré")
                                             else:
                                                   messages.add_message(request,messages.INFO,"Le VRF est deja Configuré")
                                             context ['result'] = [loopsw,vsw,descsw,modesw,vlanmembersw,vlanmemberswrt,looprt,interfacertsw,vlantype,desc,binding,adresse,stat,upstream,routs1,routs2]  
                                   except ValueError:
                                       messages.error(request, '@ NON VALIDE')    
                              elif  len(route1)==6 and route1[0]=='' or  route1[1]=='' or route1[2]=='' or route1[3]=='' or route1[4]=='' or route1[5]=='':
                                   messages.error(request, ' Erreur Static-route')
                    
                              elif  len(route1)>6:
                                   messages.error(request, ' Erreur Static-route')
                               
                         except ValueError:
                               messages.error(request, '@ NON VALIDE')      
               else:
                     messages.error(request, 'Service deja traité')                         
     return render(request, 'liste_routeur/Addservicemanuel.html',context)

 except:
                return render(request, 'liste_routeur/erreurconnect.html')     


@login_required(login_url='login')
@forCustomer
def SCmanuel(request):
     service=ServiceManuel.objects.all()
      
      
     
     context={'service':service}
     return render(request, 'liste_routeur/scriptmanuel.html',context)

def nodeToDictionary(node):
    """
    A utility function to convert object of type Blog to a Python Dictionary
    """
    output = {}
    output["id_node"] = node.id_node
    output["name"] = node.name
    output["device_type"] = node.device_type
    output["x"] = node.x
    output["y"] = node.y
     
   

    return output

def linkToDictionary(link):
    """
    A utility function to convert object of type Blog to a Python Dictionary
    """
    output = {}
    output["src_name"] = link.src_name
    output["dist_name"] = link.dist_name
    output["source"] = link.source
    output["target"] = link.target
    output["srcUtilMap"] = link.srcUtilMap
     
   

    return output

@login_required(login_url='login')
@forCustomer
def devicetopologie(request):
      
     #FN.objects.filter().values_list('description','percent')
      
     tempnodes = [] 
     templinks = []
     nodes = Node.objects.all()
     links=Link.objects.all()
     for i in range(len(nodes)):
            tempnodes.append(nodeToDictionary(nodes[i]))  
     for i in range(len(links)):
            templinks.append(linkToDictionary(links[i])) 
     nodes = tempnodes
     links = templinks
     context={ 
            
               "nodes": nodes,
               "links":links
              }

     return render(request, 'liste_routeur/testnextUI.html',context)
from django.db.models import Q, Sum


@swagger_auto_schema(method='get'   ,operation_description="Methode sert a recuperer les scripts New Service ralises par ING IP", responses={200: ServiceSerializer, 404:"HTTP_404_NOT_FOUND",401:"Token Invalid",429:"Request was throttled"})
@api_view(['GET'])
def newservice_list(request):
    try:
        if request.method == 'GET':
            service = Service.objects.filter(etat='DEMANDE') 

            serializer = ServiceSerializer(service, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except:
        Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='get'   ,operation_description="Methode sert a recuperer les scripts update ralises par ING IP", responses={200: ScriptSerializer,404:"HTTP_404_NOT_FOUND",401:"Token Invalid",429:"Request was throttled"})
@api_view(['GET'])
def updservice_list(request):
    try:
        if request.method == 'GET':
            script = Script.objects.filter(etat='DEMANDE')

            serializer = ScriptSerializer(script, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except:
        Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='put' , request_body=ServiceSerializer,operation_description="Methode sert a mettre a jour les scripts New Service ralises par ING IP", responses={200: ServiceSerializer,404:"HTTP_404_NOT_FOUND",401:"Token Invalid",429:"Request was throttled",406:"Access denied to this object"})
@api_view(['GET', 'PUT'])
def crudservice(request, pk):
    try:
        service = Service.objects.get(pk=pk)

    except Service.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' and service.etat=="DEMANDE" or service.etat=="PLANNED":
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    elif request.method == 'PUT' and service.etat=="DEMANDE" or service.etat=="PLANNED":

        serializer = ServiceSerializer(service, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and service.etat=="DEMANDE" or service.etat=="PLANNED":
        service.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)
@swagger_auto_schema(method='put' , request_body=ScriptSerializer,operation_description="Methode sert a mettre a jour les scripts update ralises par ING IP", responses={200: ScriptSerializer,404:"HTTP_404_NOT_FOUND",401:"Token Invalid",429:"Request was throttled",406:"Access denied to this object"})
@api_view(['GET', 'PUT'])
def crudupdate(request, pk):
    try:
        script = Script.objects.get(pk=pk)

    except Script.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' and service.etat=="DEMANDE" or service.etat=="PLANNED":
        serializer = ScriptSerializer(script)
        return Response(serializer.data)

    elif request.method == 'PUT' and service.etat=="DEMANDE" or service.etat=="PLANNED":

        serializer = ScriptSerializer(script, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and service.etat=="DEMANDE" or service.etat=="PLANNED":
        script.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    else:
        return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)


def error_404_view(request,exception):
     return render(request, 'liste_routeur/pages-error-404.html')


def error_500_view(request):
    return render(request, 'liste_routeur/pages-error-500.html')