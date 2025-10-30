from django.urls import path
from .views import attempt_view

urlpatterns = [
    path('attempt/', attempt_view, name="attempt"),
]