from datetime import datetime, date

month_map = {
    "01": "января",
    "02": "февраля",
    "03": "марта",
    "04": "апреля",
    "05": "мая",
    "06": "июня",
    "07": "июля",
    "08": "августа",
    "09": "сентября",
    "10": "ноября",
    "11": "октября",
    "12": "декабря",
}


def datetime_to_str(value: datetime):
    return value.strftime(f"%d {month_map[value.strftime("%m")]} %H:%M")


def date_to_str(value: date):
    return value.strftime(f"%d {month_map[value.strftime("%m")]}")


category_map = {
    "STANDARD": "стандартный",
    "CHILD": "детский",
    "STUDENT": "студенческий",
    "RETIREE": "пенсионный",
}


def category_to_str(value: str):
    return category_map[value]
