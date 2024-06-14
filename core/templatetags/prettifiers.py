from datetime import datetime, date

from django import template

from events.models import EventSet
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


@register.filter()
def has_single_event(basket_events):
    for basket_event in basket_events:
        if basket_event.set_id is None:
            return True
    return False


@register.simple_tag()
def set_by_uuid(value):
    return EventSet.objects.get(set_id=value).id
