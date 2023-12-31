from django.urls import path
from . import views

urlpatterns = [
    path("", views.keywords, name="keywords"),
    path("data/", views.paginate_keywords, name="paginate_keywords"),
    path("get/<int:keyword_id>", views.get_keyword, name="get_keyword"),
    path("get/searchterms/<int:keyword_id>", views.get_search_terms, name="get_search_terms"),
    path("get/user-information/<int:keyword_id>", views.get_user_information, name="get_user_information"),
    path("edit/<int:keyword_id>", views.edit_keyword, name="edit_keyword"),
    path("delete/<int:keyword_id>", views.delete_keyword, name="delete_keyword"),
    path("create/", views.create_keyword, name="create_keyword"),
]
