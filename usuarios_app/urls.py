from django.urls import path
from . import views

urlpatterns = [
    path("", views.users, name='users'),
    path("create/", views.create_user, name='create_user'),
]