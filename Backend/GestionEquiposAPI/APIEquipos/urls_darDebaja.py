from django.urls import path
from .views import dar_baja_equipo

urlpatterns = [
    path("equipo/<str:codigo_inventario>/dar_baja/", dar_baja_equipo),
]
