from django.contrib import admin
from django.urls import path, include
from perguntas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('perguntas.urls')),
]