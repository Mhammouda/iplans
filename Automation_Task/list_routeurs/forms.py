from django.forms import ModelForm, fields
from .models import Script
from .models import Routeur
from .models import Switch
from .models import User
from .models import Execution
from .models import Service
from .models import L2VC 
from .models import Front 
from .models import VRF
from .models import DelService
from .models import ServiceManuel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ScriptForm(ModelForm):
    class Meta:
        model=Script
        fields="__all__"
        exclude =('user','generate','etat','swan','date_changement','comment')


class L2VCForm(ModelForm):
    class Meta:
        model=L2VC
        fields="__all__"
        exclude =('user','generate','interfacertsw')

class VRFForm(ModelForm):
    class Meta:
        model=VRF
        fields="__all__"

class RouteurForm(ModelForm):
    class Meta:
        model=Routeur
        fields="__all__"

class ServiceForm(ModelForm):
    class Meta:
        model=Service
        fields="__all__"
        exclude =('ipadress','ipadresspublic','interfacertsw','user','ipadresspublic31','generate','etat','swan','date_changement','comment')

class UserForm(ModelForm):
    class Meta:
        model=User
        fields="__all__"

class ExecutionForm(ModelForm):
    class Meta:
        model=Execution
        fields="__all__"


class CreateNewUser(UserCreationForm):
    class Meta:
        model=User
        fields="__all__"

class DelServiceForm(ModelForm):
    class Meta:
        model=DelService
        fields="__all__"
        exclude =('user','generate',)

class SwitchForm(ModelForm):
    class Meta:
        model=Switch
        fields="__all__"

class FrontForm(ModelForm):
    class Meta:
        model=Front
        fields="__all__"
        exclude =('user',)


class ServiceManuelForm(ModelForm):
    class Meta:
        model=ServiceManuel
        fields="__all__"
        exclude =('user','generate','dist','interfacertsw','ipmasquedis','nexthopedis','dist1','ipmasquedis1','nexthopedis1')
