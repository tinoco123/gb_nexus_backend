import json
from bson import ObjectId
from datetime import datetime, date
import re


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
    for result in search_results:
        if result["title"] == "na" or result["title"] == "-":
            collection_name = result["collectionName"]
            result["title"] = mexico_states_dict[collection_name]
        elif result["title"] == "DESCARGA LA GACETA" and result["collectionName"] == "EdomexPeriodicoOficial":
            result["title"] = "Diario Oficial del Estado de México"


def change_title_label(search_result: dict):
    if search_result["title"] == "na" or search_result["title"] == "-":
        collection_name = search_result["collectionName"]
        search_result["title"] = mexico_states_dict[collection_name]


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
