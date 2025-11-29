from django.urls import path
from .views import UbicacionView

urlpatterns = [
    path('', UbicacionView.as_view()),
    path('<int:id_ubicacion>/', UbicacionView.as_view()),
]
