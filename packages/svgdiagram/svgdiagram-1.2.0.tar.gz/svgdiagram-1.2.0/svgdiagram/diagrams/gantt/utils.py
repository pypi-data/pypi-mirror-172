from datetime import date, datetime, timedelta
import re


def str_to_date_datetime(date_string):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_string):
        return date.fromisoformat(date_string)
    else:
        return datetime.fromisoformat(date_string)


def date_datetime_to_str(date_datetime):
    return date_datetime.isoformat()


def day_iterator(start_date, end_date):
    c_date = start_date
    while c_date <= end_date:
        yield c_date
        c_date += timedelta(days=1)
