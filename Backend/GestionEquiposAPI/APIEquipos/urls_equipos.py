from django.urls import path, re_path
from .views import EquipoView

urlpatterns = [
    path('', EquipoView.as_view()),
    re_path(r'(?P<codigo_inventario>.+)/$', EquipoView.as_view()),
]