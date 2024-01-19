from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name="home"),
    path('routeur/',views.routeur , name="routeur"),
    path('newservice/', views.newservice_list),
    path('updservice/', views.updservice_list),
    path('crudservice/<int:pk>/', views.crudservice),
    path('crudupdate/<int:pk>/', views.crudupdate),
    path('switch/',views.SW ,name="sw"),
    path('front/',views.front ,name="front"),
    path('serviceL2VC/',views.serviceL2VC ,name="serviceL2VC"),
    path('MX/<str:pk>',views.MX ,name="MX"),
    path('script/',views.SC ,name="SC"),
    path('Visiteur/',views.Visiteur ,name="Visiteur"),
    path('SCADMIN/',views.SCADMIN ,name="SCADMIN"),
    path('SCADMINBBIP/',views.SCADMINBBIP ,name="SCADMINBBIP"),
    path('SCADMINBBTRAFIC/',views.SCADMINBBTRAFIC ,name="SCADMINBBTRAFIC"),
    path('SCADMINBH/',views.SCADMINBH ,name="SCADMINBH"),
    path('SCADMINFN/',views.SCADMINFN ,name="SCADMINFN"),
    path('SCADMINSW/',views.SCADMINSW ,name="SCADMINSW"),
    path('SCADMINCPU/',views.SCADMINCPU ,name="SCADMINCPU"),


    path('devicetopologie/',views.devicetopologie ,name="devicetopologie"),


    path('create/',views.create ,name="create"),
    path('dimmensionnement/',views.dimmensionnement ,name="dimmensionnement"),
    path('SCmanuel/',views.SCmanuel ,name="SCmanuel"),
    path('servicemanuel/',views.servicemanuel ,name="servicemanuel"),
    path('dimmensionnementBH/',views.dimmensionnementBH ,name="dimmensionnementBH"),
    path('dimmensionnementFN/',views.dimmensionnementFN ,name="dimmensionnementFN"),
    path('dimmensionnementsw/',views.dimmensionnementsw ,name="dimmensionnementsw"),
    path('dimmensionnementMECP/',views.dimmensionnementMECP ,name="dimmensionnementMECP"),
    path('genratescript/',views.genratescript ,name="genratescript"),
    path('adduser/',views.adduser ,name="adduser"),
    path('deletedelserviceALL/',views.deletedelserviceALL ,name="deletedelserviceALL"),
    path('deletedelservice/<str:pk>',views.deletedelservice ,name="deletedelservice"),
    path('deletedelscriptALL/',views.deletedelscriptALL ,name="deletedelscriptALL"),
    path('deletedelscript/<str:pk>',views.deletedelscript ,name="deletedelscript"),

    path('deletedelscriptALLMAN/',views.deletedelscriptALLMAN ,name="deletedelscriptALLMAN"),
    path('deletedelscriptMAN/<str:pk>',views.deletedelscriptMAN ,name="deletedelscriptMAN"),

    path('deleteserviceALL/',views.deleteserviceALL ,name="deleteserviceALL"),
    path('changelog/',views.changelog ,name="changelog"),
    path('deleteL2VCALL/',views.deleteL2VCALL ,name="deleteL2VCALL"),
    path('update/<str:pk>',views.update ,name="update"),

    path('deleteL2VC/<str:pk>',views.deleteL2VC ,name="deleteL2VC"),
    path('updateswitch/<str:pk>',views.updateswitch ,name="updateswitch"),
    path('updateuser/<str:pk>',views.updateuser ,name="updateuser"),
    path('generatescript/<str:pk>',views.generatescript ,name="generatescript"),
    path('generatenewscript/<str:pk>',views.generatenewscript ,name="generatenewscript"),

    path('generatedelscript/<str:pk>',views.generatedelscript ,name="generatedelscript"),
    path('generateupscript/<str:pk>',views.generateupscript ,name="generateupscript"),
    path('generatescriptmanuel/<str:pk>',views.generatescriptmanuel ,name="generatescriptmanuel"),

    path('generatescript1/<str:pk>',views.generatescript1 ,name="generatescript1"),
    path('generatenewscript1/<str:pk>',views.generatenewscript1 ,name="generatenewscript1"),

    path('generatedelscript1/<str:pk>',views.generatedelscript1 ,name="generatedelscript1"),
    path('generateupscript1/<str:pk>',views.generateupscript1 ,name="generateupscript1"),
    path('delete-script/<str:pk>/', views.delete_script, name='delete-script'),



    path('delete_service/<str:pk>/', views.delete_service, name='delete_service'),
    path('change_architect_service/<str:pk>/', views.change_architect_service_NAT, name='change_architect_service'),
    path('sans_nat_avec_CPE/<str:pk>/', views.change_architect_service_SANS_NAT_AVEC_CPE, name='sans_nat_avec_CPE'),
    path('sans_nat_sans_CPE/<str:pk>/', views.change_architect_service_SANS_NAT_SANS_CPE, name='sans_nat_sans_CPE'),

    path('delete_service_manuel/<str:pk>/', views.delete_service_manuel, name='delete_service_manuel'),
    path('delete_service_resiliation/<str:pk>/', views.delete_service_resiliation, name='delete_service_resiliation'),
    path('delete_service_MPLS/<str:pk>/', views.delete_service_MPLS, name='delete_service_MPLS'),



    path('addscript/',views.index ,name="addscript"),

    path('deleteservice/<str:pk>',views.deleteservice ,name="deleteservice"),
    path('deleterouteur/<str:pk>',views.deleterouteur ,name="deleterouteur"),
    path('deleteswitch/<str:pk>',views.deleteswitch ,name="deleteswitch"),
    path('deleteuser/<str:pk>',views.deleteuser ,name="deleteuser"),
    path('register/',views.register ,name="register"),
    path('login/',views.userLogin ,name="login"),
    path('logout/',views.userlogout ,name="logout"),
    path('change_password/',views.change_password ,name="change_password"),
    path('userreporting/',views.userreporting ,name="userreporting"),
    path('scriptreporting/',views.scriptreporting ,name="scriptreporting"),
    path('reportingB2B/',views.reportingB2B ,name="reportingB2B"),
    path('user/',views.userProfile ,name="userProfile"),
    path('configt/<str:pk>',views.routeurConfig1 ,name="configt"),
    path('infoRouteur/<str:pk>',views.infoRouteur ,name="infoRouteur"),
    path('infoportup/<str:pk>',views.infoportup ,name="infoportup"),
    path('infoportdown/<str:pk>',views.infoportdown ,name="infoportdown"),
    path('B2B/<str:pk>',views.B2B ,name="B2B"),
    path('vueG/<str:pk>',views.vueG ,name="vueG"),
    path('ConfigR/<str:pk>',views.ConfigR ,name="ConfigR"),
    path('service/',views.service ,name="service"),
    path('addvrf/',views.addvrf ,name="addvrf"),
    path('delservice/',views.delservice ,name="delservice"),
    path('createswitch/',views.createswitch ,name="createswitch"),



     
]
