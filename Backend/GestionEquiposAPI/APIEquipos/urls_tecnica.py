# APIEquipos/urls_tecnica.py

from django.urls import path
from .views import MetrologiaTecnicaView

urlpatterns = [
    path('', MetrologiaTecnicaView.as_view()),                           # GET all, POST
    path('<str:id_metrologia_tecnica>/', MetrologiaTecnicaView.as_view())  # GET one, PUT, DELETE
]
