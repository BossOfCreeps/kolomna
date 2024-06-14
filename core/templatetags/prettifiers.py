from datetime import datetime, date

from django import template

from helpers import date_to_str, datetime_to_str, category_to_str

register = template.Library()


@register.simple_tag()
def datetime_to_str_tag(value: datetime):
    return datetime_to_str(value)


@register.simple_tag()
def date_to_str_tag(value: date):
    return date_to_str(value)


@register.simple_tag()
def category_to_str_tag(value: str):
    return category_to_str(value)


@register.simple_tag()
def count_price(value: list):
    return sum([v.event_price.price * v.count for v in value if v.set_id is None])
