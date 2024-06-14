import logging
from datetime import datetime

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
    logger.debug(response)
    return response["order0000000000"]


def add_product(name: str):
    list_response = bx.call("crm.product.list", {"filter": {"NAME": name}})
    if list_response:
        logger.debug(list_response)
        return list_response["ID"]

    add_response = bx.call("crm.product.add", {"fields": {"NAME": name}})
    logger.debug(add_response)
    return add_response["order0000000000"]


def add_deal(title: str, bitrix_id: int, price: int, start_at: datetime, end_at: datetime, event_prices: list):
    add_response = bx.call(
        "crm.deal.add",
        {
            "fields": {
                "TITLE": title,
                "CONTACT_ID": bitrix_id,
                "CURRENCY_ID": "RUB",
                "OPPORTUNITY": price,
                "BEGINDATE": start_at.isoformat(),
                "CLOSEDATE": end_at.isoformat(),
            }
        },
    )
    pk = add_response["order0000000000"]
    logger.debug(add_response)

    set_response = bx.call(
        "crm.deal.productrows.set",
        {
            "id": pk,
            "rows": [{"PRODUCT_ID": event_price.bitrix_id, "PRICE": event_price.price} for event_price in event_prices],
        },
    )
    logger.debug(set_response)

    return pk
