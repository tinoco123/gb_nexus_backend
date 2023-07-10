from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.users, name='users'),
    path("get_users/", views.get_users, name='get_users'),

]