from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_enquetes, name='listar_enquetes'),
    path('enquete/<int:enquete_id>/', views.responder_enquete, name='responder_enquete'),
    path('enquete/<int:enquete_id>/respondida/', views.enquete_respondida, name='enquete_respondida'),
    path('enquete/<int:enquete_id>/resultados/', views.exibir_resultados, name='exibir_resultados'),
]