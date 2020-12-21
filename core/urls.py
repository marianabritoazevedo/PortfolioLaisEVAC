from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('dashboard/paciente', views.dashboard_paciente, name='dashboard_paciente'),
    path('dashboard/profissional', views.dashboard_profissional, name='dashboard_profissional'),
    path('logout/', views.logout, name='logout'),
    path('selecionar_municipio/', views.selecionar_municipio, name='selecionar_municipio'),
    path('selecionar_estabelecimento/<id>/', views.selecionar_estabelecimento, name='selecionar_estabelecimento'),
    path('agendar_vacinacao/<id>/', views.agendar_vacinacao, name='agendar_vacinacao'),
    path('profissional_registro_data', views.profissional_registro_data, name='profissional_registro_data'),
    path('registrar_vacina', views.registrar_vacina, name='registrar_vacina'),
    path('estoque', views.estoque, name='estoque'),
    path('dashboard/coord', views.dashboard_coord, name='dashboard_coord'),
]