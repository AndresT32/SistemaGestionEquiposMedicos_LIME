from django.urls import path
from .views import RegistroActividadesView

urlpatterns = [
    path('', RegistroActividadesView.as_view()),
    path('<str:id_registro>/', RegistroActividadesView.as_view()),
]
