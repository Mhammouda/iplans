from django.db import models
from django import forms
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords
class Task(models.Model):
    task=(
            ('Upgarde','Upgarde'),
            ('ADD_service','ADD_service'),
            ('DEL_service','DEL_service'),
        )
    task=models.CharField(max_length=100, null=True,choices=task)
    def __str__(self):
            return self.task

class User(models.Model):

      username=models.CharField(max_length=190, null=True,unique=True)
      password=models.CharField(max_length=190, null=True)
      port=models.PositiveIntegerField(max_length=5, null=True)
      date=models.DateTimeField(auto_now_add=True, null=True)
      def __str__(self):
            return self.username

class Routeur(models.Model):
    
    name=models.CharField(max_length=190, null=True, unique=True)
    #Loopback=models.CharField(max_length=190, null=True,unique=True)
    Loopback=(
                
('10.51.2.1', '10.51.2.1'),
('10.51.2.10', '10.51.2.10'),
('10.51.2.100', '10.51.2.100'),
('10.51.2.101', '10.51.2.101'),
('10.51.2.102', '10.51.2.102'),
('10.51.2.103', '10.51.2.103'),
('10.51.2.104', '10.51.2.104'),
('10.51.2.105', '10.51.2.105'),
('10.51.2.106', '10.51.2.106'),
('10.51.2.107', '10.51.2.107'),
('10.51.2.108', '10.51.2.108'),
('10.51.2.109', '10.51.2.109'),
('10.51.2.11', '10.51.2.11'),
('10.51.2.110', '10.51.2.110'),
('10.51.2.111', '10.51.2.111'),
('10.51.2.112', '10.51.2.112'),
('10.51.2.113', '10.51.2.113'),
('10.51.2.114', '10.51.2.114'),
('10.51.2.115', '10.51.2.115'),
('10.51.2.116', '10.51.2.116'),
('10.51.2.117', '10.51.2.117'),
('10.51.2.118', '10.51.2.118'),
('10.51.2.119', '10.51.2.119'),
('10.51.2.12', '10.51.2.12'),
('10.51.2.120', '10.51.2.120'),
('10.51.2.121', '10.51.2.121'),
('10.51.2.122', '10.51.2.122'),
('10.51.2.123', '10.51.2.123'),
('10.51.2.124', '10.51.2.124'),
('10.51.2.125', '10.51.2.125'),
('10.51.2.126', '10.51.2.126'),
('10.51.2.127', '10.51.2.127'),
('10.51.2.128', '10.51.2.128'),
('10.51.2.129', '10.51.2.129'),
('10.51.2.13', '10.51.2.13'),
('10.51.2.130', '10.51.2.130'),
('10.51.2.131', '10.51.2.131'),
('10.51.2.132', '10.51.2.132'),
('10.51.2.133', '10.51.2.133'),
('10.51.2.134', '10.51.2.134'),
('10.51.2.135', '10.51.2.135'),
('10.51.2.136', '10.51.2.136'),
('10.51.2.137', '10.51.2.137'),
('10.51.2.138', '10.51.2.138'),
('10.51.2.139', '10.51.2.139'),
('10.51.2.14', '10.51.2.14'),
('10.51.2.140', '10.51.2.140'),
('10.51.2.141', '10.51.2.141'),
('10.51.2.142', '10.51.2.142'),
('10.51.2.143', '10.51.2.143'),
('10.51.2.144', '10.51.2.144'),
('10.51.2.145', '10.51.2.145'),
('10.51.2.146', '10.51.2.146'),
('10.51.2.147', '10.51.2.147'),
('10.51.2.148', '10.51.2.148'),
('10.51.2.149', '10.51.2.149'),
('10.51.2.15', '10.51.2.15'),
('10.51.2.151', '10.51.2.151'),
('10.51.2.152', '10.51.2.152'),
('10.51.2.153', '10.51.2.153'),
('10.51.2.154', '10.51.2.154'),
('10.51.2.155', '10.51.2.155'),
('10.51.2.156', '10.51.2.156'),
('10.51.2.157', '10.51.2.157'),
('10.51.2.158', '10.51.2.158'),
('10.51.2.159', '10.51.2.159'),
('10.51.2.16', '10.51.2.16'),
('10.51.2.160', '10.51.2.160'),
('10.51.2.161', '10.51.2.161'),
('10.51.2.162', '10.51.2.162'),
('10.51.2.163', '10.51.2.163'),
('10.51.2.164', '10.51.2.164'),
('10.51.2.165', '10.51.2.165'),
('10.51.2.166', '10.51.2.166'),
('10.51.2.167', '10.51.2.167'),
('10.51.2.168', '10.51.2.168'),
('10.51.2.169', '10.51.2.169'),
('10.51.2.17', '10.51.2.17'),
('10.51.2.170', '10.51.2.170'),
('10.51.2.171', '10.51.2.171'),
('10.51.2.172', '10.51.2.172'),
('10.51.2.173', '10.51.2.173'),
('10.51.2.174', '10.51.2.174'),
('10.51.2.175', '10.51.2.175'),
('10.51.2.176', '10.51.2.176'),
('10.51.2.177', '10.51.2.177'),
('10.51.2.178', '10.51.2.178'),
('10.51.2.179', '10.51.2.179'),
('10.51.2.18', '10.51.2.18'),
('10.51.2.180', '10.51.2.180'),
('10.51.2.181', '10.51.2.181'),
('10.51.2.182', '10.51.2.182'),
('10.51.2.183', '10.51.2.183'),
('10.51.2.184', '10.51.2.184'),
('10.51.2.185', '10.51.2.185'),
('10.51.2.186', '10.51.2.186'),
('10.51.2.187', '10.51.2.187'),
('10.51.2.188', '10.51.2.188'),
('10.51.2.189', '10.51.2.189'),
('10.51.2.19', '10.51.2.19'),
('10.51.2.190', '10.51.2.190'),
('10.51.2.191', '10.51.2.191'),
('10.51.2.192', '10.51.2.192'),
('10.51.2.193', '10.51.2.193'),
('10.51.2.194', '10.51.2.194'),
('10.51.2.195', '10.51.2.195'),
('10.51.2.196', '10.51.2.196'),
('10.51.2.197', '10.51.2.197'),
('10.51.2.198', '10.51.2.198'),
('10.51.2.199', '10.51.2.199'),
('10.51.2.2', '10.51.2.2'),
('10.51.2.20', '10.51.2.20'),
('10.51.2.201', '10.51.2.201'),
('10.51.2.202', '10.51.2.202'),
('10.51.2.203', '10.51.2.203'),
('10.51.2.204', '10.51.2.204'),
('10.51.2.205', '10.51.2.205'),
('10.51.2.206', '10.51.2.206'),
('10.51.2.207', '10.51.2.207'),
('10.51.2.208', '10.51.2.208'),
('10.51.2.209', '10.51.2.209'),
('10.51.2.21', '10.51.2.21'),
('10.51.2.210', '10.51.2.210'),
('10.51.2.211', '10.51.2.211'),
('10.51.2.212', '10.51.2.212'),
('10.51.2.213', '10.51.2.213'),
('10.51.2.214', '10.51.2.214'),
('10.51.2.215', '10.51.2.215'),
('10.51.2.216', '10.51.2.216'),
('10.51.2.217', '10.51.2.217'),
('10.51.2.218', '10.51.2.218'),
('10.51.2.219', '10.51.2.219'),
('10.51.2.22', '10.51.2.22'),
('10.51.2.220', '10.51.2.220'),
('10.51.2.221', '10.51.2.221'),
('10.51.2.222', '10.51.2.222'),
('10.51.2.223', '10.51.2.224'),
('10.51.2.225', '10.51.2.225'),
('10.51.2.226', '10.51.2.226'),
('10.51.2.227', '10.51.2.227'),
('10.51.2.228', '10.51.2.228'),
('10.51.2.229', '10.51.2.229'),
('10.51.2.23', '10.51.2.23'),
('10.51.2.230', '10.51.2.230'),
('10.51.2.231', '10.51.2.231'),
('10.51.2.232', '10.51.2.232'),
('10.51.2.233', '10.51.2.233'),
('10.51.2.234', '10.51.2.234'),
('10.51.2.235', '10.51.2.235'),
('10.51.2.236', '10.51.2.236'),
('10.51.2.237', '10.51.2.237'),
('10.51.2.238', '10.51.2.238'),
('10.51.2.239', '10.51.2.239'),
('10.51.2.24', '10.51.2.24'),
('10.51.2.240', '10.51.2.240'),
('10.51.2.241', '10.51.2.241'),
('10.51.2.242', '10.51.2.242'),
('10.51.2.243', '10.51.2.243'),
('10.51.2.244', '10.51.2.244'),
('10.51.2.245', '10.51.2.245'),
('10.51.2.246', '10.51.2.246'),
('10.51.2.247', '10.51.2.247'),
('10.51.2.248', '10.51.2.248'),
('10.51.2.249', '10.51.2.249'),
('10.51.2.25', '10.51.2.25'),
('10.51.2.250', '10.51.2.250'),
('10.51.2.251', '10.51.2.251'),
('10.51.2.252', '10.51.2.252'),
('10.51.2.253', '10.51.2.253'),
('10.51.2.254', '10.51.2.254'),
('10.51.2.26', '10.51.2.26'),
('10.51.2.27', '10.51.2.27'),
('10.51.2.28', '10.51.2.28'),
('10.51.2.29', '10.51.2.29'),
('10.51.2.3', '10.51.2.3'),
('10.51.2.30', '10.51.2.30'),
('10.51.2.31', '10.51.2.31'),
('10.51.2.32', '10.51.2.32'),
('10.51.2.33', '10.51.2.33'),
('10.51.2.34', '10.51.2.34'),
('10.51.2.35', '10.51.2.35'),
('10.51.2.36', '10.51.2.36'),
('10.51.2.37', '10.51.2.37'),
('10.51.2.38', '10.51.2.38'),
('10.51.2.39', '10.51.2.39'),
('10.51.2.4', '10.51.2.4'),
('10.51.2.40', '10.51.2.40'),
('10.51.2.41', '10.51.2.41'),
('10.51.2.42', '10.51.2.42'),
('10.51.2.43', '10.51.2.43'),
('10.51.2.44', '10.51.2.44'),
('10.51.2.45', '10.51.2.45'),
('10.51.2.46', '10.51.2.46'),
('10.51.2.47', '10.51.2.47'),
('10.51.2.48', '10.51.2.48'),
('10.51.2.49', '10.51.2.49'),
('10.51.2.5', '10.51.2.5'),
('10.51.2.50', '10.51.2.50'),
('10.51.2.51', '10.51.2.51'),
('10.51.2.52', '10.51.2.52'),
('10.51.2.53', '10.51.2.53'),
('10.51.2.54', '10.51.2.54'),
('10.51.2.55', '10.51.2.55'),
('10.51.2.56', '10.51.2.56'),
('10.51.2.57', '10.51.2.57'),
('10.51.2.58', '10.51.2.58'),
('10.51.2.59', '10.51.2.59'),
('10.51.2.6', '10.51.2.6'),
('10.51.2.60', '10.51.2.60'),
('10.51.2.61', '10.51.2.61'),
('10.51.2.62', '10.51.2.62'),
('10.51.2.63', '10.51.2.63'),
('10.51.2.64', '10.51.2.64'),
('10.51.2.65', '10.51.2.65'),
('10.51.2.66', '10.51.2.66'),
('10.51.2.67', '10.51.2.67'),
('10.51.2.68', '10.51.2.68'),
('10.51.2.69', '10.51.2.69'),
('10.51.2.7', '10.51.2.7'),
('10.51.2.70', '10.51.2.70'),
('10.51.2.71', '10.51.2.71'),
('10.51.2.72', '10.51.2.72'),
('10.51.2.73', '10.51.2.73'),
('10.51.2.74', '10.51.2.74'),
('10.51.2.75', '10.51.2.75'),
('10.51.2.76', '10.51.2.76'),
('10.51.2.78', '10.51.2.78'),
('10.51.2.79', '10.51.2.79'),
('10.51.2.8', '10.51.2.8'),
('10.51.2.80', '10.51.2.80'),
('10.51.2.81', '10.51.2.81'),
('10.51.2.82', '10.51.2.82'),
('10.51.2.83', '10.51.2.83'),
('10.51.2.84', '10.51.2.84'),
('10.51.2.85', '10.51.2.85'),
('10.51.2.86', '10.51.2.86'),
('10.51.2.87', '10.51.2.87'),
('10.51.2.88', '10.51.2.88'),
('10.51.2.89', '10.51.2.89'),
('10.51.2.9', '10.51.2.9'),
('10.51.2.90', '10.51.2.90'),
('10.51.2.91', '10.51.2.91'),
('10.51.2.92', '10.51.2.92'),
('10.51.2.93', '10.51.2.93'),
('10.51.2.94', '10.51.2.94'),
('10.51.2.95', '10.51.2.95'),
('10.51.2.96', '10.51.2.96'),
('10.51.2.97', '10.51.2.97'),
('10.51.2.98', '10.51.2.98'),
('10.51.2.99', '10.51.2.99'),

                                                
    )
    Loopback=models.CharField(max_length=100, null=True,choices=Loopback,unique=True)
    category=(
            ('NE40E-X3','NE40E-X3'),
            ('NE40E-M2E','NE40E-M2E'),
            ('NE40E-X16A(V8)','NE40E-X16A(V8)'),
            ('NE40E-X2-M8','NE40E-X2-M8'),
            ('NE40E-X2-M8A','NE40E-X2-M8A'),
            ('NE40E-X8','NE40E-X8'),
            ('NE40E-X8A(V8)','NE40E-X8A(V8)'),
            ('NE8000_M8','NE8000_M8'),
            ('NE8000_M14','NE8000_M14'),
      
    )

    category=models.CharField(max_length=100, null=True,choices=category)
    percentmemory=models.FloatField(null=True,blank=True,default=0)
    percentcpu=models.FloatField(null=True,blank=True,default=0)
    def __str__(self):
        return self.name + "\n\n" + self.Loopback

