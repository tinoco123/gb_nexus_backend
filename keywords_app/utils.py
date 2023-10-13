from datetime import datetime

def conver_date_to_datetime(date):
    datetime_obj = datetime.combine(date, datetime.min.time())
    return datetime_obj
