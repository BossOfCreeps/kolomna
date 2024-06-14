from django.conf import settings
from yookassa import Configuration, Payment

from users.models import CustomUser

Configuration.account_id = settings.YOOKASSA_ID
Configuration.secret_key = settings.YOOKASSA_KEY


def create_yookassa_url(total_price, purchase_ids: list[int], user: CustomUser, return_url):
    res = Payment.create(
        {
            "amount": {"value": total_price, "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": f"Заказы ({', '.join(list(map(str, purchase_ids)))})",
            #"metadata": {"orderNumber": f"{purchase_id}"},
            "receipt": {"customer": {"full_name": user.get_full_name(), "email": user.email}},
        }
    )

    return res.confirmation.confirmation_url
