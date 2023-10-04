import json
from datetime import datetime, date


class DateJSONEnconder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, o)