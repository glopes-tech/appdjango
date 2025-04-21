from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('enquetes/', views.listar_enquetes, name='listar_enquetes'),
    path('enquete/<int:enquete_id>/', views.responder_enquete, name='responder_enquete'),
    path('enquete/<int:enquete_id>/respondida/', views.enquete_respondida, name='enquete_respondida'),
    path('enquete/<int:enquete_id>/resultados/', views.exibir_resultados, name='exibir_resultados'),

    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/<int:aluno_id>/', views.detalhar_aluno, name='detalhar_aluno'),

    path('areas-interesse/', views.listar_areas_interesse, name='listar_areas_interesse'),
    path('areas-interesse/<int:area_id>/', views.detalhar_area_interesse, name='detalhar_area_interesse'),

    path('interesses/', views.listar_interesses_alunos, name='listar_interesses_alunos'),
    path('interesses/<int:interesse_id>/', views.detalhar_interesse_aluno, name='detalhar_interesse_aluno'),
]