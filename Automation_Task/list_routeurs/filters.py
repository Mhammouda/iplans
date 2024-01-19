import django_filters
from .models import *

class RouteurFilter(django_filters.FilterSet):
    class Meta:
        model=Routeur
        fields=['name','Loopback']

class ScriptFilter(django_filters.FilterSet):
    class Meta:
        model= Script
        fields=['interface']