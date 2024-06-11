from datetime import datetime
from pprint import pprint

from django.conf import settings
from fast_bitrix24 import Bitrix

bx = Bitrix(settings.BITRIX_URL)


def add_contact(first_name: str, last_name: str, email: str):
    response = bx.call(
        "crm.contact.add",
        {
            "fields": {
                "NAME": first_name,
                "LAST_NAME": last_name,
                "OPENED": "Y",
                "TYPE_ID": "CLIENT",
                "EMAIL": email,
            }
        },
    )
    return response["order0000000000"]


def list_contact():
    leads = bx.get_all("crm.contact.list")
    pprint(leads)


def add_deal(title: str, bitrix_id: int, price: int, start_at: datetime, end_at: datetime, event_prices: list):
    response = bx.call(
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
    pk = response["order0000000000"]

    bx.call(
        "crm.deal.productrows.set",
        {
            "id": pk,
            "rows": [{"PRODUCT_ID": event_price.bitrix_id, "PRICE": event_price.price} for event_price in event_prices],
        },
    )

    return pk


def add_product(name: str, price: int):
    response = bx.call("crm.product.add", {"fields": {"NAME": name, "CURRENCY_ID": "RUB", "PRICE": price}})
    return response["order0000000000"]
