from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients, name="clients"),
    path("create/", views.create_client, name="create_client"),
    path("get/<int:client_id>", views.get_client, name="get_client"),
    path("edit/<int:client_id>", views.edit_client, name="edit_client"),
    path("delete/<int:client_id>", views.delete_client, name="delete_client"),
    path("mail-frequency/", views.set_mail_frequency, name="mail_frequency"),
    path("data/", views.paginate_clients, name="paginate_clients"),
]