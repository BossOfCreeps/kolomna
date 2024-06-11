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
    pprint(response)
    return response["order0000000000"]


def list_contact():
    leads = bx.get_all("crm.contact.list")
    pprint(leads)
