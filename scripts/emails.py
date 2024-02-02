from datetime import datetime
from io import BytesIO
import os

import PyPDF2
from gb_nexus_backend import renderers
from keywords_app.models import Keyword
from resultados_busqueda_app.utils import resaltar_keywords, change_title_label, create_mail
from mongo_connection.connection import MongoConnection
from mongo_connection.search_result_repository import SearchResultRepository
from tipos_usuarios.models import Cliente
from django.utils import timezone
from datetime import timedelta
from django.db.models.manager import BaseManager
from pymongo.errors import OperationFailure, PyMongoError


def run():
    clientes = get_clients_with_mail_on()

    for cliente in clientes:
        try:
            mail_frequency = cliente.mail_frequency
            today_date = timezone.now().date()
            last_mail_date = today_date - timedelta(days=mail_frequency)

            start_date = datetime.combine(last_mail_date, datetime.min.time())
            end_date = datetime.combine(today_date, datetime.min.time())

            keywords = get_keywords_with_mail_on(cliente)
            pdfs_to_merge = []
            keywords_list = []
            pdfs_size = 0
            pdf_size_limit_passed = False
            for keyword in keywords:
                keyword_query = keyword.query()
                # time range to search information
                if keyword.start_date or keyword.end_date:
                    keyword_query["$and"][-1]["date"] = {
                        '$gte': start_date, '$lte': end_date}
                else:
                    keyword_query['$and'].append(
                        {"date": {'$gte': start_date, '$lte': end_date}})

                keyword_title = keyword.title
                subkeywords = list(keyword.searchterms_set.values_list("name", flat=True))
                
                context = get_context_for_pdf(keyword_query, keyword_title, subkeywords)
                if context is None:
                    continue
                pdf = renderers.render_to_pdf("pdf/report.html", context)
                pdf_size = BytesIO(pdf.content).getbuffer().nbytes
                if pdf_size + pdfs_size > 10000000:  # 10MB
                    pdf_size_limit_passed = True
                    break
                pdfs_size += pdf_size
                keywords_list.append({"title": keyword_title, "subkeywords": subkeywords})
                pdfs_to_merge.append(pdf)
            if len(pdfs_to_merge) >= 1:
                merged_pdf = merge_pdfs(pdfs_to_merge)                
                pdf_to_attach = {
                    "filename": f"Reporte-{today_date.strftime('%Y-%m-%d')}", "content": merged_pdf, "mimetype": "application/pdf"}
                notification_mail = create_notification_mail(
                    cliente.email, today_date, cliente.first_name, start_date, end_date, keywords_list, pdf_to_attach, pdf_size_limit_passed)

                notification_mail.send(fail_silently=False)
        except Exception as ex:
            print(ex)
            continue
        finally:
            cliente.next_mail = today_date + timedelta(days=mail_frequency)  # Next mail
            cliente.save()
                


def get_clients_with_mail_on() -> BaseManager[Cliente]:
    clientes = Cliente.objects.filter(
        is_active=True, next_mail=timezone.now().date())
    return clientes


def get_keywords_with_mail_on(client: Cliente) -> BaseManager[Keyword]:
    keywords = client.keyword_set.filter(is_mail_active=True)
    return keywords


def get_context_for_pdf(query: dict, keyword_title: str, subkeywords: list[str]) -> dict:
    try:
        mongo_client = MongoConnection(str(os.getenv("MONGODB_DATABASE")), str(
            os.getenv("MONGODB_COLLECTION")))
        search_result_repository = SearchResultRepository(mongo_client)
        search_results_found = search_result_repository.get_document_for_pdf_optimized(
            query)
        search_results_to_show = []
        context = {"data": search_results_to_show}
        for search_result in search_results_found:
            change_title_label(search_result)
            hightlighted_sinopsys = resaltar_keywords(
                subkeywords, search_result["sinopsys"])
            search_result["sinopsys"] = hightlighted_sinopsys
            if search_result["urlAttach"] is not None:
                for attachment in search_result["urlAttach"]:
                    attachment["sinopsys"] = resaltar_keywords(
                        subkeywords, attachment["sinopsys"])
            search_result["keyword"] = keyword_title
            search_results_to_show.append(search_result)
        if len(search_results_to_show) >= 1:
            return context
        else:
            return None        
    except OperationFailure as ex:
        print(ex)
        return None 
    except PyMongoError as ex:
        print(ex)
        return None
    


def merge_pdfs(pdf_list):
    merger = PyPDF2.PdfMerger()

    for pdf_data in pdf_list:
        pdf_buffer = BytesIO(pdf_data.content)        
        merger.append(pdf_buffer)

    merged_result = BytesIO()
    merger.write(merged_result)

    return merged_result.getvalue()


def create_notification_mail(recipient, today_date, first_name, initial_date, final_date, keywords_list: list[dict], pdf, pdf_size_limit_passed: bool):
    if pdf_size_limit_passed: 
        attached_message = "Le informamos que sus búsquedas fueron limitadas para evitar que su reporte superara el límite de peso de 10 MB. Por lo cual, le sugerimos que ingrese al sistema COMPASS y revise los resultados que no se pueden observar en este reporte adjunto."
    else:
        attached_message = "Los resultados de las búsquedas podrán encontrarla en los documentos PDFs anexos."
    subject = f"COMPASS: Resultados de búsqueda del {today_date.strftime('%Y-%m-%d')}"
    context = {
        "username": first_name,
        "keywords": keywords_list,
        "initial_date": initial_date.strftime("%Y-%m-%d"),
        "final_date": final_date.strftime("%Y-%m-%d"),
        "attached_message": attached_message
    }
    email = create_mail(recipient, subject, context,
                        "mails/many_search_results.html", [pdf])
    return email
