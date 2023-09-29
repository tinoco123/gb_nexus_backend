import datetime
import json
import os
from django.http import Http404, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
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
from gb_nexus_backend import renderers

load_dotenv()


@login_required
def search_results(request):
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
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            if request.GET.get("keyword") == "undefined" or int(request.GET.get("keyword")) == 0:
                return JsonResponse({
                    "last_page": 0,
                    "data": []
                })

            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            keyword_id = int(request.GET.get("keyword"))
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))

            keyword = get_object_or_404(Keyword, pk=keyword_id)
            query = keyword.query()
            paginator = Pagination(page_size, query, mongo_client)
            last_page = paginator.calc_last_page()

            if page_number < 0:
                return JsonResponse({"error": "La página solicitada es inválida(Menor a 0)"}, status=400)
            if page_number > last_page:
                if last_page == 0:
                    return JsonResponse({"last_page": 0, "data": [], "error": "Sin resultados de búsqueda  para esta keyword"})

                return JsonResponse({"error": "La página solicitada es mayor a la última disponible"}, status=400)
            if page_size not in (10, 20, 30, 40, 50):
                return JsonResponse({"error": "El tamaño de los resultados de búsqueda debe tener alguno de los siguientes valores: 10, 20, 30, 40, 50"}, status=400)

            documents = paginator.get_page(page_number)
            search_results = [doc for doc in documents]
            data_dict = {
                "last_page": last_page,
                "data": search_results
            }
            return JsonResponse(data_dict, encoder=MongoJSONEncoder)
        except TypeError as e:
            print(e)
            return JsonResponse({"error": "Debes proporcionar los parametros necesarios"}, 400)
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


@login_required
def generate_pdf(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_ids = data.get('selectedIds', [])
            keyword = data.get("keyword", [])

            response_validated_date = validate_data_to_generate_pdf(
                selected_ids, keyword)
            context = get_context_data_pdf(selected_ids, keyword)

            if response_validated_date:
                return response_validated_date
            else:
                response = renderers.render_to_pdf("pdf/report.html", context)
                if response.status_code == 404:
                    raise Http404("Resultados de búsqueda no encontrados")

                filename = f"Reporte-{datetime.date.today()}.pdf"
                content = f"inline; filename={filename}"
                download = request.GET.get("download")
                if download:
                    content = f"attachment; filename={filename}"
                response["Content-Disposition"] = content

                return response

        except json.JSONDecodeError:
            return JsonResponse({'error': 'No se pudieron obtener los IDs seleccionados'}, status=400)
        except InvalidId:
            return HttpResponseBadRequest("El id que solicitaste tiene un formato erroneo")
        except ServerSelectionTimeoutError:
            return HttpResponseServerError("El servidor tardo en retornar una respuesta")
        except ConnectionFailure:
            return HttpResponseServerError("Error en la conexión a la base de datos")
        except OperationFailure:
            return HttpResponseServerError("El servidor fallo en la ejecución de la operación")


def validate_data_to_generate_pdf(selected_ids: list, keyword: str):
    if len(selected_ids) <= 0:
        return JsonResponse({"error": "No seleccionaste ningún documento"}, status=400)
    if len(selected_ids) > 10:
        return JsonResponse({"error": "La cantidad máxima de documentos a exportar es 10"}, status=400)
    if not keyword:
        return JsonResponse({"error": "Se necesita el parametro de keyword"}, status=400)


def get_context_data_pdf(selected_ids: list, keyword: str):
    mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
        os.getenv("MONGODB_COLLECTION")))

    search_result_repo = SearchResultRepository(mongo_client)

    documents_data = []
    context = {"data": documents_data}
    keyword = Keyword.objects.get(pk=int(keyword)).title
    for id in selected_ids:
        document = search_result_repo.get_document_for_pdf(id)
        document["keyword"] = keyword
        documents_data.append(document)

    return context
