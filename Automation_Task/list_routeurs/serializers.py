from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Service,Script


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Service
        fields=('id','nomClient','routeur','interface','vlan','debit','ipadress','ipadresspublic','ipadresspublic31','ipadresspublic28','ipadresspublic29','user','generate','swan','etat','VRF','trans','date_changement','comment')
        read_only_fields = ('user', 'id','routeur','nomClient','swan','generate','ipadress','ipadresspublic','ipadresspublic31','ipadresspublic28','ipadresspublic29','interface','vlan','debit','VRF','trans')


class ScriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Script
        fields=('id','routeur','user','generate','swan','etat','date_changement','comment')
        read_only_fields = ('user', 'id','routeur','swan','generate')
        #read_only_fields = ('user', 'id','routeur','swan','generate')