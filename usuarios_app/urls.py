from django.urls import path
from . import views

urlpatterns = [
    path("", views.users, name='users'),
    path("create/", views.create_user, name='create_user'),
    path("get/<int:user_id>", views.get_user, name='get_user'),
    path("edit/<int:user_id>", views.edit_user, name="edit_user")
]