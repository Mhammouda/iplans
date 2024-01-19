from django.apps import AppConfig


class ListRouteursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'list_routeurs'

    def ready(self):
        from . import updater
        updater.start()
        updater.finich()
        updater.collect()
        updater.ras()
        updater.sharingIN()
        updater.resetBH()
        updater.nodal()
        updater.dimnodal()
        updater.resetnodal()
        updater.delnodal()
        updater.dimsw()
        updater.reset_sw()
        updater.startcpumem()
        updater.reset_cpu()
        updater.tOPONODE()
        updater.tOPOLink()
        updater.reporting()