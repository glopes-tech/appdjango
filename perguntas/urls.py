from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enquetes/', views.gerenciar_enquetes, name='gerenciar_enquetes'),
    path('enquetes/gerenciar/', views.gerenciar_enquetes, name='enquetes/gerenciar_enquetes'),
    path('enquete/<int:enquete_id>/responder/', views.responder_enquete, name='responder_enquete'),
    path('enquete/respondida/', views.enquete_respondida, name='enquete_respondida'),
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/registrar/', views.registrar_aluno, name='registrar_aluno'),
    path('admin/criar-enquete/', views.criar_enquete, name='admin_criar_enquete'),
    path('areas-interesse/', views.listar_areas_interesse, name='listar_areas_interesse'),
    path('admin/', admin.site.urls),
]
