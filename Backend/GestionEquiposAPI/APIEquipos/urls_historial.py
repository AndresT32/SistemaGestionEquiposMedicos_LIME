from django.urls import path
from .views import HistorialView

urlpatterns = [
    path('', HistorialView.as_view()),
    path('<str:id_historial>/', HistorialView.as_view()),
]
