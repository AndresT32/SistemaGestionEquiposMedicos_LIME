from django.urls import path
from .views_estadisticas import estadisticas_generales, catalogos_filtros

urlpatterns = [
    path("estadisticas/", estadisticas_generales),
    path("catalogos/", catalogos_filtros),
]
