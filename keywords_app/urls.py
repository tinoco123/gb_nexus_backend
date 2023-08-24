from django.urls import path
from . import views

urlpatterns = [
    path("", views.keywords, name="keywords"),
    path("data/", views.paginate_keywords, name="paginate_keywords"),
    path("get/<int:keyword_id>", views.get_keyword, name="get_keyword"),
    path("create/", views.create_keyword, name="create_keyword")
]
