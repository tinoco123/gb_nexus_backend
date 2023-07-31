import os
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mongo_connection.paginator import Pagination
from dotenv import load_dotenv
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, ConnectionFailure
from .utils import MongoJSONEncoder

load_dotenv()


@login_required
def search_results(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        return render(request, "search_results.html")


@login_required
def get_page_of_search_results(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))
        except ValueError:
            return HttpResponseBadRequest()
 
        if page_number >= 1 and page_size <= 50:
            try:
                paginator = Pagination(page_size, str(os.getenv("MONGODB_DATABASE")), str(
                    os.getenv("MONGODB_COLLECTION")))
                last_page = paginator.last_page
                documents = paginator.get_page(page_number)
                search_results = [doc for doc in documents]
                data_dict = {
                    "last_page": last_page,
                    "data": search_results
                }
                return JsonResponse(data_dict, encoder=MongoJSONEncoder)
            except ServerSelectionTimeoutError as e:
                return HttpResponseServerError()
            except ConnectionFailure as e:
                return HttpResponseServerError()
            except OperationFailure as e:
                return HttpResponseServerError()
        else:
            return HttpResponseBadRequest()
