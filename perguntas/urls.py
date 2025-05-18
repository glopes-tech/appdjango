from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enquetes/', views.gerenciar_enquetes, name='gerenciar_enquetes'),
    path('enquetes/criar/', views.EnqueteCreateView.as_view(), name='criar_enquete'),
    path('enquetes/<int:pk>/editar/', views.EnqueteUpdateView.as_view(), name='editar_enquete'),
    path('enquetes/<int:pk>/detalhar/', views.EnqueteDetailView.as_view(), name='detalhar_enquete'),
    path('enquetes/', views.EnqueteListView.as_view(), name='listar_enquetes'),
    path('enquetes/<int:pk>/deletar/', views.EnqueteDeleteView.as_view(), name='deletar_enquete'),
    path('enquete/<int:enquete_id>/responder/', views.responder_enquete, name='responder_enquete'),
    path('enquete/respondida/', views.enquete_respondida, name='enquete_respondida'),
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/registrar/', views.registrar_aluno, name='registrar_aluno'),
#    path('admin/criar-enquete/', views.criar_enquete, name='admin_criar_enquete'),
    path('areas-interesse/', views.listar_areas_interesse, name='listar_areas_interesse'),
    path('admin/', admin.site.urls),
]
