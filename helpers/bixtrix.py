import logging

from django.conf import settings
from bitrix24 import Bitrix24, BitrixError

bx = Bitrix24(settings.BITRIX_URL)

logger = logging.getLogger(__name__)


def add_contact(first_name: str, last_name: str, email: str, phone: str):
    try:
        response = bx.callMethod(
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
        return response

    except BitrixError:
        pass


def add_product(name: str):
    try:
        list_response = bx.callMethod("crm.product.list", {"filter": {"NAME": name}})
        if list_response:
            return list_response[0]["ID"]

        add_response = bx.callMethod("crm.product.add", {"fields": {"NAME": name}})
        return add_response
    except BitrixError:
        pass


def add_deal(title, user_bitrix_id, price, basket_events, is_set: bool):
    try:
        add_response = bx.callMethod(
            "crm.deal.add",
            {
                "fields": {
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
        pk = add_response

        price_if_set = None
        if is_set:
            price_if_set = price / len(basket_events)

        bx.callMethod(
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

    except BitrixError:
        pass


def update_deal_stage(bitrix_id, stage: str = "EXECUTING"):
    try:
        bx.callMethod("crm.deal.add", {"id": bitrix_id, "fields": {"STAGE_ID": stage}})
    except BitrixError:
        pass


def add_task(title, deal_bitrix_id):
    try:
        bx.callMethod(
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
    except BitrixError:
        pass
