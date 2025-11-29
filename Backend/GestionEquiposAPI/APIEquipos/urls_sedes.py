from django.urls import path
from .views import SedeView

urlpatterns = [
    path('', SedeView.as_view()),  # GET all / POST
    path('<str:codigo_sede>/', SedeView.as_view()),  # GET / PUT / DELETE
]
