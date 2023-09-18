from django.urls import path
from . import views

urlpatterns = [
    path("", views.users, name='users'),
    path("create/", views.create_user, name='create_user'),
    path("get/<int:user_id>", views.get_user, name='get_user'),
    path("edit/<int:user_id>", views.edit_user, name="edit_user"),
    path("delete/<int:user_id>", views.delete_user, name="delete_user"),
    path("data/", views.paginate_users, name="paginate_users")
]