from django.urls import path
from .views import MetrologiaAdministrativaView

urlpatterns = [
    path('', MetrologiaAdministrativaView.as_view()),
    path('<str:id_metrologia_adm>/', MetrologiaAdministrativaView.as_view()),
]
