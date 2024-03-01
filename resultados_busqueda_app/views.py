import threading
import traceback
import json
import os
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from mongo_connection.paginator import Pagination
from dotenv import load_dotenv
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, ConnectionFailure
from bson.errors import InvalidId
from .utils import MongoJSONEncoder, resaltar_keywords, change_title_labels, change_title_label, create_mail, conver_base64_to_bytes, mexico_states_dict
from mongo_connection.connection import MongoConnection
from mongo_connection.search_result_repository import SearchResultRepository
from keywords_app.models import Keyword
from gb_nexus_backend import renderers
from gb_nexus_backend.decorators import terms_accepted_required

load_dotenv()


@login_required
@terms_accepted_required
def search_results(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        return render(request, "search_results.html")


@login_required
@terms_accepted_required
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

            if page_size not in (20, 30, 40, 50):
                return JsonResponse({"error": "El tamaño de los resultados de búsqueda debe tener alguno de los siguientes valores: 20, 30, 40, 50"}, status=400)

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

            documents = paginator.get_page(page_number)
            search_results = [doc for doc in documents]
            change_title_labels(search_results)
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
@terms_accepted_required
def get_search_result_by_id(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            keyword_id = int(request.GET.get("keyword"))
            keyword = get_object_or_404(Keyword, pk=keyword_id)
            subkeywords = list(
                keyword.searchterms_set.values_list("name", flat=True))
            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            search_result_repo = SearchResultRepository(mongo_client)
            search_result = search_result_repo.get_by_id(id, subkeywords[0])

            if search_result:
                keyword_id = int(request.GET.get("keyword"))
                keyword = get_object_or_404(Keyword, pk=keyword_id)
                subkeywords = list(
                    keyword.searchterms_set.values_list("name", flat=True))

                if search_result["sinopsys"] in ("na", "N/A"):
                    collection_name = search_result["collectionName"]
                    search_result["sinopsys"] = mexico_states_dict[collection_name]
                else:
                    search_result["sinopsys"] = resaltar_keywords(
                        subkeywords, search_result["sinopsys"])

                if search_result.get("urlAttach") is not None:
                    if len(search_result["urlAttach"]) >= 1:
                        first_attachment_url = search_result["urlAttach"][0]["urlAttach"]
                        search_result["firstUrl"] = first_attachment_url

                        attachments_with_sinopsys = list(filter(lambda attachment: attachment["sinopsys"] != "",
                                                                search_result["urlAttach"]))

                        attachments_with_bold_sinopsys = list(map(lambda attachment: {
                            **attachment, "sinopsys": resaltar_keywords(subkeywords, attachment["sinopsys"])}, attachments_with_sinopsys))

                        search_result["urlAttach"] = attachments_with_bold_sinopsys

                return JsonResponse(search_result, encoder=MongoJSONEncoder)
            else:
                return HttpResponseBadRequest("No se encontró el elemento solicitado")
        except KeyError as ex:
            print(ex)
            return JsonResponse(search_result, encoder=MongoJSONEncoder)
        except InvalidId as ex:
            print(ex)
            return HttpResponseBadRequest("El id que solicitaste tiene un formato erroneo")
        except ValueError as ex:
            print(ex)
            return HttpResponseBadRequest("Id de keyword no valido")
        except ServerSelectionTimeoutError as ex:
            print(ex)
            return HttpResponseServerError("El servidor tardo en retornar una respuesta")
        except ConnectionFailure as ex:
            print(ex)
            return HttpResponseServerError("Error en la conexión a la base de datos")
        except OperationFailure as ex:
            print(ex)
            return HttpResponseServerError("El servidor fallo en la ejecución de la operación")


@login_required
@terms_accepted_required
def get_pdf_of_dof_document(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            search_result_repo = SearchResultRepository(mongo_client)
            base64_string = search_result_repo.get_base_64_string(id)
            pdf_bytes = conver_base64_to_bytes(base64_string)
            return HttpResponse(content=pdf_bytes, content_type='application/pdf')
        except TypeError:
            return JsonResponse({"error": "El documento no se puede convertir a pdf"}, status=500)
        except ValueError:
            return JsonResponse({"error": "El documento no se puede convertir a pdf"}, status=500)
        except InvalidId:
            return JsonResponse({"error": "Documento con identificador invalido"}, status=400)
        except ServerSelectionTimeoutError:
            return JsonResponse({"error": "El servidor tardo en retornar una respuesta"}, status=500)
        except ConnectionFailure:
            return JsonResponse({"error": "Error en la conexión a la base de datos"}, status=500)
        except OperationFailure:
            return JsonResponse({"error": "El servidor fallo en la ejecución de la operación"}, status=500)


@login_required
@terms_accepted_required
def get_doc_sinopsys_from_dof_collection(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
                os.getenv("MONGODB_COLLECTION")))
            search_result_repo = SearchResultRepository(mongo_client)

            sinopsys = search_result_repo.get_doc_sinopsys_from_dof_collection(
                id)
            if sinopsys:
                keyword_id = int(request.GET.get("keyword"))
                keyword = get_object_or_404(Keyword, pk=keyword_id)
                subkeywords = list(
                    keyword.searchterms_set.values_list("name", flat=True))
                sinopsys = resaltar_keywords(subkeywords, sinopsys)
            return JsonResponse({"sinopsys": sinopsys}, status=200)
        except InvalidId:
            return JsonResponse({"error": "Documento con identificador invalido"}, status=400)
        except ServerSelectionTimeoutError:
            return JsonResponse({"error": "El servidor tardo en retornar una respuesta"}, status=500)
        except ConnectionFailure:
            return JsonResponse({"error": "Error en la conexión a la base de datos"}, status=500)
        except OperationFailure:
            return JsonResponse({"error": "El servidor fallo en la ejecución de la operación"}, status=500)


@login_required
@terms_accepted_required
def generate_pdf(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_ids = data.get('selected_ids', [])
            keyword = data.get("keyword", [])
            response_validated_date = validate_data_to_generate_pdf(
                selected_ids, keyword)
            if response_validated_date:
                return response_validated_date
            else:
                context = get_context_data_pdf(selected_ids, keyword)
                response = renderers.render_to_pdf("pdf/report.html", context)
                if response.status_code == 404:
                    raise Http404("Resultados de búsqueda no encontrados")

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

    keyword = Keyword.objects.get(pk=int(keyword))
    keyword_title = keyword.title
    subkeywords = list(keyword.searchterms_set.values_list("name", flat=True))

    for id in selected_ids:
        document = search_result_repo.get_document_for_pdf(id)
        if not document:
            continue
        change_title_label(document)
        hightlighted_sinopsys = resaltar_keywords(
            subkeywords, document["sinopsys"])
        document["sinopsys"] = hightlighted_sinopsys
        if document["urlAttach"]:
            for attachment in document["urlAttach"]:
                attachment["sinopsys"] = resaltar_keywords(
                    subkeywords, attachment["sinopsys"])
        document["keyword"] = keyword_title
        documents_data.append(document)
    return context


def send_search_results_mail(request, keyword_id, recipient_list):
    keyword = get_object_or_404(Keyword, id=int(keyword_id))
    keyword_title = keyword.title
    subkeywords = list(keyword.searchterms_set.values_list("name", flat=True))

    pdf = {"filename": f"{keyword_title}", "content": generate_pdf(
        request).content, "mimetype": "application/pdf"}

    recipient = recipient_list if len(recipient_list) >= 1 else [
        request.user.email]
    context = {
        "username": "" if len(recipient_list) >= 1 else request.user.first_name,
        "keyword_title": keyword_title,
        "subkeywords": subkeywords
    }
    mail = create_mail(
        recipient, f"Resultados de búsqueda de Compass - Keyword: {keyword_title}", context, "mails/search_results.html", [pdf])

    mail.send(fail_silently=False)


@login_required
@terms_accepted_required
def send_mail(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_ids = data.get('selected_ids', [])
            keyword_id = data.get("keyword", [])
            recipient_list = data.get('recipient_list', [])

            error_in_input_data = validate_data_to_generate_pdf(
                selected_ids, keyword_id)
            if error_in_input_data:
                return error_in_input_data

            thread = threading.Thread(
                target=send_search_results_mail(request, keyword_id, recipient_list))
            thread.start()
            return JsonResponse({}, status=200)
        except Exception as ex:
            print(ex)
            return JsonResponse({"error": traceback.format_exc()}, status=400)
