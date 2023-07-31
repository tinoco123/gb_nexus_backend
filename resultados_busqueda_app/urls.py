from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_results, name='search_results'),
    path("data/", views.get_page_of_search_results, name='get_page_search_results')
]