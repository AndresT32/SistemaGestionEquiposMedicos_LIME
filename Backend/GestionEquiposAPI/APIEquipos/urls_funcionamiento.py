from django.urls import path
from .views import CondicionesFuncionamientoView

urlpatterns = [
    path('', CondicionesFuncionamientoView.as_view()),
    path('<str:id_condiciones>/', CondicionesFuncionamientoView.as_view()),
]
