from django.urls import path,re_path
from .views import EquipoViewDetailed

urlpatterns = [
    path('', EquipoViewDetailed.as_view()),
    re_path(r'(?P<codigo_inventario>.+)/$', EquipoViewDetailed.as_view()),
]