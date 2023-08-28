import os
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from mongo_connection.paginator import Pagination
from dotenv import load_dotenv
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, ConnectionFailure
from bson.errors import InvalidId
from .utils import MongoJSONEncoder
from mongo_connection.connection import MongoConnection
from mongo_connection.search_result_repository import SearchResultRepository
from keywords_app.models import Keyword
from tipos_usuarios.models import UserBaseAccount


load_dotenv()


@login_required
def search_results(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        user = get_object_or_404(UserBaseAccount, pk=request.user.id)
        if request.user.user_type == "ADMINISTRADOR":
            keyword_list = Keyword.objects.all()
        else:
            keyword_list = Keyword.objects.filter(user=user)
        return render(request, "search_results.html", {"keyword_list": keyword_list})


@login_required
def get_page_of_search_results(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            if request.GET.get("keyword") == "undefined":
                return JsonResponse({
                    "last_page": 0,
                    "data": []
                })

            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            keyword_id = int(request.GET.get("keyword"))
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))

            keyword = Keyword.objects.get(pk=keyword_id)
            if keyword is None:
                return JsonResponse({"error": "La keyword solicitada no se encuentra registrada en el sistema"}, status=404)
            query = keyword.query()
            paginator = Pagination(page_size, query, mongo_client)
            last_page = paginator.calc_last_page()
            print(last_page)
            if page_number < 1 or page_number > last_page:
                return HttpResponseBadRequest("La página solicitada es menor a 1 o mayor a la última pagina disponible")
            if page_size not in (10, 20, 30, 40, 50):
                return HttpResponseBadRequest("El tamaño de los resultados de búsqueda debe tener alguno de los siguientes valores: 10, 20, 30, 40, 50")

            documents = paginator.get_page(page_number)
            search_results = [doc for doc in documents]
            data_dict = {
                "last_page": last_page,
                "data": search_results
            }
            return JsonResponse(data_dict, encoder=MongoJSONEncoder)
        except TypeError as e:
            print(e)
            return HttpResponseBadRequest("Debes proporcionar los parametros necesarios")
        except ValueError as e:
            print(e)
            return HttpResponseBadRequest()
        except ServerSelectionTimeoutError as e:
            print(e)
            return HttpResponseServerError()
        except ConnectionFailure as e:
            print(e)
            return HttpResponseServerError()
        except OperationFailure as e:
            print(e)
            return HttpResponseServerError()


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