# Create your models here.
class Switch(models.Model):
    namedevice=models.CharField(max_length=100, null=True,unique=True)
    loopswitch=models.CharField(max_length=100, null=True,unique=True)
    interfaceswrt=models.CharField(max_length=100, null=True)
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback')
    interfacertsw=models.CharField(max_length=100, null=True)
    percent=models.FloatField(null=True,blank=True,default=0)
    capa=models.CharField(max_length=20000, null=True,default="1G")
    date=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.namedevice + "\n\n\n\n\n\n\n\n" + str(self.loopswitch) 
         



class Script(models.Model):

     
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback')
     

    interface=models.CharField(max_length=100, null=True,blank=True)
     
    debit=models.PositiveIntegerField(max_length=5, null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
    user=models.CharField(max_length=1000, null=True)
    generate=models.TextField(max_length=10000, null=True)
    etat = models.CharField(max_length=100000, null=True, blank=True, default="DEMANDE")
    swan = models.CharField(max_length=100000, null=True, blank=True, default="XXXXX")
    date_changement = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    comment = models.CharField(max_length=10000, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.interface + "\n\n\n\n\n\n\n\n" + "\n\n\n\n\n\n\n\n\n\n" +  str(self.routeur)
  
class Execution(models.Model):
     
    script=models.TextField(max_length=1000, null=True)
    def __str__(self):
        return self.script

class Service(models.Model):

    nomClient=models.CharField(max_length=100, null=True,default='nom du client')
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback',blank=True)
    switch=models.CharField(max_length=100, null=True,blank=True)
    interface=models.CharField(max_length=100, null=True,blank=True)
    interfacertsw=models.CharField(max_length=100, null=True,blank=True)
    vlan=models.PositiveIntegerField(max_length=5, null=True)
    debit=models.PositiveIntegerField(max_length=5, null=True, blank=True)
    ipadress=models.CharField(max_length=100, null=True, blank=True)
    ipadresspublic=models.CharField(max_length=100, null=True, blank=True) 
    ipadresspublic31=models.CharField(max_length=100, null=True, blank=True)
    ipadresspublic28 = models.CharField(max_length=100, null=True, blank=True)
    ipadresspublic29 = models.CharField(max_length=100, null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
    user=models.CharField(max_length=100, null=True)
    
    
    VRF=(
                ('Internet_vpn','Internet_vpn'),
                 
            )


    VRF=models.CharField(max_length=100, null=True,choices=VRF)
    trans=(
            ('FH','FH'),
            ('FO','FO'),

    )
    trans=models.CharField(max_length=100, null=True,choices=trans)
    generate=models.TextField(max_length=100000, null=True, blank=True)
    etat = models.CharField(max_length=100000, null=True, blank=True, default="DEMANDE")
    swan = models.CharField(max_length=100000, null=True, blank=True, default="XXXXX")

    date_changement = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    comment=models.CharField(max_length=10000, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.interface



class L2VC(models.Model):
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback',blank=True)
    switch=models.CharField(max_length=100, null=True,choices=[],blank=True)
    interface=models.CharField(max_length=100, null=True,choices=[],blank=True)
    interfacertsw=models.CharField(max_length=100, null=True,choices=[],blank=True)
    vlan=models.PositiveIntegerField(max_length=5, null=True)
    description=models.CharField(max_length=100, null=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
    user=models.CharField(max_length=100, null=True)
    trans=(
            ('FH','FH'),
            ('FO','FO'),

    )
    trans=models.CharField(max_length=100, null=True,choices=trans)
     

    dist=(
            ('10.51.2.4','10.51.2.4'),
            ('10.51.2.2','10.51.2.2'),

    )
    dist=models.CharField(max_length=100, null=True,choices=dist)
    generate=models.CharField(max_length=20000, null=True)
    def __str__(self):
        return self.interface

class VRF(models.Model):
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback')
    route_distinguisher=models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.route_distinguisher 

class DelService(models.Model):
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback')
    interface=models.CharField(max_length=100, null=True,choices=[],blank=True)
     
    date=models.DateTimeField(auto_now_add=True, null=True)
    user=models.CharField(max_length=100, null=True)
    generate=models.CharField(max_length=100000, null=True)
    def __str__(self):
        return self.interface

class Front(models.Model):
    nom_client=models.CharField(max_length=100, null=True)
    List_client=models.CharField(max_length=100, null=True,choices=[],blank=True)
     
    date=models.DateTimeField(auto_now_add=True, null=True)
    user=models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.interface

class Trafic(models.Model):
    routeur=models.CharField(max_length=100, null=True)
    percent=models.FloatField(null=True,choices=[],blank=True)
     
    date=models.DateTimeField(auto_now_add=True, null=True)
     
    def __str__(self):
        return self.routeur


class Dimens(models.Model):
   
    liaison=models.CharField(max_length=20000, null=True)
    loopback_dim=models.CharField(max_length=20000, null=True)
    percent=models.FloatField(null=True,blank=True,default=0)
    capa=models.CharField(max_length=20000, null=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
    interface=models.CharField(max_length=20000, null=True,blank=True)    
    def __str__(self):
        return self.liaison


 
class Bh_sharing(models.Model):
    liaison=models.CharField(max_length=20000, null=True)
    loopback_dim=models.CharField(max_length=20000, null=True)
    percent=models.FloatField(null=True,blank=True,default=0)
    interface=models.CharField(max_length=20000, null=True)
    capa=models.CharField(max_length=20000, null=True)
    typeBH=(
            ('BH_TT','BH_TT'),
            ('BH_OOO','BH_OOO'),

    )
    typeBH=models.CharField(max_length=100, null=True,choices=typeBH)
    date=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.liaison


class FN(models.Model):
       
    description=models.CharField(max_length=20000, null=True)
    interface=models.CharField(max_length=20000, null=True)
    routeur=models.CharField(max_length=100, null=True)
    percent=models.FloatField(null=True,blank=True,default=0)
    capa=models.CharField(max_length=20000, null=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
     
    def __str__(self):
        return self.description
    

 
class ServiceManuel(models.Model):
    
    nomClient=models.CharField(max_length=100, null=True,default='nom du client')
    routeur=models.ForeignKey(Routeur,null=True,on_delete=models.SET_NULL, to_field='Loopback')
    switch=models.CharField(max_length=100, null=True,choices=[],blank=True)
    interface=models.CharField(max_length=100, null=True,choices=[],blank=True)
    interfacertsw=models.CharField(max_length=100, null=True,choices=[],blank=True)
    vlan=models.PositiveIntegerField(max_length=5, null=True)
    debit=models.PositiveIntegerField(max_length=5, null=True, blank=True)
    ipGW=models.CharField(max_length=100, null=True )
    ipmasque=models.CharField(max_length=100, null=True)
    date=models.DateTimeField(auto_now_add=True, null=True)
    VRF=(
                ('Internet_vpn','Internet_vpn'),
                ('Boutique_Orange','Boutique_Orange'),
                ('Voice_vpn','Voice_vpn'),
                ('CCTV_Wimax','CCTV_Wimax'),
                ('CCTV','CCTV'),
                ('MonitoringB2B_vpn','MonitoringB2B_vpn'),
                ('Voice_Avaya_Client','Voice_Avaya_Client')
            )


    VRF=models.CharField(max_length=100, null=True,choices=VRF)
    trans=(
            ('FH','FH'),
            ('FO','FO'),

    )
    trans=models.CharField(max_length=100, null=True,choices=trans)
    user=models.CharField(max_length=100, null=True)
    generate=models.CharField(max_length=100000, null=True)
    dist=models.CharField(max_length=100, null=True)
    ipmasquedis=models.CharField(max_length=100, null=True)
    nexthopedis=models.CharField(max_length=100, null=True)
    dist1=models.CharField(max_length=100, null=True)
    ipmasquedis1=models.CharField(max_length=100, null=True)
    nexthopedis1=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.interface

class Node(models.Model):
    id_node=models.CharField(null=True,blank=True,max_length=20000000)
    name=models.CharField(null=True,blank=True,max_length=20000000)
    device_type=models.CharField(null=True,blank=True,max_length=20000000)
    x=models.PositiveIntegerField(null=True,blank=True)  
    y=models.PositiveIntegerField(null=True,blank=True)
    def __str__(self):
        return self.name
class Link(models.Model):
   
    src_name=models.CharField(null=True,blank=True,max_length=20000000)
    dist_name=models.CharField(null=True,blank=True,max_length=20000000)
    source=models.CharField(null=True,blank=True,max_length=20000000)
    target=models.CharField(null=True,blank=True,max_length=20000000)
    srcUtilMap=models.PositiveIntegerField(null=True,blank=True)
      
    def __str__(self):
        return self.src_name


class ReportingB2BService(models.Model):
    name_device = models.CharField(null=True, blank=True, max_length=20000000)
    nbr_service_Internet=models.PositiveIntegerField(null=True,blank=True)
    nbr_service_voip = models.PositiveIntegerField(null=True, blank=True)
    nbr_service_L2VC = models.PositiveIntegerField(null=True, blank=True)
    nbr_service_BUSINESS_CLIENT_VSI = models.PositiveIntegerField(null=True, blank=True)
    nbr_service_BUSINESS_VSI = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name_device