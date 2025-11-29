from django.urls import path
from .views import autocomplete_equipo

urlpatterns = [
    path("equipo/", autocomplete_equipo),  
]
