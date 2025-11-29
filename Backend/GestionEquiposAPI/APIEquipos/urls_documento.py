from django.urls import path
from .views import DocumentoView

urlpatterns = [
    path('', DocumentoView.as_view()),
    path('<str:id_documento>/', DocumentoView.as_view()),
]
