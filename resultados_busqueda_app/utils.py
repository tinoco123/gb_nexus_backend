import json
from bson import ObjectId
from datetime import datetime, date
import re
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self, o)


def resaltar_keywords(keywords: list, sinopsys: str):
    sinopsys_resaltada = sinopsys.capitalize()

    def reemplazar(match):
        return f"<strong>{match.group()}</strong>"
    for keyword in keywords:
        sinopsys_resaltada = re.sub(
            r'\b' + re.escape(keyword.lower()) + r'\b', reemplazar, sinopsys_resaltada, flags=re.IGNORECASE)
    return sinopsys_resaltada


def change_title_labels(search_results: list):
    for search_result in search_results:
        try:
            title = search_result["title"]
            collection_name = search_result["collectionName"]
            if is_common_title(title) or collection_name == "OaxacaDictamen":
                search_result["title"] = mexico_states_dict[collection_name]
        except KeyError:
            continue


def change_title_label(search_result: dict):
    try:
        title = search_result["title"]
        collection_name = search_result["collectionName"]
        if is_common_title(title) or collection_name == "OaxacaDictamen":
            search_result["title"] = mexico_states_dict[collection_name]
    except KeyError:
        return


common_titles = ["na", "-", "n/a", "descarga la gaceta",
                 "orden del", "lista de ejemplares"]


def is_common_title(title: str):
    for common_title in common_titles:
        patron = r"\b" + common_title + r"\b" if common_title != '-' else re.escape(common_title)
        match = re.search(patron, title, re.IGNORECASE)
        if match:
            return True
    else:
        return False


def create_mail(recipient_list: list, subject: str, context: dict, template_path: str, attachments: list[dict]):
    template = get_template(template_path)
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=f"COMPASS <{settings.EMAIL_HOST_USERNAME}>",
        to=recipient_list
    )
    mail.attach_alternative(content, "text/html")

    for attachment in attachments:
        mail.attach(attachment["filename"],
                    attachment["content"], attachment["mimetype"])

    return mail

