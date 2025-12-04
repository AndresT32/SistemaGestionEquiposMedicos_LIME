from django.urls import path, re_path
from . import views 

urlpatterns = [
    # Ruta raíz (Buscar)
    path('', views.EquipoView.as_view()),

    # IMPORTANTE: Llamamos a 'EquipoViewDetailed' porque ahí está el método PUT
    re_path(r'(?P<codigo_inventario>.+)/$', views.EquipoViewDetailed.as_view()),
]

