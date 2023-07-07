from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.list_users, name='list_users'),
]