mexico_states_dict = {
    'BCNComunicacion': 'Congreso de Baja California Norte',
    'BCNDictamenes': 'Congreso de Baja California Norte',
    'BCNGaceta': 'Congreso de Baja California Norte',
    'BCNIniciativa': 'Congreso de Baja California Norte',
    'BCNPeriodicoOficial': 'Diario Oficial de Baja California Norte',
    'BCSComunicacion': 'Congreso de Baja California Sur',
    'BCSPeriodicoOficial': 'Diario Oficial de Baja California Sur',
    'CdmxComunicacion': 'Congreso de la Ciudad de México',
    'CdmxGaceta': 'Congreso de la Ciudad de México',
    'CdmxIniciativa': 'Congreso de la Ciudad de México',
    'ChiapasGaceta': 'Congreso de Chiapas',
    'ChiapasSesiones': 'Congreso de Chiapas',
    'ChihuahuaComunicacion': 'Congreso de Chihuahua',
    'ChihuahuaPeriodicoOficial': 'Diario Oficial de Chihuahua',
    'CoahuilaComunicacion': 'Congreso de Coahuila',
    'CoahuilaGaceta': 'Congreso de Coahuila',
    'CoahuilaIniciativa': 'Congreso de Coahuila',
    'CoahuilaPeriodicoOficial': 'Diario Oficial de Coahuila',
    'ColimaComunicacion': 'Congreso de Colima',
    'ColimaDictamen': 'Congreso de Colima',
    'ColimaGaceta': 'Congreso de Colima',
    'ColimaIniciativa': 'Congreso de Colima',
    'ColimaPeriodicoOficial': 'Diario Oficial de Colima',
    'CongresoDurangoComunicacion': 'Congreso de Durango',
    'DurangoComunicacion': 'Congreso de Durango',
    'DurangoPeriodicoOficial': 'Diario Oficial de Durango',
    'EdomexGaceta': 'Congreso del Estado de México',
    'EdomexPeriodicoOficial': 'Diario Oficial del Estado de México',
    'GuanajuatoIniciativa': 'Congreso de Guanajuato',
    'GuanajuatoComunicacion': 'Congreso de Guanajuato',
    'GuanajuatoCongreso': 'Congreso de Guanajuato',
    'GuanajuatoGaceta': 'Congreso de Guanajuato',
    'GuanajuatoPeriodico': 'Diario Oficial de Guanajuato',
    'GuerreroCongresoComunicacion': 'Congreso de Guerrero',
    'GuerreroCongresoOrdenDia': 'Congreso de Guerrero',
    'GuerreroPeriodicoOficial': 'Diario Oficial de Guerrero',
    'HidalgoCongreso': 'Congreso de Hidalgo',
    'HidalgoPeriodicoOficial': 'Diario Oficial de Hidalgo',
    'JaliscoComunicacion': 'Congreso de Jalisco',
    'JaliscoPeriodicoOficial': 'Diario Oficial de Jalisco',
    'MichoacanComunicacion': 'Congreso de Michoacán',
    'MichoacanGaceta': 'Congreso de Michoacán',
    'MichoacanIniciativa': 'Congreso de Michoacán',
    'MichoacanPeriodicoOficial': 'Diario Oficial de Michoacán',
    'MorelosPeriodico': 'Diario Oficial de Morelos',
    'NLComunicacion': 'Congreso de Nuevo León',
    'NLGaceta': 'Congreso de Nuevo León',
    'NLIniciativa': 'Congreso de Nuevo León',
    'NLPeriodicoOficial': 'Diario Oficial de Nuevo León',
    'NayaritComunicacion': 'Congreso de Nayarit',
    'NayaritGaceta': 'Congreso de Nayarit',
    'NayaritIniciativa': 'Congreso de Nayarit',
    'NayaritPeriodicoOficial': 'Diario Oficial de Nayarit',
    'OaxacaPeriodicoOficial': 'Diario Oficial de Oaxaca',
    'OaxacaDictamen': 'Congreso de Oaxaca',
    'OaxacaGaceta': 'Congreso de Oaxaca',
    'OaxacaIniciativa': 'Congreso de Oaxaca',
    'PueblaComunicacion': 'Congreso de Puebla',
    'PueblaGaceta': 'Congreso de Puebla',
    'PueblaIniciativa': 'Congreso de Puebla',
    'PueblaPeriodicoOficial': 'Diario Oficial de Puebla',
    'QRooGaceta': 'Congreso de Quintana Roo',
    'QRooIniciativa': 'Congreso de Quintana Roo',
    'QRooPeriodicoOficial': 'Diario Oficial de Quintana Roo',
    'QueretaroComunicacion': 'Congreso de Querétaro',
    'QueretaroGaceta': 'Congreso de Querétaro',
    'QueretaroIniciativa': 'Congreso de Querétaro',
    'SanLuisPotosiCongreso': 'Congreso de San Luis Potosí',
    'SanLuisPotosiCongresoNoticias': 'Congreso de San Luis Potosí',
    'SinaloaComunicacion': 'Congreso de Sinaloa',
    'SinaloaDictamenes': 'Congreso de Sinaloa',
    'SinaloaGaceta': 'Congreso de Sinaloa',
    'SinaloaIniciativa': 'Congreso de Sinaloa',
    'SinaloaPeriodicoOficial': 'Diario Oficial de Sinaloa',
    'SonoraComunicacion': 'Congreso de Sonora',
    'SonoraGaceta': 'Congreso de Sonora',
    'SonoraIniciativa': 'Congreso de Sonora',
    'SonoraPeriodicoOficial': 'Diario Oficial de Sonora',
    'TabascoComunicacion': 'Congreso de Tabasco',
    'TabascoDictamen': 'Congreso de Tabasco',
    'TabascoGaceta': 'Congreso de Tabasco',
    'TabascoIniciativa': 'Congreso de Tabasco',
    'TabascoPeriodicoOficial': 'Diario Oficial de Tabasco',
    'TamaulipasComunicacion': 'Congreso de Tamaulipas',
    'TamaulipasDictamenes': 'Congreso de Tamaulipas',
    'TamaulipasGaceta': 'Congreso de Tamaulipas',
    'TamaulipasIniciativa': 'Congreso de Tamaulipas',
    'TamaulipasPeriodicoOficial': 'Diario Oficial de Tamaulipas',
    'TlaxcalaComunicacion': 'Congreso de Tlaxcala',
    'TlaxcalaDictamen': 'Congreso de Tlaxcala',
    'TlaxcalaGaceta': 'Congreso de Tlaxcala',
    'TlaxcalaPeriodicoOficial': 'Diario Oficial de Tlaxcala',
    'VeracruzComunicacion': 'Congreso de Veracruz',
    'VeracruzGaceta': 'Congreso de Veracruz',
    'VeracruzIniciativa': 'Congreso de Veracruz',
    'VeracruzPeriodicoOficial': 'Diario Oficial de Veracruz',
    'YucatanComunicacion': 'Congreso de Yucatán',
    'YucatanGaceta': 'Congreso de Yucatán',
    'YucatanIniciativa': 'Congreso de Yucatán',
    'YucatanPeriodicoOficial': 'Diario Oficial de Yucatán',
    'ZacatecasComunicacion': 'Congreso de Zacatecas',
    'ZacatecasGaceta': 'Congreso de Zacatecas',
    'ZacatecasPeriodicoOficial': 'Diario Oficial de Zacatecas',
}
