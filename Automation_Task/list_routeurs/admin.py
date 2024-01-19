from django.contrib import admin

# Register your models here.
from .models import  *
admin.site.register(Script)
admin.site.register(User)
admin.site.register(Routeur)
admin.site.register(Task)
admin.site.register(Execution)
admin.site.register(Service)
admin.site.register(L2VC)
admin.site.register(VRF)
admin.site.register(DelService)
admin.site.register(Switch)
admin.site.register(Trafic)
admin.site.register(Dimens)
admin.site.register(Bh_sharing)  
admin.site.register(FN)
admin.site.register(ServiceManuel)
admin.site.register(Node)
admin.site.register(Link)
admin.site.register(ReportingB2BService)
