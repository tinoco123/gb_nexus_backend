from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients, name="clients"),
    path("create/", views.create_client, name="create_client"),
    path("data/", views.paginate_clients, name="paginate_clients"),
    path("data/all-clients", views.all_clients, name="all_clients")
]