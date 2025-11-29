# APIEquipos/urls_descargar.py

from django.urls import path
from . import views

urlpatterns = [
    # 🚨 CAMBIO DE <str:codigo_inventario> A <path:codigo_inventario> 🚨
    path('<path:codigo_inventario>/', views.descargar_equipo_xlsx, name='descargar_equipo_xlsx'),
]