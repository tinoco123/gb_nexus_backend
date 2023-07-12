from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.users, name='users'),
    path("create_user/", views.create_user, name='create_user'),
]