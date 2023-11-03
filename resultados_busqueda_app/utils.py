import json
from bson import ObjectId
from datetime import datetime, date
import re


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def resaltar_keywords(keywords: list, sinopsys: str):
    sinopsys_resaltada = sinopsys.capitalize()

    def reemplazar(match):
        return f"<strong>{match.group()}</strong>"
    for keyword in keywords:
        sinopsys_resaltada = re.sub(
            r'\b' + re.escape(keyword.lower()) + r'\b', reemplazar, sinopsys_resaltada)
    return sinopsys_resaltada

def change_title_label_when_is_na(search_results: list):
    for result in search_results:
        if result["title"] == "na":
            result["title"] = "-"
    
