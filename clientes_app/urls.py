from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients, name="clients"),
    path("data/", views.paginate_clients, name="paginate_clients"),
    path("data/all-clients", views.all_clients, name="all_clients")
]