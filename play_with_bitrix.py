from pprint import pprint

from fast_bitrix24 import Bitrix

# замените на ваш вебхук для доступа к Bitrix24
webhook = ""
bx = Bitrix(webhook)

pprint(
    bx.call(
        "crm.contact.add",
        {
            "fields": {
                "NAME": "Глеб",
                "SECOND_NAME": "Егорович",
                "LAST_NAME": "Титов",
                "OPENED": "Y",
                "TYPE_ID": "CLIENT",
                "PHONE": [{"VALUE": "555888", "VALUE_TYPE": "WORK"}],
            }
        },
    )
)

leads = bx.get_all("crm.contact.list")
pprint(leads)
