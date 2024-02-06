from datetime import datetime
from io import BytesIO
import os, traceback, logging, PyPDF2
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
    logging.basicConfig(filename='scripts/mails.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    clientes = get_clients_with_mail_on()
    logging.info(f"{clientes.count()} clientes con mails para hoy")
    for cliente in clientes:
        try:
            client_email = cliente.email
            logging.info(f"Cliente: {client_email}")
            mail_frequency = cliente.mail_frequency
            today_date = timezone.now().date()
            last_mail_date = today_date - timedelta(days=mail_frequency)

            start_date = datetime.combine(last_mail_date, datetime.min.time())
            end_date = datetime.combine(today_date, datetime.min.time())

            keywords = get_keywords_with_mail_on(cliente)
            keywords_count = keywords.count()
            logging.info(f"{client_email} tiene {keywords_count} keywords activas")
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
                    logging.info(f"Keyword {keyword_title} de {client_email} sin resultados en periodo del {start_date} al {end_date}")
                    continue
                logging.info(f"Keyword {keyword_title} de {client_email} con resultados")
                pdf = renderers.render_to_pdf("pdf/report.html", context)
                pdf_size = BytesIO(pdf.content).getbuffer().nbytes
                if pdf_size + pdfs_size > 10000000:  # 10MB
                    logging.info(f"Keyword {keyword_title} de {client_email} supero tamaño de 10MB")
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
                    client_email, today_date, cliente.first_name, start_date, end_date, keywords_list, pdf_to_attach, pdf_size_limit_passed)

                notification_mail.send(fail_silently=False)
                logging.info(f"Mail enviado a {client_email} con {len(pdfs_to_merge)} pdfs unidos de {keywords_count} keywords")
            else:
                logging.info(f"Sin mail que mandar a {client_email} con {keywords_count} keywords activas")
        except Exception as ex:
            print(ex)
            logging.info(f"{traceback.print_exc()}")
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
        attached_message = "Le informamos que sus búsquedas fueron limitadas para evitar que su reporte superara el límite de peso de 10 MB. Por lo cual, le sugerimos que ingrese al sistema COMPASS(<a href='http://compass.globalnexusdc.com/'>compass.globalnexusdc.com</a>) y revise más resultados de sus búsquedas requeridas."
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
