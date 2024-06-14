import logging

from django.conf import settings
from fast_bitrix24 import Bitrix

bx = Bitrix(settings.BITRIX_URL)

logger = logging.getLogger(__name__)


def add_contact(first_name: str, last_name: str, email: str, phone: str):
    response = bx.call(
        "crm.contact.add",
        {
            "fields": {
                "NAME": first_name,
                "LAST_NAME": last_name,
                "OPENED": "Y",
                "TYPE_ID": "CLIENT",
                "EMAIL": [{"VALUE": email, "VALUE_TYPE": "PERSONAL"}],
                "PHONE": [{"VALUE": phone, "VALUE_TYPE": "PERSONAL"}],
            }
        },
    )
    return response["order0000000000"]


def add_product(name: str):
    list_response = bx.call("crm.product.list", {"filter": {"NAME": name}})
    if list_response:
        return list_response["ID"]

    add_response = bx.call("crm.product.add", {"fields": {"NAME": name}})
    return add_response["order0000000000"]


def add_deal(title, user_bitrix_id, price, basket_events, is_set: bool):
    add_response = bx.call(
        "crm.deal.add",
        {
            "fields": {
                "ID": "11",
                "TITLE": title,
                "CONTACT_ID": user_bitrix_id,
                "CURRENCY_ID": "RUB",
                "OPPORTUNITY": price,
                "IS_NEW": "Y",
                "STAGE_ID": "NEW",  # EXECUTING
                "OPENED": "Y",
                "CLOSED": "N",
            }
        },
    )
    pk = add_response["order0000000000"]

    price_if_set = None
    if is_set:
        price_if_set = price / len(basket_events)

    bx.call(
        "crm.deal.productrows.set",
        {
            "id": pk,
            "rows": [
                {
                    "PRODUCT_ID": be.event_price.bitrix_id,
                    "QUANTITY": be.count,
                    "PRICE": be.event_price.price if price_if_set is None else price_if_set,
                }
                for be in basket_events
            ],
        },
    )

    return pk


def update_deal_stage(bitrix_id, stage: str = "EXECUTING"):
    bx.call("crm.deal.add", {"id": bitrix_id, "fields": {"STAGE_ID": stage}})


def add_task(title, deal_bitrix_id):
    bx.call(
        "tasks.task.add",
        {
            "fields": {
                "TITLE": title,
                "UF_CRM_TASK": [f"D_{deal_bitrix_id}"],
                "CREATED_BY": 1,
                "RESPONSIBLE_ID": settings.CALL_CENTER_BITRIX_USER_ID,
            }
        },
    )
