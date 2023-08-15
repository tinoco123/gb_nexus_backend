from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients, name="clients"),
    path("data/", views.all_clients, name="all_clients")
]