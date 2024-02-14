from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_results, name='search_results'),
    path("data/", views.get_page_of_search_results, name='get_page_search_results'),
    path("data/get/<str:id>", views.get_search_result_by_id, name='get_search_result_by_id'),
    path("data/get-pdf/<str:id>", views.get_pdf_of_dof_document, name='generate_pdf_dof'),
    path("generate-pdf/", views.generate_pdf, name='generate_pdf'),
    path("send-mail/", views.send_mail, name='send_mail')
]