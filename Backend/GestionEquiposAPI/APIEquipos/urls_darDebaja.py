from django.urls import path
from . import views

urlpatterns = [
    path('equipo/<path:codigo_inventario>/dar_baja/', views.dar_baja_equipo),
    # --- NUEVA URL PARA ACTIVAR ---
    path('equipo/<path:codigo_inventario>/reactivar/', views.reactivar_equipo),
]