from django.urls import path
from . import views

urlpatterns = [
    path("", views.keywords, name="keywords"),
    path("create/", views.create_keyword, name="create_keyword")
]