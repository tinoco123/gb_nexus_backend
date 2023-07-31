import os
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mongo_connection.paginator import Pagination
from dotenv import load_dotenv
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, ConnectionFailure
from bson.errors import InvalidId
from .utils import MongoJSONEncoder
from mongo_connection.connection import MongoConnection
from mongo_connection.search_result_repository import SearchResultRepository

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


@login_required
def get_search_result_by_id(request, id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            search_result_repo = SearchResultRepository(mongo_client)
            search_result = search_result_repo.get_by_id(id)
            if search_result:
                return JsonResponse(search_result, encoder=MongoJSONEncoder)
            else:
                return HttpResponseBadRequest("No se encontró el elemento solicitado")
        except InvalidId:
            return HttpResponseBadRequest("El id que solicitaste tiene un formato erroneo")
        except ServerSelectionTimeoutError:
            return HttpResponseServerError("El servidor tardo en retornar una respuesta")
        except ConnectionFailure:
            return HttpResponseServerError("Error en la conexión a la base de datos")
        except OperationFailure:
            return HttpResponseServerError("El servidor fallo en la ejecución de la operación")
